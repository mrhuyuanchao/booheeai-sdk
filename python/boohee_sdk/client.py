"""核心客户端"""
import time
import threading
from typing import Optional, Dict, Any, Union
import requests

from .auth import AuthMode, rsa_sign, build_signature_string
from .cache import TokenCache
from .exceptions import AuthenticationError, APIError, NetworkError
from .request import BaseReq


class BooheeClient:
    """薄荷开放平台客户端"""

    DEFAULT_BASE_URL = "https://api.boohee.com"
    DEFAULT_TIMEOUT = 30
    TOKEN_REFRESH_BUFFER = 300

    def __init__(
        self,
        # Access Token 模式参数
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        private_key: Optional[str] = None,
        # API Key 模式参数
        api_key: Optional[str] = None,
        # 通用配置
        auth_mode: AuthMode = AuthMode.ACCESS_TOKEN,
        base_url: str = DEFAULT_BASE_URL,
        cache: Optional[TokenCache] = None,
        timeout: Union[int, float] = DEFAULT_TIMEOUT
    ):
        """
        初始化客户端

        Args:
            app_id: 应用 ID(Access Token 模式必需)
            app_key: 应用密钥(Access Token 模式必需)
            private_key: RSA 私钥 PEM 格式(Access Token 模式必需)
            api_key: API Key(API Key 模式必需)
            auth_mode: 认证模式,默认 ACCESS_TOKEN
            base_url: API 基础 URL
            cache: Token 缓存实现(可选)
            timeout: 请求超时时间(秒)
        """
        self.auth_mode = auth_mode
        self.base_url = base_url.rstrip('/')
        self.cache = cache
        self.timeout: Union[int, float] = timeout

        # Access Token 模式
        if auth_mode == AuthMode.ACCESS_TOKEN:
            if not app_id:
                raise ValueError("app_id is required for ACCESS_TOKEN mode")
            if not app_key:
                raise ValueError("app_key is required for ACCESS_TOKEN mode")
            if not private_key:
                raise ValueError("private_key is required for ACCESS_TOKEN mode")

            self.app_id = app_id
            self.app_key = app_key
            self.private_key = private_key
            self.api_key = None

            # Token 管理
            self._access_token: Optional[str] = None
            self._token_expires_at: float = 0
            self._token_lock = threading.Lock()

        # API Key 模式
        elif auth_mode == AuthMode.API_KEY:
            if not api_key:
                raise ValueError("api_key is required for API_KEY mode")

            self.api_key = api_key
            self.app_id = None
            self.app_key = None
            self.private_key = None

        else:
            raise ValueError(f"Invalid auth_mode: {auth_mode}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送 GET 请求

        Args:
            path: API 路径
            params: 查询参数

        Returns:
            API 响应(已解析为 dict)
        """
        return self._request('GET', path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送 POST 请求

        Args:
            path: API 路径
            data: 请求体数据

        Returns:
            API 响应(已解析为 dict)
        """
        return self._request('POST', path, json_data=data)

    def execute(self, req: BaseReq) -> Dict[str, Any]:
        """
        执行 BaseReq 请求

        开发者实现 `BaseReq` 子类后,通过本方法统一发起调用。
        内部会根据 `req.get_method()` 选择 GET / POST,
        并分别传入 query params 与 JSON body。

        Args:
            req: BaseReq 实例

        Returns:
            API 响应(已解析为 dict)
        """
        method = req.get_method()
        path = req.get_url()
        params = req.get_query_params()
        data = req.get_body()

        return self._request(method, path, params=params, json_data=data)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送 HTTP 请求

        Args:
            method: HTTP 方法(GET/POST)
            path: API 路径
            params: 查询参数
            json_data: JSON 请求体

        Returns:
            API 响应
        """
        url = f"{self.base_url}{path}"
        headers = self._get_headers()

        try:
            response = self._send_request(method, url, params, json_data, headers)

            # 检查响应状态:401 时自动刷新 token 并重试一次
            if response.status_code == 401 and self.auth_mode == AuthMode.ACCESS_TOKEN:
                self._force_refresh_access_token()
                headers = self._get_headers()
                response = self._send_request(method, url, params, json_data, headers)

            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    raise APIError(error_data.get('code', response.status_code),
                                 error_data.get('message', response.text))
                except (ValueError, KeyError):
                    raise APIError(response.status_code, response.text)

            return response.json()

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {str(e)}")

    def _send_request(self, method, url, params, json_data, headers):
        """发送 HTTP 请求的辅助方法"""
        if method == 'GET':
            return requests.get(url, params=params, headers=headers, timeout=self.timeout)
        elif method == 'POST':
            return requests.post(url, json=json_data, headers=headers, timeout=self.timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    def _get_headers(self) -> Dict[str, str]:
        """
        获取请求头

        Returns:
            包含认证信息的请求头
        """
        headers: Dict[str, str] = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if self.auth_mode == AuthMode.ACCESS_TOKEN:
            token = self._get_access_token()
            headers['AccessToken'] = token
        elif self.auth_mode == AuthMode.API_KEY:
            headers['X-Api-Key'] = self.api_key

        return headers

    def _get_access_token(self) -> str:
        """
        获取 access_token(自动缓存和刷新)

        Returns:
            access_token 字符串
        """
        # 检查是否已缓存且未过期
        if self._access_token and time.time() < self._token_expires_at - self.TOKEN_REFRESH_BUFFER:
            return self._access_token

        # 尝试从缓存获取
        if self.cache:
            cached_token = self.cache.get(self.app_id)
            if cached_token:
                self._access_token = cached_token
                # 保守假设:cache 返回的 token 可能在 10 分钟内过期
                # 下次调用时会触发 API 刷新
                self._token_expires_at = time.time() + 600
                return self._access_token

        # 刷新 token
        with self._token_lock:
            # 双重检查,防止并发刷新
            if self._access_token and time.time() < self._token_expires_at - self.TOKEN_REFRESH_BUFFER:
                return self._access_token

            self._refresh_access_token()
            return self._access_token

    def _refresh_access_token(self):
        """
        调用 API 刷新 access_token
        """
        timestamp = int(time.time())
        signature_str = build_signature_string(self.app_id, self.app_key, timestamp)
        sign = rsa_sign(signature_str, self.private_key)

        payload = {
            'app_id': self.app_id,
            'timestamp': timestamp,
            'sign': sign
        }

        try:
            response = requests.post(
                f"{self.base_url}/open-apis/v1/access_token",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )

            if response.status_code >= 400:
                raise AuthenticationError(f"Failed to get access_token: {response.text}")

            data = response.json()
            self._access_token = data['access_token']
            self._token_expires_at = time.time() + data['expires_in']

            # 缓存 token
            if self.cache:
                self.cache.set(self.app_id, self._access_token, data['expires_in'])

        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Token refresh failed: {str(e)}")

    def _force_refresh_access_token(self):
        """
        强制刷新 token(忽略缓存)
        """
        self._access_token = None
        self._token_expires_at = 0
        if self.cache:
            self.cache.delete(self.app_id)
        self._refresh_access_token()

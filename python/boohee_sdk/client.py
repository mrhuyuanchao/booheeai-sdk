"""核心客户端"""
import time  # TODO: used by Task 10 (token management)
import threading
from typing import Optional, Dict, Any, Union
import requests  # TODO: used by Task 9 (HTTP methods)

from .auth import AuthMode, rsa_sign, build_signature_string
from .cache import TokenCache
from .exceptions import AuthenticationError, APIError, NetworkError  # TODO: used by Task 9-10


class BooheeClient:
    """薄荷开放平台客户端"""

    DEFAULT_BASE_URL = "https://api.boohee.com"
    DEFAULT_TIMEOUT = 30
    TOKEN_REFRESH_BUFFER = 300  # TODO: used by Task 10 (token refresh)

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
            if method == 'GET':
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    json=json_data,
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # 检查响应状态
            if response.status_code == 401:
                # Token 过期,尝试刷新后重试(仅 ACCESS_TOKEN 模式)
                if self.auth_mode == AuthMode.ACCESS_TOKEN:
                    # _force_refresh_token 将在 Task 10 实现
                    # 暂时先跳过,后续补充
                    pass

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
            # _get_access_token 将在 Task 10 实现
            # 暂时使用占位,后续补充
            token = self._access_token or 'placeholder_token'
            headers['AccessToken'] = token
        elif self.auth_mode == AuthMode.API_KEY:
            headers['X-Api-Key'] = self.api_key

        return headers

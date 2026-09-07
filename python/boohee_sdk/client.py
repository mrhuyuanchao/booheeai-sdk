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

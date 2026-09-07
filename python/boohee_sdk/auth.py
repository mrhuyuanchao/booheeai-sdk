"""认证相关"""
from enum import Enum


class AuthMode(str, Enum):
    """认证模式"""
    ACCESS_TOKEN = 'access_token'
    API_KEY = 'api_key'

    def __str__(self) -> str:
        return self.value


__all__ = ['AuthMode']

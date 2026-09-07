"""认证相关"""
from enum import Enum


class AuthMode(Enum):
    """认证模式"""
    ACCESS_TOKEN = 'access_token'
    API_KEY = 'api_key'

import pytest
from boohee_sdk import BooheeClient, AuthMode


def test_client_init_access_token_mode():
    """测试 Access Token 模式初始化"""
    client = BooheeClient(
        app_id='test_app',
        app_key='test_key',
        private_key='test_key_pem'
    )
    assert client.auth_mode == AuthMode.ACCESS_TOKEN
    assert client.app_id == 'test_app'
    assert client.app_key == 'test_key'


def test_client_init_api_key_mode():
    """测试 API Key 模式初始化"""
    client = BooheeClient(
        api_key='test_api_key',
        auth_mode=AuthMode.API_KEY
    )
    assert client.auth_mode == AuthMode.API_KEY
    assert client.api_key == 'test_api_key'


def test_client_init_missing_params():
    """测试缺少必需参数"""
    with pytest.raises(ValueError, match="app_id is required"):
        BooheeClient(app_key='key', private_key='pem')

    with pytest.raises(ValueError, match="api_key is required"):
        BooheeClient(auth_mode=AuthMode.API_KEY)


def test_client_init_custom_base_url():
    """测试自定义 base_url"""
    client = BooheeClient(
        api_key='test_key',
        auth_mode=AuthMode.API_KEY,
        base_url='https://custom.api.com/'
    )
    assert client.base_url == 'https://custom.api.com'

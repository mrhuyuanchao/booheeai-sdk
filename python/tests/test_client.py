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


def test_client_default_base_url():
    """测试默认 base_url"""
    client = BooheeClient(
        api_key='test_key',
        auth_mode=AuthMode.API_KEY
    )
    assert client.base_url == 'https://api.boohee.com'


def test_client_default_timeout():
    """测试默认 timeout"""
    client = BooheeClient(
        api_key='test_key',
        auth_mode=AuthMode.API_KEY
    )
    assert client.timeout == 30


def test_client_cache_parameter():
    """测试 cache 参数"""
    from boohee_sdk.cache import TokenCache

    class MockCache:
        def get(self, app_id): return None
        def set(self, app_id, token, expires_in): pass
        def delete(self, app_id): pass

    cache = MockCache()
    client = BooheeClient(
        app_id='test',
        app_key='key',
        private_key='pem',
        cache=cache
    )
    assert client.cache is cache


def test_client_invalid_auth_mode():
    """测试无效 auth_mode"""
    with pytest.raises(ValueError, match="Invalid auth_mode"):
        BooheeClient(auth_mode="invalid")


def test_client_token_management_init():
    """测试 Token 管理属性初始化"""
    import threading
    client = BooheeClient(
        app_id='test',
        app_key='key',
        private_key='pem'
    )
    assert client._access_token is None
    assert client._token_expires_at == 0
    assert isinstance(client._token_lock, type(threading.Lock()))


def test_client_api_key_mode_isolation():
    """测试 API Key 模式属性隔离"""
    client = BooheeClient(
        api_key='test_key',
        auth_mode=AuthMode.API_KEY
    )
    assert client.app_id is None
    assert client.app_key is None
    assert client.private_key is None


def test_client_empty_string_params():
    """测试空字符串参数被拒绝"""
    with pytest.raises(ValueError):
        BooheeClient(app_id='', app_key='key', private_key='pem')

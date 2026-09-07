import pytest
import time
from unittest.mock import Mock, patch
from boohee_sdk import BooheeClient, AuthMode
from boohee_sdk.exceptions import APIError, NetworkError


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


def test_client_get_request():
    """测试 GET 请求"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response

        result = client.get('/open-apis/v1/food/search', {'keyword': 'apple'})

        assert result == {'data': 'test'}
        mock_get.assert_called_once()

        # 验证 Header 包含 X-Api-Key
        call_kwargs = mock_get.call_args[1]
        assert 'X-Api-Key' in call_kwargs['headers']
        assert call_kwargs['headers']['X-Api-Key'] == 'test_key'


def test_client_post_request():
    """测试 POST 请求"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response

        result = client.post('/open-apis/v1/weight/record', {'weight': 70.5})

        assert result == {'success': True}
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs['json'] == {'weight': 70.5}
        assert call_kwargs['headers']['X-Api-Key'] == 'test_key'


def test_client_api_error():
    """测试 API 错误处理"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'code': 400, 'message': 'invalid params'}
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            client.get('/open-apis/v1/food/search', {})

        assert exc_info.value.code == 400
        assert exc_info.value.message == 'invalid params'


def test_client_network_error():
    """测试网络错误处理"""
    import requests as req
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_get.side_effect = req.exceptions.ConnectionError("Connection refused")

        with pytest.raises(NetworkError):
            client.get('/open-apis/v1/food/search', {})


def test_client_access_token_header():
    """测试 ACCESS_TOKEN 模式的 Header"""
    client = BooheeClient(
        app_id='test',
        app_key='key',
        private_key='pem'
    )
    # 设置一个未过期的 token
    client._access_token = 'test_token'
    client._token_expires_at = time.time() + 3600

    headers = client._get_headers()
    assert headers['AccessToken'] == 'test_token'
    assert 'X-Api-Key' not in headers


def test_client_invalid_method():
    """测试不支持的 HTTP 方法"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client._request('DELETE', '/test')


def test_token_refresh():
    """测试 Token 自动刷新"""
    client = BooheeClient(
        app_id='test_app',
        app_key='test_key',
        private_key='test_private_key'
    )

    with patch('requests.post') as mock_post:
        # Mock AccessToken API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_token',
            'expires_in': 86400
        }
        mock_post.return_value = mock_response

        # Mock RSA 签名
        with patch('boohee_sdk.client.rsa_sign') as mock_sign:
            mock_sign.return_value = 'mock_signature'

            token = client._get_access_token()

            assert token == 'new_token'
            assert mock_post.called


def test_token_cache():
    """测试 Token 缓存"""

    class MockCache:
        def __init__(self):
            self.storage = {}
        def get(self, app_id):
            return self.storage.get(app_id)
        def set(self, app_id, token, expires_in):
            self.storage[app_id] = token
        def delete(self, app_id):
            self.storage.pop(app_id, None)

    cache = MockCache()
    client = BooheeClient(
        app_id='test_app',
        app_key='test_key',
        private_key='test_private_key',
        cache=cache
    )

    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'cached_token',
            'expires_in': 86400
        }
        mock_post.return_value = mock_response

        with patch('boohee_sdk.client.rsa_sign') as mock_sign:
            mock_sign.return_value = 'mock_signature'

            # 第一次获取,应该调用 API
            token1 = client._get_access_token()
            assert token1 == 'cached_token'
            assert cache.get('test_app') == 'cached_token'


def test_token_401_retry():
    """测试 401 自动重试"""
    client = BooheeClient(
        app_id='test_app',
        app_key='test_key',
        private_key='test_private_key'
    )
    client._access_token = 'expired_token'
    client._token_expires_at = time.time() + 3600

    with patch('requests.get') as mock_get:
        # 第一次返回 401
        mock_401 = Mock()
        mock_401.status_code = 401

        # 第二次返回 200
        mock_200 = Mock()
        mock_200.status_code = 200
        mock_200.json.return_value = {'data': 'success'}

        mock_get.side_effect = [mock_401, mock_200]

        # Mock token refresh to avoid RSA key parsing
        mock_post = Mock()
        mock_post.status_code = 200
        mock_post.json.return_value = {'access_token': 'new_token', 'expires_in': 86400}

        with patch('requests.post', return_value=mock_post):
            with patch('boohee_sdk.client.rsa_sign', return_value='mock_signature'):
                result = client.get('/test', {})

        assert result == {'data': 'success'}
        assert mock_get.call_count == 2


def test_client_server_error():
    """测试 5xx 服务端错误"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'code': 500, 'message': 'internal error'}
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            client.get('/test', {})

        assert exc_info.value.code == 500


def test_client_401_api_key_mode():
    """测试 401 在 API_KEY 模式下抛出 APIError"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'code': 401, 'message': 'invalid api key'}
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            client.get('/test', {})

        assert exc_info.value.code == 401

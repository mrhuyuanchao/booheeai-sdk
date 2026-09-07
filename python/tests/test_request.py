"""BaseReq 接口与 BooheeClient.execute 的测试"""
from typing import Dict, Any
from unittest.mock import Mock, patch

from boohee_sdk import BooheeClient, AuthMode, BaseReq


# ===== 测试用的 BaseReq 子类 =====

class FoodSearchReq(BaseReq):
    """食物搜索请求示例"""

    def __init__(self, keyword: str, page: int = 1):
        self.keyword = keyword
        self.page = page

    def get_method(self) -> str:
        return 'GET'

    def get_url(self) -> str:
        return '/open-apis/v1/food/search'

    def get_query_params(self) -> Dict[str, Any]:
        return {
            'keyword': self.keyword,
            'page': self.page,
        }


class WeightRecordReq(BaseReq):
    """记录体重请求示例"""

    def __init__(self, user_id: str, weight: float):
        self.user_id = user_id
        self.weight = weight

    def get_method(self) -> str:
        return 'POST'

    def get_url(self) -> str:
        return '/open-apis/v1/weight/record'

    def get_body(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'weight': self.weight,
        }


class MinimalGetReq(BaseReq):
    """最小 GET:只实现抽象方法,依赖 query_params/body 默认值"""

    def get_method(self) -> str:
        return 'GET'

    def get_url(self) -> str:
        return '/open-apis/v1/ping'


class MinimalPostReq(BaseReq):
    """最小 POST:只实现抽象方法"""

    def get_method(self) -> str:
        return 'POST'

    def get_url(self) -> str:
        return '/open-apis/v1/ping'


# ===== BaseReq 行为测试 =====

def test_base_req_get():
    """测试 GET 请求的各 accessor"""
    req = FoodSearchReq('apple', page=2)
    assert req.get_method() == 'GET'
    assert req.get_url() == '/open-apis/v1/food/search'
    assert req.get_query_params() == {'keyword': 'apple', 'page': 2}
    assert req.get_body() is None


def test_base_req_post():
    """测试 POST 请求的各 accessor"""
    req = WeightRecordReq('user123', 70.5)
    assert req.get_method() == 'POST'
    assert req.get_url() == '/open-apis/v1/weight/record'
    assert req.get_body() == {'user_id': 'user123', 'weight': 70.5}
    assert req.get_query_params() is None


def test_base_req_defaults():
    """测试未重写时 query_params / body 默认为 None"""
    req = MinimalGetReq()
    assert req.get_query_params() is None
    assert req.get_body() is None


def test_base_req_is_abstract():
    """BaseReq 不能直接实例化"""
    import pytest
    with pytest.raises(TypeError):
        BaseReq()  # type: ignore[abstract]


# ===== BooheeClient.execute 集成测试 =====

def test_client_execute_get():
    """测试 execute 走 GET:参数透传到 requests.get 的 params"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'foods': []}
        mock_get.return_value = mock_response

        req = FoodSearchReq('apple', page=3)
        result = client.execute(req)

        assert result == {'foods': []}
        mock_get.assert_called_once()

        call_kwargs = mock_get.call_args[1]
        assert call_kwargs['params'] == {'keyword': 'apple', 'page': 3}
        # GET 不应传 json body
        assert 'json' not in call_kwargs or call_kwargs['json'] is None
        assert call_kwargs['headers']['X-Api-Key'] == 'test_key'


def test_client_execute_post():
    """测试 execute 走 POST:参数透传到 requests.post 的 json"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response

        req = WeightRecordReq('user123', 70.5)
        result = client.execute(req)

        assert result == {'success': True}
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs['json'] == {'user_id': 'user123', 'weight': 70.5}
        assert call_kwargs['headers']['X-Api-Key'] == 'test_key'


def test_client_execute_with_defaults():
    """测试 execute 在 query_params/body 为 None 时也能正常调用"""
    client = BooheeClient(api_key='test_key', auth_mode=AuthMode.API_KEY)

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'pong': True}
        mock_get.return_value = mock_response

        result = client.execute(MinimalGetReq())
        assert result == {'pong': True}
        mock_get.assert_called_once()

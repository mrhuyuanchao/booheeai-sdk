from boohee_sdk.auth import AuthMode


def test_auth_mode_values():
    """测试认证模式枚举值"""
    assert AuthMode.ACCESS_TOKEN.value == 'access_token'
    assert AuthMode.API_KEY.value == 'api_key'


def test_auth_mode_enum():
    """测试枚举类型"""
    mode = AuthMode.ACCESS_TOKEN
    assert isinstance(mode, AuthMode)
    assert mode.name == 'ACCESS_TOKEN'

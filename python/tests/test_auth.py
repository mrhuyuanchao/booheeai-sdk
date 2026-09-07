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


def test_auth_mode_string_interop():
    """测试字符串互操作"""
    assert AuthMode.ACCESS_TOKEN == 'access_token'
    assert f"{AuthMode.API_KEY}" == 'api_key'


def test_auth_mode_lookup():
    """测试值查找"""
    assert AuthMode('access_token') == AuthMode.ACCESS_TOKEN
    assert AuthMode('api_key') == AuthMode.API_KEY


def test_auth_mode_invalid_value():
    """测试无效值"""
    import pytest
    with pytest.raises(ValueError):
        AuthMode('invalid')


def test_auth_mode_immutable():
    """测试不可变性"""
    import pytest
    with pytest.raises(AttributeError):
        AuthMode.ACCESS_TOKEN = 'changed'


def test_auth_mode_iteration():
    """测试迭代"""
    modes = list(AuthMode)
    assert len(modes) == 2
    assert AuthMode.ACCESS_TOKEN in modes
    assert AuthMode.API_KEY in modes


def test_auth_mode_identity():
    """测试身份唯一性"""
    assert AuthMode.ACCESS_TOKEN is AuthMode.ACCESS_TOKEN
    assert AuthMode.API_KEY is AuthMode.API_KEY

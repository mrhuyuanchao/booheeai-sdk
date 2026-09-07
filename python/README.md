# 薄荷健康开放平台 Python SDK

## 安装

```bash
pip install boohee-sdk
```

## 快速开始

### Access Token 模式

```python
from boohee_sdk import BooheeClient
from boohee_sdk.endpoints import ENDPOINT_FOOD_SEARCH

# 初始化客户端
client = BooheeClient(
    app_id='your_app_id',
    app_key='your_app_key',
    private_key=open('private.pem').read()
)

# 搜索食物
result = client.get(ENDPOINT_FOOD_SEARCH, {
    'keyword': 'apple',
    'page': 1,
    'per_page': 20
})
print(result)
```

### API Key 模式

```python
from boohee_sdk import BooheeClient, AuthMode
from boohee_sdk.endpoints import ENDPOINT_FOOD_SEARCH

client = BooheeClient(
    api_key='your_api_key',
    auth_mode=AuthMode.API_KEY
)

result = client.get(ENDPOINT_FOOD_SEARCH, {'keyword': 'banana'})
print(result)
```

### Token 缓存

```python
import redis
from boohee_sdk import BooheeClient

class RedisTokenCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, app_id):
        return self.redis.get(f"boohee:token:{app_id}")

    def set(self, app_id, token, expires_in):
        self.redis.setex(f"boohee:token:{app_id}", expires_in, token)

    def delete(self, app_id):
        self.redis.delete(f"boohee:token:{app_id}")

redis_client = redis.Redis(host='localhost', port=6379)
cache = RedisTokenCache(redis_client)

client = BooheeClient(
    app_id='your_app_id',
    app_key='your_app_key',
    private_key=open('private.pem').read(),
    cache=cache
)
```

## API 端点

所有 API 端点都定义为常量,在 `boohee_sdk.endpoints` 模块中:

```python
from boohee_sdk.endpoints import (
    ENDPOINT_FOOD_SEARCH,
    ENDPOINT_FOOD_DETAIL,
    ENDPOINT_WEIGHT_RECORD,
    # ... 63 个端点
)
```

完整列表请查看源码 `boohee_sdk/endpoints.py`。

## 错误处理

```python
from boohee_sdk.exceptions import AuthenticationError, APIError, NetworkError

try:
    result = client.get(ENDPOINT_FOOD_SEARCH, {'keyword': 'apple'})
except AuthenticationError as e:
    print(f"认证失败: {e}")
except APIError as e:
    print(f"API 错误 {e.code}: {e.message}")
except NetworkError as e:
    print(f"网络错误: {e}")
```

## 开发

```bash
# 安装开发依赖
pip install -e .
pip install pytest

# 运行测试
pytest tests/ -v
```

## License

MIT

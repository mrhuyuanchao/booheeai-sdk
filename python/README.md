# 薄荷健康开放平台 Python SDK

## 安装

```bash
pip install boohee-sdk
```

## 快速开始

SDK 采用 `BaseReq` 接口模式:开发者通过继承 `BaseReq` 描述一次 API 调用
(URL、HTTP 方法、query / body),再交给 `BooheeClient.execute(req)` 统一执行。

### API Key 模式

```python
from typing import Dict, Any
from boohee_sdk import BooheeClient, AuthMode, BaseReq

# 1. 定义请求类
class FoodSearchReq(BaseReq):
    def __init__(self, keyword: str, page: int = 1):
        self.keyword = keyword
        self.page = page

    def get_method(self) -> str:
        return 'GET'

    def get_url(self) -> str:
        return '/open-apis/v1/food/search'

    def get_query_params(self) -> Dict[str, Any]:
        return {'keyword': self.keyword, 'page': self.page}

# 2. 初始化客户端
client = BooheeClient(
    api_key='your_api_key',
    auth_mode=AuthMode.API_KEY
)

# 3. 执行请求
req = FoodSearchReq('apple', page=1)
result = client.execute(req)
print(result)
```

### Access Token 模式

```python
from boohee_sdk import BooheeClient, BaseReq

client = BooheeClient(
    app_id='your_app_id',
    app_key='your_app_key',
    private_key=open('private.pem').read()
)

# 复用上面的 FoodSearchReq
result = client.execute(FoodSearchReq('apple'))
print(result)
```

### POST 请求示例

```python
class WeightRecordReq(BaseReq):
    def __init__(self, weight: float):
        self.weight = weight

    def get_method(self) -> str:
        return 'POST'

    def get_url(self) -> str:
        return '/open-apis/v1/weight/record'

    def get_body(self):
        return {'weight': self.weight}

client.execute(WeightRecordReq(70.5))
```

### `BaseReq` 接口

```python
class BaseReq(ABC):
    def get_method(self) -> str:            # 必需:'GET' 或 'POST'
    def get_url(self) -> str:               # 必需:API 路径
    def get_query_params(self) -> Optional[Dict[str, Any]]:  # 可选,默认 None
    def get_body(self) -> Optional[Dict[str, Any]]:          # 可选,默认 None
```

只需继承并实现 `get_method` / `get_url`,其余按需重写。

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

## API 端点参考

过去 SDK 通过 `boohee_sdk.endpoints` 导出 63 个端点常量;自 v0.2.0 起,
端点常量已移至 `examples/endpoints_example.py` 作为参考清单,
建议直接在 `BaseReq.get_url()` 中写回需要的路径。

## 错误处理

```python
from boohee_sdk.exceptions import AuthenticationError, APIError, NetworkError

try:
    result = client.execute(FoodSearchReq('apple'))
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

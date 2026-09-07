#!/usr/bin/env python3
"""基础使用示例 —— BaseReq 接口模式"""

from typing import Optional, Dict, Any

from boohee_sdk import BooheeClient, AuthMode, BaseReq


# ===== 1. 定义请求类 =====

class FoodSearchReq(BaseReq):
    """搜索食物(GET 请求示例)"""

    def __init__(self, keyword: str, page: int = 1, per_page: int = 20):
        self.keyword = keyword
        self.page = page
        self.per_page = per_page

    def get_method(self) -> str:
        return 'GET'

    def get_url(self) -> str:
        return '/open-apis/v1/food/search'

    def get_query_params(self) -> Dict[str, Any]:
        return {
            'keyword': self.keyword,
            'page': self.page,
            'per_page': self.per_page,
        }


class WeightRecordReq(BaseReq):
    """记录体重(POST 请求示例)"""

    def __init__(self, weight: float, recorded_at: Optional[str] = None):
        self.weight = weight
        self.recorded_at = recorded_at

    def get_method(self) -> str:
        return 'POST'

    def get_url(self) -> str:
        return '/open-apis/v1/weight/record'

    def get_body(self) -> Dict[str, Any]:
        body: Dict[str, Any] = {'weight': self.weight}
        if self.recorded_at:
            body['recorded_at'] = self.recorded_at
        return body


# ===== 2. 使用客户端执行 =====

def api_key_example():
    client = BooheeClient(
        api_key='your_api_key_here',
        auth_mode=AuthMode.API_KEY
    )

    # GET
    result = client.execute(FoodSearchReq('apple', page=1))
    print("搜索结果:", result)

    # POST
    result = client.execute(WeightRecordReq(70.5))
    print("记录结果:", result)


def access_token_example():
    private_key = """-----BEGIN RSA PRIVATE KEY-----
...your private key...
-----END RSA PRIVATE KEY-----"""

    client = BooheeClient(
        app_id='your_app_id',
        app_key='your_app_key',
        private_key=private_key
    )

    result = client.execute(FoodSearchReq('banana'))
    print("搜索结果:", result)


if __name__ == '__main__':
    # 运行示例(需要替换真实的凭证)
    # api_key_example()
    # access_token_example()
    print("请替换示例中的凭证后运行")

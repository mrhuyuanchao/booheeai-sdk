#!/usr/bin/env python3
"""基础使用示例"""

from boohee_sdk import BooheeClient, AuthMode
from boohee_sdk.endpoints import ENDPOINT_FOOD_SEARCH


# API Key 模式示例
def api_key_example():
    client = BooheeClient(
        api_key='your_api_key_here',
        auth_mode=AuthMode.API_KEY
    )

    result = client.get(ENDPOINT_FOOD_SEARCH, {
        'keyword': 'apple',
        'page': 1,
        'per_page': 10
    })
    print("搜索结果:", result)


# Access Token 模式示例
def access_token_example():
    # 假设你已经有 RSA 私钥
    private_key = """-----BEGIN RSA PRIVATE KEY-----
...your private key...
-----END RSA PRIVATE KEY-----"""

    client = BooheeClient(
        app_id='your_app_id',
        app_key='your_app_key',
        private_key=private_key
    )

    result = client.get(ENDPOINT_FOOD_SEARCH, {
        'keyword': 'banana',
        'page': 1
    })
    print("搜索结果:", result)


if __name__ == '__main__':
    # 运行示例(需要替换真实的凭证)
    # api_key_example()
    # access_token_example()
    print("请替换示例中的凭证后运行")

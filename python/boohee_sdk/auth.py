"""认证相关"""
import base64
from enum import Enum

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss


class AuthMode(str, Enum):
    """认证模式"""
    ACCESS_TOKEN = 'access_token'
    API_KEY = 'api_key'

    def __str__(self) -> str:
        return self.value


def rsa_sign(plaintext: str, private_key_pem: str) -> str:
    """
    RSA-PSS + SHA256 签名

    Args:
        plaintext: 待签名的字符串
        private_key_pem: RSA 私钥 PEM 格式字符串

    Returns:
        Base64 编码的签名字符串
    """
    key = RSA.import_key(private_key_pem)
    h = SHA256.new(plaintext.encode("utf-8"))
    signature = pss.new(key).sign(h)
    return base64.b64encode(signature).decode("utf-8")


__all__ = ['AuthMode', 'rsa_sign']

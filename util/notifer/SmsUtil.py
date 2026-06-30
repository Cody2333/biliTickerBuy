import hashlib
import hmac
import json
import time
import uuid
import urllib.parse
import base64

import requests
import loguru

from util.notifer.Notifier import NotifierBase


def _sign_aliyun(access_key_secret: str, string_to_sign: str) -> str:
    """HMAC-SHA1 sign and base64 encode."""
    mac = hmac.new(
        f"{access_key_secret}&".encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    )
    return base64.b64encode(mac.digest()).decode("utf-8")


def _build_aliyun_signature(params: dict, access_key_secret: str, method: str = "POST") -> str:
    """Build Alibaba Cloud POP signature (HMAC-SHA1)."""
    # Sort params, build canonicalized query string
    sorted_keys = sorted(params.keys())
    encoded_params = []
    for k in sorted_keys:
        v = str(params[k])
        encoded_params.append(
            f"{urllib.parse.quote(k, safe='~')}={urllib.parse.quote(v, safe='~')}"
        )
    canonicalized_query = "&".join(encoded_params)

    string_to_sign = f"{method}&{urllib.parse.quote('/', safe='~')}&{urllib.parse.quote(canonicalized_query, safe='~')}"
    return _sign_aliyun(access_key_secret, string_to_sign)


def send_sms(
    access_key_id: str,
    access_key_secret: str,
    phone_numbers: str,
    sign_name: str,
    template_code: str,
    template_param: dict | None = None,
) -> dict:
    """Send SMS via Alibaba Cloud Dysmsapi.

    Args:
        access_key_id: Alibaba Cloud AccessKey ID.
        access_key_secret: Alibaba Cloud AccessKey Secret.
        phone_numbers: Comma-separated phone numbers (e.g. "13800138000,13900139000").
        sign_name: SMS signature name (must be approved).
        template_code: SMS template code (e.g. "SMS_123456789").
        template_param: Template variables dict (e.g. {"code": "1234"}).

    Returns:
        API response dict.
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    nonce = str(uuid.uuid4())

    params = {
        "AccessKeyId": access_key_id,
        "Action": "SendSms",
        "Format": "JSON",
        "PhoneNumbers": phone_numbers,
        "SignName": sign_name,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureNonce": nonce,
        "SignatureVersion": "1.0",
        "TemplateCode": template_code,
        "TemplateParam": json.dumps(template_param or {}, ensure_ascii=False),
        "Timestamp": timestamp,
        "Version": "2017-05-25",
    }

    signature = _build_aliyun_signature(params, access_key_secret)
    params["Signature"] = signature

    url = "https://dysmsapi.aliyuncs.com/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=params, headers=headers, timeout=15)
    response.raise_for_status()
    result = response.json()

    if result.get("Code") != "OK":
        raise RuntimeError(f"短信发送失败: {result.get('Message', result)}")

    return result


class SmsNotifier(NotifierBase):
    """阿里云短信通知器。

    Config fields:
        sms_access_key_id:    阿里云 AccessKey ID
        sms_access_key_secret: 阿里云 AccessKey Secret
        sms_sign_name:        短信签名（需审核通过）
        sms_template_code:    短信模板代码
        sms_phone_numbers:    接收手机号，多个用逗号分隔
    """

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        sign_name: str,
        template_code: str,
        phone_numbers: str,
        title: str = "",
        content: str = "",
        interval_seconds: int = 10,
        duration_minutes: int = 10,
    ):
        super().__init__(title, content, interval_seconds, duration_minutes)
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.sign_name = sign_name
        self.template_code = template_code
        self.phone_numbers = phone_numbers

    def send_message(self, title: str, message: str):
        """Send SMS via Alibaba Cloud."""
        if not all(
            [
                self.access_key_id,
                self.access_key_secret,
                self.sign_name,
                self.template_code,
                self.phone_numbers,
            ]
        ):
            raise ValueError("短信通知配置不完整，请检查 AccessKey、签名、模板和手机号")

        # 将 title + message 内容放入模板变量
        # 用户的短信模板需要包含 ${content} 变量
        template_param = {"title": title, "content": message}

        result = send_sms(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            phone_numbers=self.phone_numbers,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=template_param,
        )
        loguru.logger.info(f"短信发送成功: {result.get('BizId', 'N/A')}")
from dataclasses import dataclass

from app_cmd.config.ConfigBasic import BasicConfig, config_field, str_to_bool


@dataclass(slots=True)
class NotifierConfig(BasicConfig):
    """Notification channels used after success or proxy exhaustion."""

    serverchan_key: str = config_field(
        "",
        env="BTB_SERVERCHANKEY",
        runtime="serverchanKey",
        db="serverchanKey",
        cli="--notifier-config.serverchan-key",
    )
    """ServerChan Turbo send key."""

    serverchan3_api_url: str = config_field(
        "",
        env="BTB_SERVERCHAN3APIURL",
        runtime="serverchan3ApiUrl",
        db="serverchan3ApiUrl",
        cli="--notifier-config.serverchan3-api-url",
    )
    """ServerChan3 API endpoint."""

    pushplus_token: str = config_field(
        "",
        env="BTB_PUSHPLUSTOKEN",
        runtime="pushplusToken",
        db="pushplusToken",
        cli="--notifier-config.pushplus-token",
    )
    """PushPlus token."""

    bark_token: str = config_field(
        "",
        env="BTB_BARKTOKEN",
        runtime="barkToken",
        db="barkToken",
        cli="--notifier-config.bark-token",
    )
    """Bark token or self-hosted Bark push path."""

    ntfy_url: str = config_field(
        "",
        env="BTB_NTFY_URL",
        runtime="ntfy_url",
        db="ntfyUrl",
        cli="--notifier-config.ntfy-url",
    )
    """ntfy topic URL."""

    ntfy_username: str = config_field(
        "",
        env="BTB_NTFY_USERNAME",
        runtime="ntfy_username",
        db="ntfyUsername",
        cli="--notifier-config.ntfy-username",
    )
    """Username for ntfy authentication."""

    ntfy_password: str = config_field(
        "",
        env="BTB_NTFY_PASSWORD",
        runtime="ntfy_password",
        db="ntfyPassword",
        cli="--notifier-config.ntfy-password",
    )
    """Password for ntfy authentication."""

    meow_nickname: str = config_field(
        "",
        env="BTB_MEOWNICKNAME",
        runtime="meowNickname",
        db="meowNickname",
        cli="--notifier-config.meow-nickname",
    )
    """MeoW nickname."""

    audio_path: str = config_field(
        "",
        env="BTB_AUDIO_PATH",
        runtime="audio_path",
        db="audioPath",
        cli="--notifier-config.audio-path",
    )
    """Local audio file played after success."""

    sms_access_key_id: str = config_field(
        "",
        env="BTB_SMS_ACCESS_KEY_ID",
        runtime="sms_access_key_id",
        db="smsAccessKeyId",
        cli="--notifier-config.sms-access-key-id",
    )
    """阿里云短信 AccessKey ID."""

    sms_access_key_secret: str = config_field(
        "",
        env="BTB_SMS_ACCESS_KEY_SECRET",
        runtime="sms_access_key_secret",
        db="smsAccessKeySecret",
        cli="--notifier-config.sms-access-key-secret",
    )
    """阿里云短信 AccessKey Secret."""

    sms_sign_name: str = config_field(
        "",
        env="BTB_SMS_SIGN_NAME",
        runtime="sms_sign_name",
        db="smsSignName",
        cli="--notifier-config.sms-sign-name",
    )
    """阿里云短信签名（需审核通过）."""

    sms_template_code: str = config_field(
        "",
        env="BTB_SMS_TEMPLATE_CODE",
        runtime="sms_template_code",
        db="smsTemplateCode",
        cli="--notifier-config.sms-template-code",
    )
    """阿里云短信模板代码（如 SMS_123456789）."""

    sms_phone_numbers: str = config_field(
        "",
        env="BTB_SMS_PHONE_NUMBERS",
        runtime="sms_phone_numbers",
        db="smsPhoneNumbers",
        cli="--notifier-config.sms-phone-numbers",
    )
    """接收短信的手机号，多个用逗号分隔（如 13800138000,13900139000）."""

    notify_proxy_exhausted: bool = config_field(
        False,
        env="BTB_NOTIFY_PROXY_EXHAUSTED",
        runtime="notify_proxy_exhausted",
        db="notifyProxyExhausted",
        cast=str_to_bool,
        cli_true="--notifier-config.notify-proxy-exhausted",
    )
    """Send a notification when all proxies enter cooldown."""

    @classmethod
    def from_runtime_options(cls, runtime_options) -> "NotifierConfig":
        data = (
            runtime_options.to_dict()
            if hasattr(runtime_options, "to_dict")
            else dict(runtime_options)
        )
        return cls.from_mapping(data, source_name="runtime")

    @classmethod
    def from_config_db(cls) -> "NotifierConfig":
        from util import ConfigDB

        return cls.from_config_getter(ConfigDB.get)

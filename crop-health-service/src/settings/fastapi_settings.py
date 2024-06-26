from typing import List, Optional

from .base_settings_mixin import BaseSettingMixin


class FastApiAppSetting(BaseSettingMixin):
    FASTAPI_DEBUG: bool = False
    FASTAPI_RELOAD: bool = False
    FASTAPI_SECRET_KEY: Optional[str] = "None"
    FASTAPI_OPEN_API_URL: Optional[str] = "/openapi.json"  # "/openapi.json"
    FASTAPI_DOCS_URL: Optional[str] = "/docs" # "/docs"
    FASTAPI_REDOC_URL: Optional[str] = "/redoc"  # "/redoc"

    # -----------------fastapi middleware-----------------
    FASTAPI_MIDDLEWARE_ENABLE_BruteForceDefenderMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_IpProtectionMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_TrustedHostMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_CORSMiddleware: bool = True
    FASTAPI_MIDDLEWARE_ENABLE_SessionMiddleware: bool = False
    FASTAPI_MIDDLEWARE_ENABLE_GZipMiddleware: bool = True

    FASTAPI_MIDDLEWARE_TRUSTED_HOST: List[str] = ["localhost", "127.0.0.1"]
    FASTAPI_MIDDLEWARE_LOCAL_IPS: List[str] = ["127.0.0.1", "localhost"]
    FASTAPI_MIDDLEWARE_ADMIN_IPS: List[str] = [""]

    FASTAPI_MIDDLEWARE_CORS_ALLOW_ORIGINS: List[str] = ["*"]
    FASTAPI_MIDDLEWARE_CORS_ALLOW_METHODS: List[str] = ["*"]
    FASTAPI_MIDDLEWARE_CORS_ALLOW_HEADERES: List[str] = ["*"]
    FASTAPI_MIDDLEWARE_GZIP_MINIMUM_SIZE: int = 1000
    # -----------------end-----------------

    def create_fastapi_app():
        pass
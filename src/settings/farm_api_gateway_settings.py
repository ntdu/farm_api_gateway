import logging
import os
from datetime import timezone
from typing import Dict, List, Optional

from .fastapi_settings import FastApiAppSetting
from .gunicorn_settings import GunicornSetting
from .redis_settings import RedisSetting
from .socketio_app_settings import AppSocketIoSetting

class FarmAPIGatewaySetting(
    FastApiAppSetting,
    GunicornSetting,
    RedisSetting,
    AppSocketIoSetting
):
    SERVICE_BASE_DIR: Optional[str] = os.getcwd()
    SERVICE_LOG_LEVEL: int = logging.INFO

    # Service info
    SERVICE_HOST: Optional[str] = ""
    SERVICE_PORT: Optional[int] = ""
    SERVICE_DOMAIN: Optional[str] = ""

    # Project
    PROJECT_NAME: Optional[str] = 'Farm API Gateway'
    PROJECT_DESCRIPTION: str = 'Description'

    # Service proxy
    SERVICE_USE_PROXY: Optional[bool] = False
    SERVICE_PROXY_ADDR: Optional[str] = ""
    SERVICE_NO_PROXY: Optional[str] = ""


__env_file_path = FarmAPIGatewaySetting.get_env_file_path(FarmAPIGatewaySetting.get_selected_env())
settings = FarmAPIGatewaySetting()
settings.setup(__env_file_path)

gconfig = FarmAPIGatewaySetting.create_gunicorn_config()

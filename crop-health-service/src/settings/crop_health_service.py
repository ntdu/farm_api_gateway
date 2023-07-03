import logging
import os
from datetime import timezone
from typing import Dict, List, Optional

from .fastapi_settings import FastApiAppSetting
from .gunicorn_settings import GunicornSetting
from .redis_settings import RedisSetting
from .socketio_app_settings import AppSocketIoSetting

class CropHealthServiceSetting(
    FastApiAppSetting,
    GunicornSetting,
    RedisSetting,
    AppSocketIoSetting
):
    SERVICE_BASE_DIR: Optional[str] = os.getcwd()
    SERVICE_LOG_LEVEL: int = logging.INFO

    # Project
    PROJECT_NAME: Optional[str] = 'CROP HEALTH SERVICE'
    PROJECT_DESCRIPTION: str = 'Description'

    # Service proxy
    SERVICE_USE_PROXY: Optional[bool] = False
    SERVICE_PROXY_ADDR: Optional[str] = ""
    SERVICE_NO_PROXY: Optional[str] = ""


__env_file_path = CropHealthServiceSetting.get_env_file_path(CropHealthServiceSetting.get_selected_env())
settings = CropHealthServiceSetting()
settings.setup(__env_file_path)

gconfig = settings.create_gunicorn_config()
locals().update(gconfig)
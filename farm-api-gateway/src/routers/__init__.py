# -*- coding: utf-8 -*-
from .auth_forward import router as auth_forward_router
from .crop_health_engine import router as crop_health_engine_router

routers = (
    auth_forward_router,
    crop_health_engine_router,
)

# -*- coding: utf-8 -*-
from src.settings import settings  # noqa # isort:skip
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response

from .events import shutdown_events, startup_events
from .middlewares import middlewares
from src.routers import routers


default_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
        Hello, welcome to {project_name}
    </body>
    </html>
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=settings.FASTAPI_DOCS_URL,
    redoc_url=settings.FASTAPI_REDOC_URL,
    openapi_url=settings.FASTAPI_OPEN_API_URL,
    on_startup=startup_events,
    on_shutdown=shutdown_events,
)

app.mount('/statics', StaticFiles(directory="statics"), name='statics')

# add routers
for x_router in routers:
    if x_router and isinstance(x_router, APIRouter):
        app.include_router(x_router)
        continue
    print(f'routers expected an instance of APIRouter but get {type(x_router)}')

# home pages
service_home_page = default_page.format(
    project_name=settings.PROJECT_NAME,
)

@app.get("/", response_class=HTMLResponse)
async def app_root():
    return service_home_page
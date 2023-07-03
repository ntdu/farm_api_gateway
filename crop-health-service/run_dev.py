import uvicorn

from src.settings import settings   # noqa # isort:skip    this is required, do NOT change or remove


if __name__ == '__main__':
    print(f'{settings.GUNICORN_HOST=} - {settings.GUNICORN_PORT}')
    uvicorn.run(
        'src.main:app',
        reload=settings.FASTAPI_RELOAD,
        host=settings.GUNICORN_HOST,
        port=int(settings.GUNICORN_PORT),
        reload_dirs=[
            # os.path.join(os.getcwd(), 'src')
        ],
        timeout_keep_alive=settings.WS_SERVER_KEEP_ALIVE,
        ws_max_size=settings.WS_SERVER_MAX_FILE_SIZE,
    )


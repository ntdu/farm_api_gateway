import os
import json
import multiprocessing
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class GunicornSetting(BaseSettingMixin):
    GUNICORN_HOST: str = '0.0.0.0'
    GUNICORN_PORT: str = '5010'
    GUNICORN_BIND_PATH: Optional[str] = None
    GUNICORN_WORKER_CONCURRENCY: Optional[int] = 4

    GUNICORN_ACCESS_LOG: Optional[str] = '-'    # default log to console
    GUNICORN_ERROR_LOG: Optional[str] = '-'     # default log to console

    def create_gunicorn_config(self):
        log_dir = os.path.join(os.getcwd(), 'log', 'gunicorn')
        _worker_tmp_dir = os.path.join(os.getcwd(), 'log', 'gunicorn', 'tmp')
        for i in (log_dir, _worker_tmp_dir):
            if not os.path.isdir(i):
                os.makedirs(i)

        workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
        max_workers_str = os.getenv("MAX_WORKERS")
        use_max_workers = None
        if max_workers_str:
            use_max_workers = int(max_workers_str)

        web_concurrency_str = os.getenv("GUNICORN_WORKER_CONCURRENCY", self.GUNICORN_WORKER_CONCURRENCY)

        host = os.getenv("HOST", self.GUNICORN_HOST)
        port = os.getenv("PORT", self.GUNICORN_PORT)
        loglevel = os.getenv("LOG_LEVEL", "info")

        cores = multiprocessing.cpu_count()
        workers_per_core = float(workers_per_core_str)
        default_web_concurrency = workers_per_core * cores
        if web_concurrency_str:
            web_concurrency = int(web_concurrency_str)
            assert web_concurrency > 0
        else:
            web_concurrency = max(int(default_web_concurrency), 2)
            if use_max_workers:
                web_concurrency = min(web_concurrency, use_max_workers)

        accesslog = os.getenv("ACCESS_LOG", os.path.join(log_dir, 'access.log')) or None
        errorlog = os.getenv("ERROR_LOG", os.path.join(log_dir, 'error.log')) or None
        graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
        timeout_str = os.getenv("TIMEOUT", "120")
        keepalive_str = os.getenv("KEEP_ALIVE", "120")

        bind = f"{host}:{port}"

        gconfig = {
            "loglevel": loglevel,
            "workers": web_concurrency,
            "bind": bind,
            "graceful_timeout": int(graceful_timeout_str),
            "timeout": int(timeout_str),
            "keepalive": int(keepalive_str),
            "errorlog": self.GUNICORN_ERROR_LOG if self.GUNICORN_ERROR_LOG else errorlog,
            "accesslog": self.GUNICORN_ACCESS_LOG if self.GUNICORN_ACCESS_LOG else accesslog,
            'worker_tmp_dir': _worker_tmp_dir,
            'limit_request_line': 0,

            # Additional, non-gunicorn variables
            "workers_per_core": workers_per_core,
            "use_max_workers": use_max_workers,
            "host": host,
            "port": port,
        }

        print(json.dumps(gconfig))
        print('Gunicorn Started with bind ', bind)

        return gconfig






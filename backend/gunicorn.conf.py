"""
    Subscriby backend `Gunicorn` process manager configuration
    https://docs.gunicorn.org/en/latest/settings.html
    
    
    If you are looking for increasing high-load capabilityof your application,
    look into that fields:
    - backlog
    - max_requests
    - max_requests_jitter
    - keepalive
"""
from multiprocessing import cpu_count
from typing import Literal

from pydantic_settings import BaseSettings


class GunicornSettings(BaseSettings):
    """
    Settings DTO from environment.
    """

    proc_bind_host: str = "0.0.0.0"
    proc_bind_port: int = 80
    proc_log_access: str = "-"
    proc_log_error: str = "-"
    proc_os_name: str = "subscriby-backend-api"
    proc_log_level: Literal["debug", "info", "warning", "error", "critical"] = "warning"
    proc_log_format: str = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
    proc_perf_workers: int = 0


def _calculate_workers_count() -> int:
    """
    Get total workers count
    """
    if settings.proc_perf_workers <= 0:
        return 2 * cpu_count() + 1
    return settings.proc_perf_workers


settings = GunicornSettings()

forwarded_allow_ips = "*"
proxy_allow_ips = "*"
worker_class = "uvicorn.workers.UvicornWorker"
workers = _calculate_workers_count()
accesslog = settings.proc_log_access
errorlog = settings.proc_log_error
loglevel = settings.proc_log_level
access_log_format = settings.proc_log_format
proc_name = settings.proc_os_name
bind = f"{settings.proc_bind_host}:{settings.proc_bind_port}"

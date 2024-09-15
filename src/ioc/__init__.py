from dishka import make_async_container

from .repo_provider import RepoProvider
from .service_provider import ServiceProvider


container = make_async_container(RepoProvider(), ServiceProvider())

__all__ = ('container', )

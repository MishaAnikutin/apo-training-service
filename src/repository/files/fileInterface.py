from abc import ABC, abstractmethod
from typing import Any


class FileInterface(ABC):
    @abstractmethod
    async def save(self, data: Any):
        ...

    @abstractmethod
    async def read(self, file_url: str):
        ...

    @abstractmethod
    async def update(self, file_url: str, new_data: Any):
        ...

    @abstractmethod
    async def delete(self, file_url: str):
        ...


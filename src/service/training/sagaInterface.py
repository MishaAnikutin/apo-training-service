from abc import ABC, abstractmethod


class SAGAInterface(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        ...

    @abstractmethod
    async def compensation(self, *args, **kwargs):
        ...

from abc import ABC, abstractmethod

from src.domain.entities import File, Query, Product


class FileParser(ABC):

    @abstractmethod
    def execute(self, file: File) -> list[Query]:
        raise NotImplementedError


class WebParser(ABC):
    url: str

    @abstractmethod
    async def execute(self) -> list[Product]:
        raise NotImplementedError
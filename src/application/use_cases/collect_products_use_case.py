from typing import List

from src.application.use_cases.base import UseCase
from src.domain.entities import Product
from src.domain.interfaces import WebParser
from src.infrastructure.logger.interfaces import ILogger


class CollectProductsUseCase(UseCase[None, List[Product]]):

    def __init__(self, web_parser: WebParser, logger: ILogger):
        self.web_parser = web_parser
        self.logger = logger

    async def __call__(self) -> List[Product]:
        try:
            self.logger.info(f'Запущен парсинг на странице {self.web_parser.url}')
            products = await self.web_parser.execute()
            self.logger.info(f'Найдено {len(products)} на странице {self.web_parser.url}')
            return products
        except Exception as ex:
            self.logger.error(f'Ошибка при сборе товаров со страницы {self.web_parser.url}',
                              exc_info=True)
            raise ex

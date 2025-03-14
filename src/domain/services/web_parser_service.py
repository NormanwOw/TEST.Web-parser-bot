from lxml import html
from aiohttp import ClientSession

from src.domain.entities import Product
from src.domain.interfaces import WebParser
from src.infrastructure.logger.interfaces import ILogger


class BSWebParser(WebParser):

    def __init__(self, url: str, xpath: str, next_page_xpath: str, logger: ILogger):
        self.url = url
        self.xpath = xpath
        self.next_page_xpath = next_page_xpath
        self.logger = logger

    async def execute(self) -> list[Product]:
        scraped_data = []
        try:
            async with ClientSession() as session:
                while self.url:
                    async with session.get(self.url) as response:
                        content = await response.text()
                        items, self.url = await self.parse(content)
                        scraped_data.extend(items)

            return self.get_products(scraped_data)
        except Exception as ex:
            self.logger.error(f'Ошибка при парсинге страницы {self.url}\n'
                              f'XPath: {self.xpath}\n'
                              f'Next Page XPath: {self.next_page_xpath}', exc_info=True)
            raise ex

    async def parse(self, content: str):
        tree = html.fromstring(content)
        elements = tree.xpath(self.xpath)
        items = [element.text for element in elements]

        if not self.next_page_xpath:
            return items, None

        next_page = tree.xpath(self.next_page_xpath)
        if not next_page:
            return items, None

        next_page_url = self.url[:self.url.rfind('/') + 1] + next_page[0].attrib['href']
        return items, next_page_url

    def get_products(self, scraped_data: list[str]) -> list[Product]:
        currency_symbols = ['$', '€', '£', '¥', '₣', '₹', '₽', '₴', '₣', '₿', '₡', '₪', '₣']
        products = []
        for data in scraped_data:
            product = Product(price=data)
            for symbol in currency_symbols:
                if symbol in data:
                    product.currency = symbol
            products.append(product)
        return products


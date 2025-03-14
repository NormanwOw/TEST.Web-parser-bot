import re
from typing import Optional

from aiogram import Bot
from pydantic import BaseModel, field_validator, model_validator

from src.application.exceptions import FileNameException


class Query(BaseModel):
    title: str
    url: str
    xpath: str
    next_page_xpath: str

    def as_message(self) -> str:
        msg = (f'<b>Название</b>: {self.title}\n'
               f'<b>Ссылка</b>: {self.url}\n'
               f'<b>XPath</b>: {self.xpath}\n')
        if self.next_page_xpath:
            msg += f'<b>XPath пагинации</b>: {self.next_page_xpath}\n'

        return msg

    @staticmethod
    async def send_message_with_queries(queries: list['Query'], bot: Bot, telegram_id: int):
        msg = '📑 <b>Данные из файла:</b>\n\n'
        for query in queries:
            msg += query.as_message() + '\n'
        await bot.send_message(telegram_id, msg)

    @staticmethod
    async def send_message_with_start_parser(queries: list['Query'], bot: Bot, telegram_id: int):
        msg = '▶️ <b>Запущен парсер сайтов:</b>\n\n'
        for query in queries:
            msg += f'{query.url}\n'
        await bot.send_message(telegram_id, msg)


class File(BaseModel):
    id: str
    name: str
    user_id: int
    path: Optional[str] = None

    @field_validator('name')
    @classmethod
    def check_name(cls, name: str) -> str:
        if not name.endswith('.xlsx'):
            raise FileNameException
        return name

    @model_validator(mode='after')
    def set_path(self):
        self.path = f'user_files/{self.user_id}.xlsx'
        return self

    async def download(self, bot: Bot):
        tg_file = await bot.get_file(file_id=self.id)
        await bot.download_file(
            file_path=tg_file.file_path,
            destination=self.path
        )


class Product(BaseModel):
    price: float | str
    currency: str = ''

    @field_validator('price')
    @classmethod
    def clean_price(cls, price: str) -> float:
        price = price.replace(',', '.')
        return float(re.sub(r'[^0-9.]', '', price).strip())

    @staticmethod
    def get_avg_price(products: list['Product']) -> float:
        if not products:
            return 0.0
        total_price = sum(product.price for product in products)
        return round(total_price / len(products), 2)


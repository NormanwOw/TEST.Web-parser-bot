import pandas as pd
from pandas import DataFrame

from src.application.exceptions import FileStructureException
from src.domain.entities import File, Query
from src.domain.interfaces import FileParser
from src.infrastructure.logger.interfaces import ILogger


class PandasFileParser(FileParser):

    def __init__(self, logger: ILogger):
        self.logger = logger

    def execute(self, file: File) -> list[Query]:
        try:
            df = pd.read_excel(file.path)
            self.check_cols(df)
            queries = self.collect_queries(df)
            return queries
        except FileStructureException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при парсинге файла {file.name} '
                              f'у пользователя {file.user_id}', exc_info=True)
            raise ex

    def check_cols(self, df: DataFrame):
        headers = df.columns.tolist()
        for header in ['title', 'url', 'xpath', 'next_page_xpath']:
            if header not in headers:
                raise FileStructureException

    def collect_queries(self, df: DataFrame) -> list[Query]:
        df = df.fillna('')
        return [
            Query(
                title=query.title,
                url=query.url,
                xpath=query.xpath,
                next_page_xpath=query.next_page_xpath,
            )
            for query in df.itertuples(index=False)
        ]
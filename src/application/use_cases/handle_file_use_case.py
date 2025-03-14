from typing import List

from aiogram import Bot

from src.application.bot.messages import INCORRECT_FILE_STRUCTURE
from src.application.exceptions import FileStructureException
from src.application.use_cases.base import UseCase
from src.domain.entities import File, Query
from src.domain.interfaces import FileParser
from src.infrastructure.logger.interfaces import ILogger
from src.infrastructure.models import UserModel, QueryModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class HandleFileUseCase(UseCase[File, List[Query]]):

    def __init__(self, bot: Bot, file_parser: FileParser, uow: IUnitOfWork, logger: ILogger):
        self.bot = bot
        self.file_parser = file_parser
        self.uow = uow
        self.logger = logger

    async def __call__(self, file: File) -> list[Query]:
        try:
            await file.download(self.bot)
            queries = self.file_parser.execute(file)
            async with self.uow:
                user = await self.uow.users.find_one(UserModel.telegram_id, file.user_id)
                if not user:
                    user = UserModel(telegram_id=file.user_id)

                for query in queries:
                    user.queries.append(QueryModel.from_domain(query, file.user_id))

                await self.uow.users.add(user)
                await self.uow.commit()

            return queries
        except FileStructureException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при обработке файла {file.name} '
                              f'у пользователя {file.user_id}', exc_info=True)
            raise ex
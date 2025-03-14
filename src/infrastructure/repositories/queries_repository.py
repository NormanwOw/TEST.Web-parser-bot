from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import QueryModel
from src.infrastructure.repositories.base import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IQueriesRepository


class QueriesRepository(SQLAlchemyRepository, IQueriesRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, QueryModel)
import uuid
from datetime import datetime
from typing import List

from openpyxl.styles.builtins import title
from sqlalchemy import UUID, BIGINT, Column, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from src.domain.entities import Query


class Base(DeclarativeBase):
    id: Mapped[uuid] = mapped_column(
        UUID, nullable=False, primary_key=True, unique=True, default=uuid.uuid4
    )


class UserModel(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    queries: Mapped[List['QueryModel']] = relationship(
        'QueryModel',
        back_populates='user',
        cascade='all, delete-orphan',
        uselist=True,
        lazy='joined'
    )


class QueryModel(Base):
    __tablename__ = 'queries'

    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    xpath: Mapped[str] = mapped_column(nullable=False)
    next_page_xpath: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id'), nullable=False, index=True
    )
    user = relationship(
        'UserModel',
        back_populates='queries',
        primaryjoin='UserModel.telegram_id == QueryModel.telegram_id',
        uselist=False,
        lazy='selectin'
    )

    @staticmethod
    def from_domain(query: Query, telegram_id: int) -> 'QueryModel':
        return QueryModel(
            title=query.title,
            url=query.url,
            xpath=query.xpath,
            next_page_xpath=query.next_page_xpath,
            telegram_id=telegram_id
        )

    def to_domain(self) -> Query:
        return Query(
            title=self.title,
            url=self.url,
            xpath=self.xpath,
            next_page_xpath=self.next_page_xpath
        )

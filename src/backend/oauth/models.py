from typing import Annotated, Any
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from datetime import datetime

Base: DeclarativeMeta = declarative_base()

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

class UserOrm(Base):
    __tablename__ = "User"

    id: Mapped[int_pk]
    login: Mapped[str_uniq]
    avatar_url: Mapped[str] = mapped_column(String)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


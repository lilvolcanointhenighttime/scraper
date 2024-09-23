from typing import Annotated, Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON

from datetime import datetime
from sqlalchemy import func, String

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Model(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }

class UserOrm(Model):
    __tablename__ = "User"

    id: Mapped[int_pk]
    login: Mapped[str_uniq]
    avatar_url: Mapped[str] = mapped_column(String)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

class HHVacancyOrm(Model):
    __tablename__ = "HHVacancy"
    
    id: Mapped[int] = mapped_column(primary_key=True) 
    link: Mapped[str]
    text: Mapped[str]
    area: Mapped[int]
    salary: Mapped[dict[str, Any]]

class HHResumeOrm(Model):
    __tablename__ = "HHResume"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str]
    text: Mapped[str]
    area: Mapped[int]
    age: Mapped[int]
    salary: Mapped[int]
    experience: Mapped[float]


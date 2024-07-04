from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON


class Model(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }

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


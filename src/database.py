from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON

engine = create_async_engine(
    "postgresql+asyncpg://postgres:123@localhost:5432/"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

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


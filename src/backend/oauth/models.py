from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON

class Model(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }

class UserORM(Model):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
from .config.database import new_session
from .schemas import UserSchema
from .models import UserOrm
from sqlalchemy import select

class UserRepository():
    @classmethod
    async def add(cls, data: UserSchema) -> None:
        async with new_session() as session:
            user_orm = UserOrm(**data)
            session.add(user_orm)
            await session.flush()
            await session.commit()

    @classmethod
    async def return_all(cls):
        async with new_session() as session:
            querry = select(UserOrm)
            result = await session.execute(querry)

            users = result.scalars().all()
            return users
        
    @classmethod
    async def filter(cls, params: dict):
        async with new_session() as session:
            querry = select(UserOrm)
            for key, value in params.items():
                if value:
                    querry = querry.filter(getattr(UserOrm, key) == value)
                    result = await session.execute(querry)
                else:
                    pass
            users = result.scalars().all()
            return users

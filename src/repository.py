from .database import new_session
from .schemas import HHVacanciesResponseSchema, HHResumesResponseSchema
from .database import HHVacancyOrm, HHResumesOrm
from sqlalchemy import select

class HHVacancyRepository():
    @classmethod
    async def add_one(cls, data: HHVacanciesResponseSchema) -> None:
        async with new_session() as session:
            for vacancy in data["items"]:
                new_vacancy = {}
                # new_vacancy["id"] = None
                new_vacancy["link"] = vacancy["url"]
                new_vacancy["title"] = vacancy["name"]
                new_vacancy["area"] = vacancy["area"]
                new_vacancy["salary"] = vacancy["salary"]

                vacancy_orm = HHVacancyOrm(**new_vacancy)
                session.add(vacancy_orm)
                await session.flush()
                await session.commit()

    @classmethod
    async def return_all(cls):
        async with new_session() as session:
            querry = select(HHVacancyOrm)
            result = await session.execute(querry)

            vacancies = result.scalars().all()
            return vacancies
        
class HHResumesRepository():
    @classmethod
    async def add_one(cls, data:HHResumesResponseSchema) -> None:
        async with new_session() as session:
            resumes_list = data["items"]
            for resume in resumes_list:
                resumes_orm = HHResumesOrm(**resume)
                session.add(resumes_orm)
            await session.flush()
            await session.commit()

    @classmethod
    async def return_all(cls):
        async with new_session() as session:
            querry = select(HHResumesOrm)
            result = await session.execute(querry)

            vacancies = result.scalars().all()
            return vacancies

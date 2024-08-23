from .config.database import new_session
from .schemas import HHVacanciesResponseSchema, HHResumesResponseSchema
from .models import HHVacancyOrm, HHResumeOrm
from sqlalchemy import select

class HHVacancyRepository():
    @classmethod
    async def add(cls, data: HHVacanciesResponseSchema) -> None:
        async with new_session() as session:
            for vacancy in data["items"]:
                new_vacancy = {}
                new_vacancy["link"] = vacancy["alternate_url"]
                new_vacancy["text"] = vacancy["name"]
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
        
    @classmethod
    async def filter(cls, params: dict):
        async with new_session() as session:
            querry = select(HHVacancyOrm)
            for key, value in params.items():
                if value:
                    querry = querry.filter(getattr(HHVacancyOrm, key) == value)
                    result = await session.execute(querry)
                else:
                    pass
            vacancies = result.scalars().all()
            return vacancies
        
class HHResumesRepository():
    @classmethod
    async def add(cls, data:HHResumesResponseSchema) -> None:
        async with new_session() as session:
            resumes_list = data["items"]
            for resume in resumes_list:
                resumes_orm = HHResumeOrm(**resume)
                session.add(resumes_orm)
            await session.flush()
            await session.commit()

    @classmethod
    async def return_all(cls):
        async with new_session() as session:
            querry = select(HHResumeOrm)
            result = await session.execute(querry)
            resumes = result.scalars().all()
            return resumes
        
    @classmethod
    async def filter(cls, params: dict):
        async with new_session() as session:
            querry = select(HHResumeOrm)
            for key, value in params.items():
                if value:
                    querry = querry.filter(getattr(HHResumeOrm, key) == value)
                    result = await session.execute(querry)
                else:
                    pass
            resumes = result.scalars().all()
            return resumes

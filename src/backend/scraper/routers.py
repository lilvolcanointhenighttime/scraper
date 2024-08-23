from fastapi import APIRouter, Header, Query
from .utils import *
from .schemas import *
from .repository import HHVacancyRepository, HHResumesRepository
from typing import Annotated


hh_router = APIRouter(
    prefix="/hh",
    tags=["HeadHunder"]
)


@hh_router.get("/vacancies")
async def get_vacancies(text: str | None = None, area: int | None = None):
    query_params = {'text': text, 'area': area}
    if text or area:
        return await HHVacancyRepository.filter(params=query_params)
    return await HHVacancyRepository.return_all()

@hh_router.post("/vacancies", response_model=HHVacanciesResponseSchema)
async def post_vacancies(model: HHVacanciesQuerySchema,
                         user_agent: Annotated[str | None, Header()] = None) -> dict:
    from .app import aiohttp_clientsession

    headers = {
        "User-Agent": user_agent
    }
    hh_vacancies_url = 'https://api.hh.ru/vacancies?cluster=true'

    data = await async_query(session = aiohttp_clientsession, headers=headers, url=hh_vacancies_url, model=model, json_encode="no", validate_area = True)
    await HHVacancyRepository.add(data=data)
    return data


@hh_router.get("/resumes")
async def get_resumes(text: str | None = None, area: int | None = None):
    query_params = {'text': text, 'area': area}
    if text or area:
        return await HHResumesRepository.filter(params=query_params)
    return await HHResumesRepository.return_all()

@hh_router.post("/resumes", response_model=HHResumesResponseSchema)
async def post_resumes(model: HHResumesQuerySchema,
                     user_agent: Annotated[str | None, Header()] = None) -> dict:
    from .app import aiohttp_clientsession

    headers = {
        "User-Agent": user_agent
    }

    data = await async_query(session = aiohttp_clientsession, headers=headers, url=hh_resume_url, model=model, json_encode="jsonable_encoder", add_area=True)
    response = await get_amount_and_items(data=data)
    await HHResumesRepository.add(response)
    return response
import json

from fastapi import APIRouter, Request, Header, Depends
from typing import Annotated

from .models import UserOrm
from .utils import *
from .schemas import *
from .repository import HHVacancyRepository, HHResumesRepository
from .producer import get_connection, produce_message



hh_router = APIRouter(
    prefix="/hh",
    tags=["HeadHunder"]
)

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@user_router.get("/get-me")
async def get_me(user_data: UserOrm = Depends(get_current_user)):
    return user_data

@user_router.post("/me")
async def get_me(request: Request):
    token = request.cookies.get('users_access_token')
    
    with get_connection() as connection:
        with connection.channel() as channel:
            body = json.dumps(token)
            produce_message(channel=channel, method="user_info", body=body)


@hh_router.get("/vacancies")
async def get_vacancies(user_data: UserOrm = Depends(get_current_user), 
                        text: str | None = None, 
                        area: int | None = None):
    query_params = {'text': text, 'area': area}
    if text or area:
        return await HHVacancyRepository.filter(params=query_params)
    return await HHVacancyRepository.return_all()

@hh_router.post("/vacancies", response_model=HHVacanciesResponseSchema)
async def post_vacancies(model: HHVacanciesQuerySchema,
                         user_agent: Annotated[str | None, Header()] = None,
                         user_data: UserOrm = Depends(get_current_user)) -> dict:
    from .app import aiohttp_clientsession

    headers = {
        "User-Agent": user_agent
    }
    hh_vacancies_url = 'https://api.hh.ru/vacancies?cluster=true'

    data = await async_query(session = aiohttp_clientsession, headers=headers, url=hh_vacancies_url, model=model, json_encode="no", validate_area = True)
    await HHVacancyRepository.add(data=data)
    return data


@hh_router.get("/resumes")
async def get_resumes(user_data: UserOrm = Depends(get_current_user),
                      text: str | None = None, 
                      area: int | None = None):
    query_params = {'text': text, 'area': area}
    if text or area:
        return await HHResumesRepository.filter(params=query_params)
    return await HHResumesRepository.return_all()

@hh_router.post("/resumes", response_model=HHResumesResponseSchema)
async def post_resumes(model: HHResumesQuerySchema,
                       user_data: UserOrm = Depends(get_current_user),
                       user_agent: Annotated[str | None, Header()] = None) -> dict:
    from .app import aiohttp_clientsession

    headers = {
        "User-Agent": user_agent
    }

    data = await async_query(session = aiohttp_clientsession, headers=headers, url=hh_resume_url, model=model, json_encode="jsonable_encoder", add_area=True)
    response = await get_amount_and_items(data=data)
    await HHResumesRepository.add(response)
    return response
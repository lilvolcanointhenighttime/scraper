import asyncio
import copy
from typing import Annotated, List
import aiohttp
from fastapi import FastAPI, Header
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager


aiohttp_session = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global aiohttp_session
    aiohttp_session = aiohttp.ClientSession()
    yield
    aiohttp_session.close()

app = FastAPI(title="Scraping", lifespan=lifespan)

class HHVacanciesQueryParamsModel(BaseModel):
    text: str = Field("", description="Переданное значение ищется во всех полях вакансии")
    area: int = Field(113, description="Регион. Необходимо передавать id из справочника /areas. Можно указать несколько значений https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas")
    only_with_salaru: bool = Field(False, description="Показывать вакансии только с указанием зарплаты")
    per_page: int = Field(10, description="Количество элементов на странице")
    page: int = Field(0, description="Текущая страница")

class HHVacanciesResponseModel(BaseModel):
    items: List[dict] = Field(..., description="Список с вакинсиями")
    found: int = Field(int, description="Количество найденных вакансий")
    pages: int = Field(int, description="Количество страниц")
    page: int = Field(int, description="Текущая страница")
    per_page: int = Field(int, description="Количество отображаемых вакансий на странице")
    clusters: List[dict] = Field(..., description="Словарь с информацией")
    arguments: None = Field(None)
    fixes: None = Field(None)
    suggests: None = Field(None)
    alternate_url: str = Field(str, description="Ссылка для альтернативно одаренных")

class HHResumesQueryParamsModel(BaseModel):
    text: str = Field("", description="Переданное значение ищется во всех полях резюме")

class HHResumesResponseModel(BaseModel):
    items: List[dict] = Field(..., description="Список с резюме")
    found: int = Field(..., description="Количество найденных резюме")



hh_vacancies_url = 'https://api.hh.ru/vacancies?clusters=true'
hh_resume_url = "https://hh.ru/search/resume?&pos=full_text&logic=normal&exp_period=all_time&"

async def async_query(session: aiohttp.ClientSession, headers: dict, url: str, query_params: dict, model: BaseModel):
    
    query_url = copy.deepcopy(url)

    query_params = model.__dict__
    for key, value in query_params.items():
        query_url += f"&{str(key)}={str(value)}"
    
    return await async_request(session, headers, query_url)

async def async_request(session: aiohttp.ClientSession, headers: dict, url: str):
    async with session.get(headers=headers, url=url) as response:
        return await response.json()

@app.post("/api/hh/vacancies", response_model=HHVacanciesResponseModel)
async def get_vacancies(model: HHVacanciesQueryParamsModel,
                        user_agent: Annotated[str | None, Header()] = None):
    headers = {
        "User-Agent": user_agent
    }

    global hh_vacancies_url
    query_url = copy.deepcopy(hh_vacancies_url)

    query_params = model.__dict__
    for key, value in query_params.items():
        query_url += f"&{str(key)}={str(value)}"

    global aiohttp_session
    data = await async_request(aiohttp_session, headers=headers, url=query_url)
    return data

@app.post("/api/hh/resume", response_model=HHResumesResponseModel)
async def get_resume(model: HHResumesQueryParamsModel,
                     user_agent: Annotated[str | None, Header()] = None):
    headers = {
        "User-Agent": user_agent
    }


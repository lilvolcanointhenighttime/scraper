import asyncio
from typing import Annotated, List
import aiohttp
from fastapi import FastAPI, Header
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from .hhresume import *


aiohttp_session = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global aiohttp_session
    aiohttp_session = aiohttp.ClientSession()
    yield
    await aiohttp_session.close()

app = FastAPI(title="Scraping", lifespan=lifespan)

# Schemas
class HHVacanciesQueryParamsSchema(BaseModel):
    text: str = Field("", description="Переданное значение ищется во всех полях вакансии")
    area: int = Field(113, description="Регион. Необходимо передавать id из справочника /areas. Можно указать несколько значений https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas")
    only_with_salaru: bool = Field(False, description="Показывать вакансии только с указанием зарплаты")
    per_page: int = Field(10, description="Количество элементов на странице")
    page: int = Field(0, description="Текущая страница")

class HHVacanciesResponseSchema(BaseModel):
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

class HHResumesQueryParamsSchema(BaseModel):
    text: str = Field("", description="Переданное значение ищется во всех полях резюме")
    currency: str = Field("", description="Код валюты. Возможные значения перечислены в поле currency.code в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries")
    salary_from: int = Field(..., description="Нижняя граница желаемой заработной платы (ЗП). По умолчанию в выдачу добавляются также резюме с неуказанной ЗП. Для выдачи резюме только с указанной ЗП передайте параметр label=only_with_salary")
    salary_to: int = Field(..., description="Верхняя граница желаемой заработной платы (ЗП). По умолчанию в выдачу добавляются также резюме с неуказанной ЗП. Для выдачи резюме только с указанной ЗП передайте параметр label=only_with_salary")
    area: int = Field(113, description="Регион. Необходимо передавать id из справочника /areas. Можно указать несколько значений https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas")
    label: str = Field("", description="Дополнительный фильтр. Возможные значения перечислены в поле resume_search_label в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. Можно указать несколько значений")
    age_from: int = Field(..., description="Нижняя граница возраста соискателя в годах. По умолчанию в выдачу добавляются также резюме с неуказанным возрастом. Для выдачи резюме только с указанным возрастом передайте значение only_with_age в параметре label")
    age_to: int = Field(..., description="Верхняя граница возраста соискателя в годах. По умолчанию в выдачу добавляются также резюме с неуказанным возрастом. Для выдачи резюме только с указанным возрастом передайте значение only_with_age в параметре label")
    relocation: str = Field("", description="Готовность к переезду. Возможные значения указаны в поле resume_search_relocation в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. Необходимо указывать вместе с параметром area")
    period: int = Field(..., description="Поиск ведется по резюме, опубликованным за указанный период в днях. Если период не указан, поиск ведется без ограничений по дате публикации")
    education_level: str = Field("", description="Уровень образования. Возможные значения перечислены в поле education_level в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. Если параметр не указан, поиск ведется без ограничений на уровень образования")
    employment: str = Field("", description="Тип занятости. Возможные значения перечислены в поле employment в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. Можно указать несколько значений")
    skill: str = Field("", description="Ключевые навыки. Указывается один или несколько идентификаторов ключевых навыков. Значения можно получить из поля id в https://api.hh.ru/openapi/redoc#tag/Podskazki/operation/get-skill-set-suggests")
    gender: str = Field("", description="Пол соискателя. Возможные значения перечислены в поле gender в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. По умолчанию вне зависимости от значения параметра будут найдены резюме, в которых пол не указан, исключить из поисковой выдачи такие резюме можно с помощью параметра label=only_with_gender")
    language: str = Field("", description="Знание языка. Можно указать несколько значений. Возможные значения перечислены в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-languages")
    schedule: str = Field("", description="График работы. Возможные значения перечислены в поле schedule в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. Можно указать несколько значений")
    order_by: str = Field("", description="Сортировка списка резюме. Возможные значения перечислены в поле resume_search_order в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries")
    citizenship: str = Field("", description="Страна гражданства соискателя. Возможные значения перечислены в https://github.com/hhru/api/blob/master/docs/areas.md#countries. Можно указать несколько значений")
    work_ticket: str = Field("", description="Страна, в которой у соискателя есть разрешение на работу. Возможные значения перечислены в https://github.com/hhru/api/blob/master/docs/areas.md#countries. Можно указать несколько значений")
    page: int = Field(int, description="Текущая страница")
    per_page: int = Field(int, description="Количество отображаемых вакансий на странице")

class HHResumesResponseSchema(BaseModel):
    items: List[dict] = Field(..., description="Список с резюме")
    found: str = Field(..., description="Количество найденных резюме у соискателей")


# urls
hh_vacancies_url = 'https://api.hh.ru/vacancies?clusters=true'
hh_resume_url = "https://hh.ru/search/resume?&pos=full_text&logic=normal&exp_period=all_time"


# routes
@app.post("/api/hh/vacancies")
async def get_vacancies(model: HHVacanciesQueryParamsSchema,
                        user_agent: Annotated[str | None, Header()] = None) -> dict:
    headers = {
        "User-Agent": user_agent
    }

    global hh_vacancies_url
    global aiohttp_session
    try:
        data = await async_query(session = aiohttp_session, headers=headers, url=hh_vacancies_url, model=model, json_encode="no")
        return data
    except:
        print("Hello")

@app.post("/api/hh/resumes", response_model=HHResumesResponseSchema)
async def get_resume(model: HHResumesQueryParamsSchema,
                     user_agent: Annotated[str | None, Header()] = None) -> dict:
    headers = {
        "User-Agent": user_agent
    }

    global hh_resume_url
    global aiohttp_session
    data = await async_query(session = aiohttp_session, headers=headers, url=hh_resume_url, model=model, json_encode="jsonable_encoder")
    response = await get_amount_and_items(data=data)
    return response




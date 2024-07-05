from typing import List, Optional
from pydantic import BaseModel, Field


class HHVacanciesQuerySchema(BaseModel):
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
    clusters: None = Field(None, description="Словарь с информацией")
    arguments: None = Field(None)
    fixes: None = Field(None)
    suggests: None = Field(None)
    alternate_url: str = Field(str, description="Ссылка для альтернативно одаренных")

class HHResumesQuerySchema(BaseModel):
    text: str = Field("", description="Переданное значение ищется во всех полях резюме")
    currency: str = Field("", description="Код валюты. Возможные значения перечислены в поле currency.code в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries")
    salary_from: int = Field(..., description="Нижняя граница желаемой заработной платы (ЗП). По умолчанию в выдачу добавляются также резюме с неуказанной ЗП. Для выдачи резюме только с указанной ЗП передайте параметр label=only_with_salary")
    salary_to: int = Field(..., description="Верхняя граница желаемой заработной платы (ЗП). По умолчанию в выдачу добавляются также резюме с неуказанной ЗП. Для выдачи резюме только с указанной ЗП передайте параметр label=only_with_salary")
    area: int = Field(113, description="Регион. Необходимо передавать id из справочника /areas. Можно указать несколько значений https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-areas")
    label: str = Field("", description="Дополнительный фильтр. Возможные значения перечислены в поле resume_search_label в https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-dictionaries. Можно указать несколько значений")
    age_from: int = Field(..., description="Нижняя граница возраста соискателя в годах. По умолчанию в выдачу добавляются также резюме с неуказанным возрастом. Для выдачи резюме только с указанным возрастом передайте значение only_with_age в параметре label")
    age_to: int = Field(..., description="Верхняя граница возраста соискателя в годах. По умолчанию в выдачу добавляются также резюме с неуказанным возрастом. Для выдачи резюме только с указанным возрастом передайте значение only_with_age в параметре label")
    page: int = Field(int, description="Текущая страница")
    per_page: int = Field(int, description="Количество отображаемых вакансий на странице")

class HHResumesResponseSchema(BaseModel):
    items: List[dict] = Field(..., description="Список с резюме")
    found: Optional[str] = None

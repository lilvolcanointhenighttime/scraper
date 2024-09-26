import aiohttp
import functools
import asyncio

from bs4 import BeautifulSoup
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, Request, status

from .repository import UserRepository
from .config.env import USE_K8S, DOMAIN_NGINX


# urls
hh_vacancies_url = 'https://api.hh.ru/vacancies?clusters=true'
hh_resume_url = "https://hh.ru/search/resume?&pos=full_text&logic=normal&exp_period=all_time"

def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper

async def async_query_post(session: aiohttp.ClientSession, url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with session.post(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data
    
async def get_current_user(request: Request):
    from .app import aiohttp_clientsession
    token = request.cookies.get('users_access_token')
    params = {"token": token}
    if USE_K8S:
        user_data = await async_query_post(session=aiohttp_clientsession, url=f"http://fastapi-oauth:8800/api/oauth/cookie/rmq-me", params=params)
    else:
        user_data = await async_query_post(session=aiohttp_clientsession, url=f"http://{DOMAIN_NGINX}/api/oauth/cookie/rmq-me", params=params)
    if user_data == {'detail': 'Token not found'} or user_data == {'detail': 'Not Found'} or user_data == {'detail': 'User not found'}:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')
    
    user_data = user_data[0]
    user = await UserRepository.filter(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user

async def async_query(session: aiohttp.ClientSession, headers: dict, url: str, model: BaseModel, json_encode: str = "no", add_area: bool = False, validate_area: bool = False) -> dict:
    query_params: dict = model.__dict__

    for key, value in query_params.items():
        if key == "area":
            area = value
        url += f"&{str(key)}={str(value)}"

    async with session.get(headers=headers, url=url) as response:
        if json_encode == "no":
            data = await response.json()
        
        if json_encode == "jsonable_encoder":
            data = jsonable_encoder(await response.text())
        
        if add_area:
            data += f"area={area}"

        if validate_area:
            for item in data["items"]:
                if item["area"]["id"].isdigit():
                    item["area"] = int(item["area"]["id"])
                else:
                    item["area"] = item["area"]["id"]
        return data
            

def is_float_or_digit(string: str) -> str | None:
    if string.isdigit():
        return "int"
    try:
        float(string)
        return "float"
    except ValueError:
        return
    
def validate_dict(params_dict: dict) -> dict:
    for key, value in params_dict.items():
        if is_float_or_digit(value) == "int":
            params_dict[key] = int(value)
        if is_float_or_digit(value) == "float":
            params_dict[key] = float(value)
    return params_dict


# def get_params(query_params: str) -> dict:
#     query_params = query_params.split("?")[1]
#     if "&" in query_params:
#         params = [param.split("=") for param in query_params.split("&")]
#         params_list = [tuple(param) for param in params]
#         params_dict = dict(params_list)
#     else:
#         params = query_params.split("=")
#         params_list = [tuple(params)]
#         params_dict = dict(params_list)

#     params_dict = validate_dict(params_dict=params_dict)
#     return params_dict


async def get_amount_of_resumes_and_applicants(data) -> str:
    soup = BeautifulSoup(data, "lxml")
    block_main = soup.find("div", class_="HH-MainContent HH-Supernova-MainContent")
    amount_of_resumes_and_applicants = block_main.find("h1", class_="bloko-header-section-3").text
    return amount_of_resumes_and_applicants

def convert_str_to_int(string: str) -> int:
    if not string:
        return
    convert_chars = "0123456789"
    modified_string = ""
    for char in string:
        if char in convert_chars:
            modified_string += char
    return(int(modified_string))


async def get_resumes_items(data, area: str) -> list:
    soup = BeautifulSoup(data, "lxml")
    block_main = soup.find("div", class_="HH-MainContent HH-Supernova-MainContent")
    all_resumes_resultset = block_main.find_all("div", attrs={"data-qa": "resume-serp__resume"})

    items = []
    for resume in all_resumes_resultset:
        link = resume.find_all("a",  attrs={"data-qa": "serp-item__title"})[0].get("href") if resume.find_all("a",  attrs={"data-qa": "serp-item__title"}) else ""
        text = resume.find_all("a",  attrs={"data-qa": "serp-item__title"})[0].find("span").text if resume.find_all("a",  attrs={"data-qa": "serp-item__title"}) else ""
        age = resume.find_all("span", attrs={"data-qa": "resume-serp__resume-age"})[0].find("span").text if resume.find_all("span", attrs={"data-qa": "resume-serp__resume-age"}) else 0
        age = convert_str_to_int(string=age) if age else 0
        salary = resume.find_all("div", class_="bloko-text bloko-text_strong")[0].text if resume.find_all("div", class_="bloko-text bloko-text_strong") else 0
        salary = convert_str_to_int(string=salary) if salary else 0
        experience = resume.find_all("div", attrs={"data-qa": "resume-serp__resume-excpirience-sum"})[0].text.replace("лет", '.').replace("года", '.').replace("год", '.').replace("месяцев", '').replace("месяца", '').replace("месяц", '') if resume.find_all("div", attrs={"data-qa": "resume-serp__resume-excpirience-sum"}) else 0.0
        experience = float("".join(experience.split())) if experience else 0.0
        resume_dict = {
            "link": f"https://hh.ru{link}",
            "text": text,
            "area": convert_str_to_int(area),
            "age": age,
            "salary": salary,
            "experience": experience
        }
        items.append(resume_dict)
    return items

async def get_amount_and_items(data) -> dict:
    amount_of_resumes_and_applicants: str = await get_amount_of_resumes_and_applicants(data)
    area = data.split("area=")[-1]
    items: list = await get_resumes_items(data, area=area)
    respons = {
        "items": items,
        "found": amount_of_resumes_and_applicants
    }
    return respons

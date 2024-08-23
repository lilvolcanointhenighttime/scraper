from bs4 import BeautifulSoup
import aiohttp
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

# urls
hh_vacancies_url = 'https://api.hh.ru/vacancies?clusters=true'
hh_resume_url = "https://hh.ru/search/resume?&pos=full_text&logic=normal&exp_period=all_time"


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

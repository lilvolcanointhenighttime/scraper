from bs4 import BeautifulSoup
import asyncio
import aiohttp
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


url = "https://hh.ru/search/resume?"
# https://hh.ru/search/resume?&pos=full_text&logic=normal&exp_period=all_time



async def async_query(session: aiohttp.ClientSession, headers: dict, url: str, model: BaseModel) -> dict:
    query_params: dict = model.__dict__
    for key, value in query_params.items():
        url += f"&{str(key)}={str(value)}"
    
    async with session.get(headers=headers, url=url) as response:
        data = jsonable_encoder(await response.text())
        return data
        

async def get_amount_of_resumes_and_applicants(data) -> str:
    soup = BeautifulSoup(data, "lxml")
    block_main = soup.find("div", class_="HH-MainContent HH-Supernova-MainContent")
    amount_of_resumes_and_applicants = block_main.find("h1", class_="bloko-header-section-3").text
    return amount_of_resumes_and_applicants


async def get_resumes_items(data) -> list:
    soup = BeautifulSoup(data, "lxml")
    block_main = soup.find("div", class_="HH-MainContent HH-Supernova-MainContent")
    all_resumes_resultset = block_main.find_all("div", attrs={"data-qa": "resume-serp__resume"})

    items = []
    for resume in all_resumes_resultset:
        link = resume.find_all("a",  attrs={"data-qa": "serp-item__title"})[0].get("href") if resume.find_all("a",  attrs={"data-qa": "serp-item__title"}) else ""
        title = resume.find_all("a",  attrs={"data-qa": "serp-item__title"})[0].find("span").text if resume.find_all("a",  attrs={"data-qa": "serp-item__title"}) else ""
        age = resume.find_all("span", attrs={"data-qa": "resume-serp__resume-age"})[0].find("span").text if resume.find_all("span", attrs={"data-qa": "resume-serp__resume-age"}) else ""
        salary = resume.find_all("div", class_="bloko-text bloko-text_strong")[0].text if resume.find_all("div", class_="bloko-text bloko-text_strong") else ""
        experience = resume.find_all("div", attrs={"data-qa": "resume-serp__resume-excpirience-sum"})[0].text if resume.find_all("div", attrs={"data-qa": "resume-serp__resume-excpirience-sum"}) else ""
        resume_dict = {
            "link": f"https://hh.ru{link}",
            "title": title,
            "age": age,
            "salary": salary,
            "experience": experience
        }
        items.append(resume_dict)
    return items

async def get_amount_and_items(data) -> dict:
    amount_of_resumes_and_applicants: str = await get_amount_of_resumes_and_applicants(data)
    items: list = await get_resumes_items(data)
    respons = {
        "items": items,
        "found": amount_of_resumes_and_applicants
    }
    return respons

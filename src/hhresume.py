from bs4 import BeautifulSoup
import asyncio
import aiohttp

url = "https://hh.ru/search/resume?page=0"
# https://hh.ru/search/resume?text=&pos=full_text&logic=normal&exp_period=all_time&page=



async def async_request(url: str, headers: dict = {}) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(headers=headers, url=url) as response:
            return await response.text()
        
async def get_amount_of_resumes_and_applicatns(url):
    data = await async_request(url)
    soup = BeautifulSoup(data, "lxml")
    block_main = soup.find("div", class_="HH-MainContent HH-Supernova-MainContent")
    block_amount_of_resumes_and_applicants = block_main.find("h1", class_="bloko-header-section-3")
    return block_amount_of_resumes_and_applicants


async def get_resumes():
    data = await async_request(url)
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
            "link": link,
            "title": title,
            "age": age,
            "salary": salary,
            "experience": experience
        }
        items.append(resume_dict)
    return items
    
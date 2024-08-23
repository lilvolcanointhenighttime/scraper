import aiohttp


async def async_query_post(session: aiohttp.ClientSession, headers: dict, url: str, params: dict) -> dict:
    async with session.post(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data
    
async def async_query_get(session: aiohttp.ClientSession, headers: dict, url: str, params: dict) -> dict:
    async with session.get(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data
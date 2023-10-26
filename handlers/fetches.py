from aiohttp_proxy import ProxyConnector
import aiohttp

async def fetch_with_proxy(url, proxy):
    connector = ProxyConnector.from_url(proxy)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Referer": "https://www.avito.ru/",
    }
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print("Request successful.")
                return await response.text()
            else:
                print(f"Request failed with status code {response.status}")


async def fetch_without_proxy(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Referer": "https://www.avito.ru/",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
        
            if response.status == 200:
                print("Request successful.")
                return await response.text()
            else:
                print(f"Request failed with status code {response.status}")
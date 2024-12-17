import asyncio

import httpx

from flipkart_scraper import *


async def parse_search_page_test():
    text_file_path = "../../data/tests/text/parse_search_page.txt"
    keywords = open_file("../../keywords.txt").splitlines()

    async with httpx.AsyncClient() as client:
        tasks = [
            get_page(keyword, client, search=True)
            for keyword in keywords
        ]
        results = await asyncio.gather(*tasks)

    products_urls = set()

    for result, keyword in zip(results, keywords):
        products_urls.update(list(parse_search_page(result.text)))

    save_file("\n".join(products_urls), text_file_path)


if __name__ == "__main__":
    asyncio.run(parse_search_page_test())

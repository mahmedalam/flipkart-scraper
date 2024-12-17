import asyncio
import os

import httpx

from flipkart_scraper import *


async def main():
    html_output_dir = "../data/raw"
    keywords = open_file("../keywords.txt").splitlines()

    async with httpx.AsyncClient() as client:
        tasks = [
            get_page(keyword, client, search=True)
            for keyword in keywords
        ]
        results = await asyncio.gather(*tasks)
        results_len = len(results)

    print(f"Getting HTML Done")

    for index, result in enumerate(results, 1):
        save_file(result.text, os.path.join(html_output_dir, f"{index}.html"))

    print(f"Saving HTML Done")

    urls = []
    for page_no in range(1, results_len + 1):
        products_urls = list(parse_search_page(open_file(os.path.join(html_output_dir, f"{page_no}.html"))))
        urls.extend(products_urls)

    save_file("\n".join(set(urls)), f"../data/products_urls.txt")


if __name__ == "__main__":
    asyncio.run(main())

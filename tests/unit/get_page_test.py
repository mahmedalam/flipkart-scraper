import asyncio
import os

import httpx

from flipkart_scraper import *


async def get_page_test():
    """
    Fetches and saves the HTML content of multiple product pages.

    This function uses asynchronous HTTP requests to fetch HTML content for a list of
    product URLs from Flipkart, and then saves the content to the specified output directory.

    No parameters are taken, and the function defines the URLs and output directory internally.

    The results are saved in the output directory as HTML files labeled sequentially.
    """
    output_dir = "../../data/tests/html"
    urls = [
        "https://www.flipkart.com/apple-macbook-air-m2-8-gb-512-gb-ssd-mac-os-monterey-mly43hn-a/p/itm85d8044d46450",
        "https://www.flipkart.com/dell-intel-core-i3-12th-gen-1215u-8-gb-512-gb-ssd-windows-11-home-inspiron-3520-thin-light-laptop/p/itm0cdfd7f4e9613",
        "https://www.flipkart.com/lenovo-ideapad-slim-3-intel-core-i3-13th-gen-1305u-8-gb-512-gb-ssd-windows-11-home-14iru8-thin-light-laptop/p/itmc1c0a3fcb69ae"
    ]

    async with httpx.AsyncClient() as client:
        tasks = [
            get_page(url, client)
            for url in urls
        ]
        results = await asyncio.gather(*tasks)

    for index, result in enumerate(results, 1):
        save_file(result.text, os.path.join(output_dir, f"get_page_{index}.html"))


if __name__ == "__main__":
    asyncio.run(get_page_test())

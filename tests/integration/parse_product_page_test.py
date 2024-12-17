import asyncio
import json
from dataclasses import asdict

import httpx

from flipkart_scraper import *


async def parse_product_page_test_laptop():
    html_file_path = "../../data/tests/html/parse_product_page_laptop.html"
    json_file_path = "../../data/tests/json/parse_product_page_laptop.json"
    url = "https://www.flipkart.com/apple-macbook-air-m2-8-gb-256-gb-ssd-mac-os-monterey-mlxw3hn-a/p/itmc2732c112aeb1"

    # For saving test html
    async with httpx.AsyncClient() as client:
        response = await get_page(url, client)
    save_file(response.text, html_file_path)

    product = parse_product_page(open_file(html_file_path), url, "laptop")
    save_file(json.dumps(asdict(product)), json_file_path)


async def parse_product_page_test_shoe():
    html_file_path = "../../data/tests/html/parse_product_page_shoe.html"
    json_file_path = "../../data/tests/json/parse_product_page_shoe.json"
    url = "https://www.flipkart.com/campus-crysta-pro-running-shoes-men/p/itm4c7f055fafd03"

    # For saving test html
    async with httpx.AsyncClient() as client:
        response = await get_page(url, client)
    save_file(response.text, html_file_path)

    product = parse_product_page(open_file(html_file_path), url, "shoe")
    save_file(json.dumps(asdict(product)), json_file_path)


if __name__ == "__main__":
    asyncio.run(parse_product_page_test_laptop())
    asyncio.run(parse_product_page_test_shoe())

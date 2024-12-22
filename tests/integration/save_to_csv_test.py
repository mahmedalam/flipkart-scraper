import asyncio
from dataclasses import asdict, fields

import httpx

from flipkart_scraper import *


async def test_save_to_csv():
    html_file_path = "../../data/tests/html/save_to_csv.html"
    csv_file_path = "../../data/tests/csv/save_to_csv.csv"
    url = "https://www.flipkart.com/campus-crysta-pro-running-shoes-men/p/itm4c7f055fafd03"

    # For saving test html
    async with httpx.AsyncClient() as client:
        response = await get_page(url, client)
    save_file(response.text, html_file_path)

    product = parse_product_page(open_file(html_file_path), url, "shoe")
    fieldnames = list(product.__annotations__.keys())
    fieldnames.remove("reviews")
    data = asdict(product)
    data.pop("reviews")
    save_to_csv(csv_file_path, [data], fieldnames)


if __name__ == "__main__":
    asyncio.run(test_save_to_csv())

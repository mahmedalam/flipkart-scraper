import httpx
from httpx import Response

from .utils import get_user_agent


async def get_page(url: str, client: httpx.AsyncClient, page_no: int | None = None,
                   search: bool = False) -> Response | None:
    """
    Fetches a webpage using an HTTP client.

    This function retrieves a page from either a direct URL or performs a search query 
    using Flipkart's search functionality. The request includes headers to mimic a browser request.

    Args:
        url (str): The URL of the page to fetch.
        client (httpx.AsyncClient): The HTTP client used for sending asynchronous requests.
        page_no (int | None, optional): The page number to retrieve if paginated. Defaults to None.
        search (bool, optional): Whether to perform a search query. Defaults to False.

    Returns:
        Response | None: The HTTP response object if successful, otherwise None.
    """
    search_url = f"https://www.flipkart.com/search?q="
    headers = {
        "User-Agent": get_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/raw,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.flipkart.com/",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1"  # Do Not Track header
    }

    if search:
        response = await client.get(search_url, params={"q": url}, headers=headers)
    elif page_no is None or page_no <= 1:
        response = await client.get(url, headers=headers)
    else:
        response = await client.get(url, params={"page": page_no}, headers=headers)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        print(f"Error fetching page {page_no}: {response.status_code}")
        return None

    return response

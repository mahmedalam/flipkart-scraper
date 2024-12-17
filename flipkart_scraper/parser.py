from urllib.parse import urljoin

from selectolax.parser import HTMLParser, Node

from .models import Product, Review
from .utils import clean_price, convert_to_int


def extract_text(tree: HTMLParser | Node, selector: str) -> str | None:
    try:
        node = tree.css_first(selector)
        return node.text(strip=True)
    except AttributeError:
        return None


def parse_search_page(html: str):
    tree = HTMLParser(html)
    products_urls = tree.css('a.CGtC98')

    if not products_urls:
        products_urls = tree.css('a.rPDeLR')

    for url in products_urls:
        yield urljoin("https://www.flipkart.com", url.attributes["href"]).split("?")[0]


def parse_product_page(html: str, url: str, category: str) -> Product:
    tree = HTMLParser(html)
    is_type_2 = False

    name = extract_text(tree, "h1._6EBuvT")
    currency = extract_text(tree, "div.Nx9bqj")[0]
    price = clean_price(extract_text(tree, "div.Nx9bqj"))
    original_price = clean_price(extract_text(tree, "div.yRaY8j"))
    discount = float(extract_text(tree, "div.UkUFwK").split("%")[0])
    rating = float(extract_text(tree, "div.XQDdHH"))

    try:
        image_url = tree.css_first("img.DByuf4.IZexXJ.jLEJ7H").attributes["src"]
    except AttributeError:
        image_url = tree.css_first("img._53J4C-.utBuJY").attributes["src"]
        is_type_2 = True

    if not is_type_2:
        reviews_count = int(extract_text(tree, "span.Wphh3N").split("&")[1].split(" ")[0])
    else:
        reviews_count = convert_to_int(extract_text(tree, "span.Wphh3N").split("and")[1].split(" ")[1])

    reviews_nodes = tree.css("div.col.EPCmJX")

    reviews = []

    for review in reviews_nodes:
        _rating = float(extract_text(review, "div.XQDdHH"))

        if not is_type_2:
            _title = extract_text(review, "p.z9E0IG")
            _desc = extract_text(review, "div.ZmyHeo")[:-9]
        else:
            _title = None
            _desc = extract_text(review, "div._11pzQk")

        _name = extract_text(review, "p.AwS1CA")
        _certified = extract_text(review, "p.MztJPv")
        _date = review.css("p._2NsDsF")[1].text(strip=True)
        _likes, _dislikes = review.css("span.tl9VpF")
        _likes = int(_likes.text(strip=True))
        _dislikes = int(_dislikes.text(strip=True))

        reviews.append(Review(
            title=_title,
            description=_desc,
            rating=_rating,
            name=_name,
            certified=_certified,
            date=_date,
            likes=_likes,
            dislikes=_dislikes,
        ))

    return Product(
        name=name,
        currency=currency,
        price=price,
        original_price=original_price,
        discount=discount,
        rating=rating,
        reviews_count=reviews_count,
        reviews=reviews,
        image_url=image_url,
        url=url,
        category=category.capitalize(),
    )

from flipkart_scraper import *

if __name__ == "__main__":
    db = Database("../../data/tests/flipkart.db")

    product_id = db.insert_product(
        name="Wireless Earbuds",
        currency="INR",
        price=100.0,
        original_price=200.0,
        discount=50.0,
        rating=4.5,
        reviews_count=100,
        image_url="https://example.com/image.jpg",
        url="https://example.com/product",
        category="Electronics"
    )

    db.insert_review(
        product_id=product_id,
        title="Great product",
        description="I love this product",
        rating=5.0,
        name="John Doe",
        certified="Yes",
        date="2021-01-01",
        likes=28,
        dislikes=3
    )

    db.commit()
    db.close()

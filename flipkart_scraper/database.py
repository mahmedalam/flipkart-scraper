import sqlite3

from flipkart_scraper.utils import generate_timestamp_id


class Database:
    def __init__(self, db_filename: str = "flipkart.db") -> None:
        self.conn = sqlite3.connect(db_filename)
        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                currency TEXT,
                price REAL,
                original_price REAL,
                discount REAL,
                rating REAL,
                reviews_count INTEGER,
                image_url TEXT NOT NULL,
                url TEXT NOT NULL,
                category TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Reviews (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                title TEXT,
                description TEXT,
                rating REAL,
                name TEXT,
                certified TEXT,
                date TEXT,
                likes INTEGER,
                dislikes INTEGER,
                FOREIGN KEY (product_id) REFERENCES Products(id)
            )
        """)

        self.commit()

    def insert_product(
            self,
            name: str,
            currency: str | None,
            price: float | None,
            original_price: float | None,
            discount: float | None,
            rating: float | None,
            reviews_count: int | None,
            image_url: str,
            url: str,
            category: str
    ) -> int:
        id = generate_timestamp_id()

        self.cur.execute("""
            INSERT INTO Products (
            id,
            name,
            currency,
            price,
            original_price,
            discount,
            rating,
            reviews_count,
            image_url,
            url,
            category
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            id,
            name,
            currency,
            price,
            original_price,
            discount,
            rating,
            reviews_count,
            image_url,
            url,
            category
        ))

        return id

    def insert_review(
            self,
            product_id: int,
            title: str | None,
            description: str | None,
            rating: float | None,
            name: str | None,
            certified: str | None,
            date: str | None,
            likes: int | None,
            dislikes: int | None
    ) -> int:
        id = generate_timestamp_id()

        self.cur.execute("""
            INSERT INTO Reviews (
            id,
            product_id,
            title,
            description,
            rating,
            name,
            certified,
            date,
            likes,
            dislikes
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            id,
            product_id,
            title,
            description,
            rating,
            name,
            certified,
            date,
            likes,
            dislikes
        ))

        return id

    def fetch_all_products(self) -> list:
        self.cur.execute("SELECT * FROM Products")
        return self.cur.fetchall()

    def fetch_all_reviews(self) -> list:
        self.cur.execute("SELECT * FROM Reviews")
        return self.cur.fetchall()

    def commit(self) -> None:
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

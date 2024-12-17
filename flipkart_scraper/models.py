from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Review:
    title: str
    description: str
    rating: float
    name: str
    certified: str | None
    date: str
    likes: int
    dislikes: int


@dataclass
class Product:
    name: str
    currency: str
    price: float
    original_price: float
    discount: float
    rating: float
    reviews_count: int
    reviews: list[Review]
    image_url: str
    url: str
    category: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

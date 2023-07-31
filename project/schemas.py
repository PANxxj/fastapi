from datetime import date
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str
    price: float

    class Config:
        orm_mode = True

class Rating(BaseModel):
    book_id: int
    user_name: str
    rating: int
    review: str = None

    class Config:
        orm_mode = True
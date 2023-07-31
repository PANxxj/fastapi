from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_date = Column(Date)
    isbn = Column(String, unique=True, index=True)
    price = Column(Float)

    ratings = relationship("Rating", back_populates="book")

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_name = Column(String)
    rating = Column(Integer)
    review = Column(String, nullable=True)

    book = relationship("Book", back_populates="ratings")

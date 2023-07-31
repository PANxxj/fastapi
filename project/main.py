# from project import models
import models
from database import engine
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from models import Book, Rating
from database import engine, SessionLocal
from schemas import Book
from sqlalchemy.orm import Session
from typing import List, Optional

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Book-related Endpoints
@app.post("/books/", response_model=Book)
async def create_book(book: Book ,db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int,db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book,db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int,db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

@app.get("/books/", response_model=List[Book])
async def read_books(skip: int = 0, limit: int = 10,db: Session = Depends(get_db)):
    return db.session.query(Book).offset(skip).limit(limit).all()

@app.get("/books/rated", response_model=List[Book])
async def read_books_rated(db: Session = Depends(get_db)):
    return db.query(Book).order_by(Book.rating.desc()).all()

# Rating-related Endpoints
@app.post("/ratings/", response_model=Rating)
async def create_rating(rating: Rating ,db: Session = Depends(get_db)):
    db_rating = Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.get("/ratings/{book_id}", response_model=List[Rating])
async def read_ratings_for_book(book_id: int,db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.book_id == book_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail="No ratings found for the book")
    return ratings

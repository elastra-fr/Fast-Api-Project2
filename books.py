from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Id is not needed to create a book", default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "title",
                "author": "author",
                "description": "description",
                "rating": 5
            }
        }
    }


BOOKS = [

    Book(id=1, title="title1", author="author1",
         description="description1", rating=5),
    Book(id=2, title="title2", author="author2",
         description="description2", rating=4),
    Book(id=3, title="title3", author="author3",
         description="description3", rating=5),
    Book(id=4, title="title4", author="author1",
         description="description4", rating=2),
    Book(id=5, title="title5", author="author3",
         description="description5", rating=3)



]

# Endpoint to read all books


@app.get("/books")
async def read_all_books():
    return BOOKS

# Endpoint to read a book by id - Using path parameter


@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return

# Endpoint to return books by rating - Using query parameter


@app.get("/books/")
async def read_books_by_rating(book_rating: int):
   books_to_return = []

   for book in BOOKS:
       if book.rating == book_rating:
           books_to_return.append(book)
   return books_to_return

# Endpoint to add a new book
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


# function to find the id of the book and increment it by 1 to assign it to the new book
def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1

    return book


# Endpoint to update a book by id
@app.put("/books/update_book")

async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            
    
# Endpoint to delete a book by id

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}
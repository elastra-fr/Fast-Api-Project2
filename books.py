from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Id is not needed to create a book", default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(ge=1900, le=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "title",
                "author": "author",
                "description": "description",
                "rating": 5,
                "published_date": 2024
            }
        }
    }


BOOKS = [

    Book(id=1, title="title1", author="author1",
         description="description1", rating=5, published_date=2021),
    Book(id=2, title="title2", author="author2",
         description="description2", rating=4, published_date=2022),
    Book(id=3, title="title3", author="author3",
         description="description3", rating=5, published_date=2023),
    Book(id=4, title="title4", author="author1",
         description="description4", rating=2, published_date=2024),
    Book(id=5, title="title5", author="author3",
         description="description5", rating=3, published_date=2025),



]

# Endpoint to read all books


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# Endpoint to read a book by id - Using path parameter and path validation
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# Endpoint to return books by rating - Using query parameter and query validation
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, le=5)):
   books_to_return = []

   for book in BOOKS:
       if book.rating == book_rating:
           books_to_return.append(book)
   return books_to_return


# Endpoint to return books by author - Using query parameter and query validation
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(publish_date: int = Query(gt=1900, le=2031)):
    books_to_return = []

    for book in BOOKS:
        if book.published_date == publish_date:
            books_to_return.append(book)
    return books_to_return


# Endpoint to add a new book
# status code for created
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
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
# status code for no content
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


# Endpoint to delete a book by id - Using path parameter and path validation
# status code for no content
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            return {"message": "Book deleted successfully"}

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

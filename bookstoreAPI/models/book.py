from pydantic import BaseModel
from bookstoreAPI.models.author import Author
class Book(BaseModel):
    isbn: str
    name: str
    author: Author
    year: int
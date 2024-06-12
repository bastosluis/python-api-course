from fastapi import FastAPI, Body
from models.user import User
from models.author import Author

app = FastAPI()
@app.post("/user")
async def post_user(user: User):
    return {"request body": user}

@app.get("/user")
async def get_user_validation(password: str):
    return {"query parameter": password}

@app.get("/book/{isbn}")
async def get_book_with_isbn(isbn: str):
    return {"query changeable parameter": isbn}

@app.get("/author/{id}/book")
async def get_authors_book(id: int, category: str, order: str = "asc"):
    return {"query changeable parameter": f"{order} {category} {str(id)}"}

@app.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}

@app.post("/user/author")
async def post_user_and_author(user: User, author: Author, auth_token: str = Body(..., embed=True)):
    return {"user": user, "author": author, "auth_token": auth_token}

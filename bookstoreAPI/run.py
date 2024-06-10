from fastapi import FastAPI, Body
from models.user import User
from models.author import Author

app = FastAPI()

@app.post("/user")
async def postUser(user: User):
    return {"request body": user}

@app.get("/user")
async def getUserValidation(password:str):
    return {"query parameter": password}

@app.get("/book/{isbn}")
async def getBookWithIsbn(isbn:str):
    return {"query changeable parameter": isbn}

@app.get("/author/{id}/book")
async def getAuthorsBook(id: int, category: str, order: str="asc"):
    return{"query changeable parameter": f"{order} {category} {str(id)}"}

@app.patch("/author/name")
async def patchAuthorName(name: str = Body(..., embed=True)):
    return {"name in body": name}

# gives 422 Unprocessable Entity with following:
'''
{
    "user": {
            "name": "user1",
            "password": "pass1",
            "email": "user@email.com",
            "role": "admin"
    },
    "author": {
        "name": "author1",
        "book": ["book1","book2"]
    },
    "auth_token": "123456"
}
'''
@app.post("/user/author")
async def postUserAndAuthor(user:str, author: Author, auth_token: str = Body(..., embed=True)):
    return {"user":user, "author":author, "auth_token": auth_token}
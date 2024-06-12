from fastapi import FastAPI, Body, File, Response
from bookstoreAPI.models.user import User
from bookstoreAPI.models.author import Author
from bookstoreAPI.models.book import Book
from ..utils.security import *

app_v1 = FastAPI(openapi_prefix="/v1")


@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User):
    return {"request body": user}

@app_v1.get("/user")
async def get_user_validation(password: str):
    return {"query parameter": password}

@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"])
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name":"author1",
        "book": ["book1", "book2"]
    }
    author1 = Author(**author_dict)
    book_dict = {
        "isbn": "isbn1",
        "name": "book1",
        "year": 2024,
        "author": author1
    }
    book1 = Book(**book_dict)
    return book1

@app_v1.get("/author/{id}/book")
async def get_authors_book(id: int, category: str, order: str = "asc"):
    return {"query changeable parameter": f"{order} {category} {str(id)}"}

@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}

@app_v1.post("/user/author", status_code=HTTP_201_CREATED)
async def post_user_and_author(user: User, author: Author, auth_token: str = Body(..., embed=True)):
    return {"user": user, "author": author, "auth_token": auth_token}

@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file size": len(profile_photo)}

@app_v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username" : form_data.username, 
                     "password": form_data.password,
                     "disabled": False,
                     "role": "admin"}
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    
    jwt_token = create_jwt_token(user)
    return {"token": jwt_token}
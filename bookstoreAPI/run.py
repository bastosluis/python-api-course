from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def helloWorld():
    return {"Hello World!"}
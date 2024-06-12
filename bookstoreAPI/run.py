from fastapi import FastAPI, Body, File, Response
from routes.v1 import app_v1

app = FastAPI()
app.mount("/v1", app_v1)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class Url(BaseModel):
    url: str


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home():
    return {"hello": "world"}


@app.get("/shortener", response_class=HTMLResponse)
def shortener(request: Request):
    return templates.TemplateResponse("shortener.html", {"request": request})

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import generate_short_url, SHORTENED_URL_LENGTH, BASE_URL
from database.dao import insert_data, fetch_longurl
from database.database import db


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
async def shortener(request: Request):
    form = await request.form()
    form_data = dict(form)
    longurl = form_data.get("longurl")

    shorturl = generate_short_url(SHORTENED_URL_LENGTH)

    insert_data(db, shorturl, longurl)

    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "base_url": BASE_URL,
                                       "shortened_url": shorturl}
                                      )


@app.get("/{shorturl}")
async def redirect(shorturl: str):
    longurl = fetch_longurl(db, shorturl)
    return RedirectResponse(url=longurl)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import generate_short_url, SHORTENED_URL_LENGTH, BASE_URL
from database.dao import insert_urls, fetch_longurl, fetch_all_urls, delete_url
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

    insert_urls(db, shorturl, longurl)

    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "base_url": BASE_URL,
                                       "shortened_url": shorturl}
                                      )


@app.post("/url-delete")
async def url_delete(request: Request):
    form = await request.form()
    form_data = dict(form)
    url_id = form_data.get("url_id")

    delete_url(db, url_id)

    return RedirectResponse("/admin")


@app.post("/admin")
@app.get("/admin")
async def admin(request: Request):
    links_obj = fetch_all_urls(db)
    links = [{"id": link[0], "shorturl": link[1], "longurl": link[2]} for link in links_obj]

    return templates.TemplateResponse("admin.html",
                                      {"request": request,
                                       "urls": links}
                                      )


@app.get("/{shorturl}")
async def redirect(shorturl: str):
    longurl = fetch_longurl(db, shorturl)
    if longurl != None:
        return RedirectResponse(url=longurl)
    else:
        return RedirectResponse("/")

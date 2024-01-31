import os

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import generate_short_url, SHORTENED_URL_LENGTH, BASE_URL
from database.dao import insert_urls, fetch_longurl, fetch_all_urls, delete_url
from database.database import db
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()


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


def authentication(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    admin_user = {
        "username": os.getenv("http_admin_username"),
        "password": os.getenv("http_admin_password")
    }
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = admin_user.get("username").encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = admin_user.get("password").encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/admin")
@app.get("/admin")
async def admin(request: Request, username: str = Depends(authentication)):
    links_obj = fetch_all_urls(db)
    links = [{"id": link[0], "shorturl": link[1], "longurl": link[2]} for link in links_obj]

    return templates.TemplateResponse("admin.html",
                                      {"request": request,
                                       "urls": links,
                                       "username": username},
                                      )


@app.get("/{shorturl}")
async def redirect(shorturl: str):
    longurl = fetch_longurl(db, shorturl)
    if longurl is not None:
        return RedirectResponse(url=longurl)
    else:
        return RedirectResponse("/")

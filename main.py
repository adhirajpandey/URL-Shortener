from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import urls, generate_short_url, SHORTENED_URL_LENGTH, BASE_URL

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

    urls[shorturl] = longurl

    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "base_url": BASE_URL,
                                       "shortened_url": shorturl}
                                      )


@app.get("/{shorturl}")
async def redirect(shorturl: str):
    longurl = urls[shorturl]
    return RedirectResponse(url=longurl)

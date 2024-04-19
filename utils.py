from string import ascii_lowercase
import random
from database.dao import fetch_all_shorturls
from database.database import db

# Configurations
BASE_URL = "https://urlshortener.adhirajpandey.me"  # "http://localhost:8000"
SHORTENED_URL_LENGTH = 8


urls = fetch_all_shorturls(db)


def generate_short_url(length):
    code = ""
    for i in range(length):
        code = code + random.choice(ascii_lowercase)

    if code in urls:
        generate_short_url(length)
    else:
        return code

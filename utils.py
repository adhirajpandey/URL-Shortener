from string import ascii_lowercase
import random

# configurations
BASE_URL = "https://urlshortener.adhiraj.live"  # "http://localhost:8000"
SHORTENED_URL_LENGTH = 8

urls = {}


def generate_short_url(length):
    code = ""
    for i in range(length):
        code = code + random.choice(ascii_lowercase)

    if code in urls:
        generate_short_url(length)
    else:
        return code

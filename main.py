# ---------------------------------------- PACKAGES ---------------------------------------- #
import lxml as lxml
from bs4 import BeautifulSoup
import requests
import lxml
from decouple import config

# ---------------------------------------- CONSTANTS ---------------------------------------- #
AMAZON_URL = "https://www.amazon.com.mx/AMD-Procesador-3-8GHz-Núcleos-Socket/dp/B0815XFSGK/ref=sr_1_1?" \
             "keywords=ryzen%2B7%2B5800x&qid=1665534459&qu=eyJxc2MiOiIyLjY1IiwicXNhIjoiMS41MCIsInFzcCI" \
             "6IjAuNjEifQ%3D%3D&sprefix=ryzen%2B%2Caps%2C144&sr=8-1&ufe=app_do%3Aamzn1.fos.66c34496-0d" \
             "28-4d73-a0a1-97a8d87ec0b2&th=1"
HEADER_URL = "http://myhttpheader.com"
CHAT_ID = config('CHAT_ID')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
HEADERS = {
    "User-Agent": "Defined",
    "Accept-Language": "es-419,es;q=0.9"
}


# ---------------------------------------- FUNCTIONS ---------------------------------------- #
def telegram_bot(text):
    parameters = {
        "chat_id": int(CHAT_ID),
        "text": text,
    }

    response = requests.post(url=TELEGRAM_API, params=parameters)
    response.raise_for_status()
    print(f"Request Status: {response.json()}\n")


def amazon_tracker():
    response = requests.get(AMAZON_URL, headers=HEADERS)
    website = response.text

    soup = BeautifulSoup(website, "lxml")

    price_tag = soup.find(name="span", class_="a-price-whole").text
    price_incomplete = price_tag.replace(",", "")
    price = price_incomplete.replace(".", "")

    try:
        with open("./lowest_price.txt", "r") as data_file:
            data = data_file.readline()
    except FileNotFoundError:
        with open("./lowest_price.txt", "w") as data_file:
            data_file.write(price)
    else:
        if int(data) > int(price):
            data = price

            message = f"NEW LOWEST PRICE FOUND\n" \
                      f"{AMAZON_URL}"
            telegram_bot(message)

            with open("./lowest_price.txt", "w") as data_file:
                data_file.write(data)


# ---------------------------------------- SCRIPT ---------------------------------------- #
amazon_tracker()


import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from csv import DictWriter

pg_index = 1

with open("quotesToScrape.csv", "w") as file:
    headers = ("name", "text", "bio")
    csv_writer = DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()
    while True:
        try:
            response = requests.get(f"http://quotes.toscrape.com/page/{pg_index}/")
            # print(response.status_code)
        except HTTPError:
            print("Page index has ended")
            break
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all(class_="quote")

            if not quotes:
                break
            for quote in quotes:
                csv_writer.writerow({
                    "name": quote.find(class_="author").get_text(),
                    "text": quote.find("span").get_text(),
                    "bio": quote.find("a")["href"]
                })

            pg_index += 1

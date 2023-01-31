import requests
from bs4 import BeautifulSoup

pg_index = 1
lst = []
while True:
    response = requests.get(f"http://books.toscrape.com/catalogue/page-{pg_index}.html")
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")
    if not articles:
        break

    for article in articles:
        title = str(article.find("h3").next_element).split('title=')[1].split(">")[0]
        price = article.find(class_="price_color").get_text()[1:]
        star_rating = str(article.find("p")).split("star-rating")[1].split('"')[0].strip() + " stars"
        in_stock = str(article.find(class_="instock availability")).split("</i>")[1].split("</p>")[0].strip()
        lst.append((title, price, star_rating, in_stock))
    pg_index += 1

num = 0
for i in range(len(lst)):
    for x in range(4):
        match num:
            case 0:
                print(f"Title: {lst[i][x]}")
            case 1:
                print(f"Price: {lst[i][x]}")
            case 2:
                print(f"Rating: {lst[i][x]}")
            case 3:
                print(f"Status: {lst[i][x]}")
        num += 1
    num = 0

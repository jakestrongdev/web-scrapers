import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from random import randint

start = time.time()
pg_index = 1
lst = []
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
            try:
                bio_response = requests.get(f"http://quotes.toscrape.com{quote.find('a')['href']}")
                # print(response.status_code)
            except HTTPError:
                print("Unable to access that page")
                break
            else:
                bio_soup = BeautifulSoup(bio_response.text, "html.parser")
                birthdate = bio_soup.find(class_="author-born-date").get_text()
                location = bio_soup.find(class_="author-born-location").get_text()
                lst.append((quote.find(class_="author").get_text(), quote.find("span").get_text(),
                            f"{birthdate} {location}"))
        pg_index += 1

r_num = randint(0, len(lst))
q = lst[r_num][1]
n = lst[r_num][0]
bd = lst[r_num][2]

guesses = 4
while True:
    match guesses:
        case 4:
            print("Here's a quote: ")
            print(q)
        case 3:
            print(f"The author was born on {bd}")
        case 2:
            print(f"The author's first name starts with a '{n[0]}'")
        case 1:
            split_name = n.split(" ")
            print(f"The author's last name starts with a '{split_name[1][0]}'")
        case 0:
            print(f"The name was {n}")
            i = input("Game over. Try again (y/n): ")
            if i == "y":
                r_num = randint(0, len(lst))
                q = lst[r_num][1]
                n = lst[r_num][0]
                bd = lst[r_num][2]
                guesses = 4
                continue
            else:
                break
    answer = input(f"Who said this? Guesses remaining, {guesses}: ")
    guesses -= 1
    if answer == n:
        print(f"Congrats! {n} is correct!")
        i = input("Try again (y/n):")
        if i == "y":
            r_num = randint(0, len(lst))
            q = lst[r_num][1]
            n = lst[r_num][0]
            bd = lst[r_num][2]
            guesses = 4
            continue
        else:
            break
    else:
        print("Sorry, incorrect!")

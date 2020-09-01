import requests
from bs4 import BeautifulSoup

URL = 'https://www.amazon.de/Syma-helicopter/dp/B00PJWNRDQ/ref=sr_1_5?__mk_de_DE=' \
      '%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=syma+x5c&qid=1598887623&sr=8-5'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) App"
                         "leWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}

# request all the data from the website
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find(id="priceblock_ourprice").get_text()
#price = soup.find(id="priceblock_ourprice")

print(title)



import requests
from bs4 import BeautifulSoup

URL = 'https://www.mediamarkt.es/es/product/_cargador-inal%C3%A1mbrico-belkin-boost-up-para-smartphones-qi-10w-pantalla-led-blanco-1457651.html'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) App"
                         "leWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}

# request all the data from the website
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')

title = soup.find('div', { "class" : "price"}).get_text()
#price = soup.find(id="priceblock_ourprice")

print(title)



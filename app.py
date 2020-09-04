import requests
from bs4 import BeautifulSoup

URL = 'https://www.mediamarkt.es/es/product/_cargador-inal%C3%A1mbrico-belkin-boost-up-para-smartphones-qi-10w-pantalla-led-blanco-1457651.html'

# request all the data from the website
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')

title = soup.find('div', { "class" : "price"}).get_text()
#price = soup.find(id="priceblock_ourprice")

print(title)



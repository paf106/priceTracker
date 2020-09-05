import requests
from bs4 import BeautifulSoup

#URL = 'https://www.mediamarkt.es/es/product/_cargador-inal%C3%A1mbrico-belkin-boost-up-para-smartphones-qi-10w-pantalla-led-blanco-1457651.html'
URL = str(input("Escribe la url: "))

# Request all the data from the website
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

if (URL.find("mediamarkt") != -1):
    # WORKING
    # We get the product title and the price
    productTitle = soup.find("h1").get_text()
    productPrice = soup.find('div', { "class" : "price"}).get_text()

    print("Nombre producto: "+productTitle.strip())
    print("Precio: "+productPrice.strip())
    
elif (URL.find("aliexpress") != -1):
    # NOT WORKING
    # We get the product title and the price
    #productPrice = soup.find('h1', { "class" : "product"}).get_text()
    #productTitle = soup.find('h1').get_text()
    productPrice = soup.find('div', { "class" : "product-info"}).get_text()
    
    print("Nombre producto: "+productTitle.strip())
    #print("Precio: "+productPrice.strip())

elif (URL.find("worten") != -1):
    # WORKING
    # We get the product title and the price
    productTitle = soup.find("h1").get_text()
    productPrice = soup.find('span', { "class" : "w-product__price__current"}).get_text()

    print("Nombre producto: "+productTitle.strip())
    print("Precio: "+productPrice.strip())
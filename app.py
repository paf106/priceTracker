import requests
from bs4 import BeautifulSoup
from tkinter import *

# Main Window
root = Tk()
root.title("Price Tracker")
root.geometry("400x400")

# Search field
inputField = Entry(root,width=38)
inputField.insert(0,"Type an URL")
inputField.grid(row=0, column=0)

# Search button
button_Search = Button(root, text="Search", command=lambda: checkPrice(inputField.get()))
button_Search.grid(row=0, column=1)

def checkPrice(URL):
    # Request all the data from the website
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

    except requests.exceptions.MissingSchema:
        print("Url not valid")
    except Exception:
        print("Something went wrong")

    if (URL.find("mediamarkt") != -1):
        # WORKING
        # We get the product title and the price
        try:
            productTitle = soup.find("h1").get_text()
            productPrice = soup.find('div', { "class" : "price"}).get_text()

            print("Product name: "+productTitle.strip())
            print("Price: "+productPrice.strip())

        except AttributeError:
            print("Product sold out or not trackable :(") 
        
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
        try:
            productTitle = soup.find("h1").get_text()
            productPrice = soup.find('span', { "class" : "w-product__price__current"}).get_text()

            print("Product name: "+productTitle.strip())
            print("Price: "+productPrice.strip())
        
        except AttributeError:
            print("Product sold out or not trackable :(")

    elif (URL.find("pccomponentes") != -1):
        # WORKING
        # We get the product title and the price
        try:
            productTitle = soup.find("h1").get_text()
            productPrice = soup.find('div', {"id" : "precio-main"}).get_text()

            print("Product name: "+productTitle.strip())
            print("Price: "+productPrice.strip())
        
        except AttributeError:
            print("Product sold out or not trackable :(")

root.mainloop()
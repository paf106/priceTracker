import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import os

# Main Window
root = Tk()
root.title("Price Tracker")
root.geometry("620x450")

# Root frame
dataFrame = LabelFrame(root)
label_dataFrame = Label(dataFrame,text="Only works with PcComponentes, Worten and Mediamarkt")
label_dataFrame.grid()
dataFrame.grid(row=2, column=0, columnspan=3, sticky="WE")

# History of products to be tracked
history = []

# Favourite products
favourite = []

# Check if "favouriteProducts.txt" exists and append the items to a list
if os.path.isfile("favouriteProducts.txt"):
    with open("favouriteProducts.txt", "r") as f:
        tempProducts = f.read()
        tempProducts = tempProducts.split(",")
        favourite = [x for x in tempProducts if x.strip()]
        f.close()

# Search field
inputField = Entry(root,width=38)
inputField.grid(row=0, column=0, ipady=4, pady=5, padx=2, sticky="WE")

def updateScreen(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def showHistory():
    historyWindow = Toplevel(root)
    historyWindow.title("History products")
    historyWindow.geometry("350x250")
    
    for link in history:
        label_url = Label(historyWindow,text=link)
        label_url.pack()
        
def deleteFavouriteProduct(product):
    pass
    

def addFavouriteProduct():
    urlToAdd = inputField_favouriteProduct.get()
    if (len(urlToAdd)!= 0 and urlToAdd.find(" ") == -1):
        button_searchFavourite = Button(favouriteWindow, text=urlToAdd, command= lambda:checkPrice(urlToAdd))
        button_searchFavourite.grid()
        
                # Add favourite products to a list
        favourite.append(urlToAdd)
        print(favourite)
    else:
        messagebox.showinfo("Empty field","You must write something")

def showFavourite():
    global favouriteWindow
    favouriteWindow = Toplevel(root)
    favouriteWindow.title("Favourite products")
    favouriteWindow.geometry("400x250")

    # Field to write an url
    global inputField_favouriteProduct
    inputField_favouriteProduct = Entry(favouriteWindow,width=38)
    inputField_favouriteProduct.grid(row=0, column=0, pady=5, padx=3, ipady=4)

    # Add button
    button_Add = Button(favouriteWindow, text="+", command=addFavouriteProduct)
    button_Add.grid(row=0, column=2, sticky="WE")

    # Delete button
    # Delete the content of the search field
    button_deleteFavourite = Button(favouriteWindow, text="X", command=lambda: button_clear(inputField_favouriteProduct))
    button_deleteFavourite.grid(row=0, column=1, sticky="WE")

    for x in favourite:
        button_favouriteProduct = Button(favouriteWindow,text=x, command = lambda: checkPrice(x)).grid()


    

def clearHistory():
    history.clear()
    messagebox.showinfo("History","History cleared")

def button_clear(entryToClear):
    entryToClear.delete(0, END)

def printProductData(name, price):
    global label_productName
    global label_productPrice

    updateScreen(dataFrame)

    label_productName = Label(dataFrame, text="Product name: "+ name[:57]+"...")
    label_productPrice = Label(dataFrame, text="Price: "+ price)

    label_productName.grid(row=2, column=0)
    label_productPrice.grid(row=3, column=0)

# Delete button
    # Delete the content of the search field
button_delete = Button(root, text="X", command=lambda: button_clear(inputField))
button_delete.grid(row=0, column=1, sticky="WE")


# Favourite urls button
button_favourite = Button(root, text="Favourite", command=showFavourite)
button_favourite.grid(row=1, column=0, sticky="EW", padx=2)

# History button
button_history = Button(root, text="History", command=showHistory)
button_history.grid(row=1, column=1, sticky="EW")

# Clear history button
button_clearHistory = Button(root, text="Clear history", command=clearHistory)
button_clearHistory.grid(row=1, column=2, sticky="EW")

# Search button
button_Search = Button(root, text="Search", command=lambda: checkPrice(inputField.get()))
button_Search.grid(row=0, column=2, sticky="EW")

def checkPrice(URL):
    # Request all the data from the website
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        if (URL.find("mediamarkt") != -1):
            # WORKING
            # We get the product title and the price
            try:
                productTitle = soup.find("h1").get_text()
                productPrice = soup.find('div', { "class" : "price"}).get_text()

                printProductData(productTitle.strip(), productPrice.strip())

                history.append(URL)

            except AttributeError:
                messagebox.showinfo("Info", "Product sold out or not trackable :(")
            
        elif (URL.find("aliexpress") != -1):
            # NOT WORKING
            # We get the product title and the price
            #productPrice = soup.find('h1', { "class" : "product"}).get_text()
            productTitle = soup.find('span', { "class" : "price"}).get_text()
            
            print("Nombre producto: "+productTitle.strip())
            #print("Precio: "+productPrice.strip())
        
        elif (URL.find("worten") != -1):
            # WORKING
            # We get the product title and the price
            try:
                productTitle = soup.find("h1").get_text()
                productPrice = soup.find('span', { "class" : "w-product__price__current"}).get_text()

                printProductData(productTitle.strip(), productPrice.strip())

                history.append(URL)
            
            except AttributeError:
                messagebox.showinfo("Info", "Product sold out or not trackable :(")

        elif (URL.find("pccomponentes") != -1):
            # WORKING
            # We get the product title and the price
            try:
                productTitle = soup.find("h1").get_text()
                productPrice = soup.find('div', {"id" : "precio-main"}).get_text()

                printProductData(productTitle.strip(), productPrice.strip())

                history.append(URL)
            
            except AttributeError:
                messagebox.showinfo("Info", "Product sold out or not trackable :(")
    # Errors handling
    except requests.exceptions.MissingSchema:
        messagebox.showwarning("Warning", "URL not valid")
    except requests.ConnectionError:
        messagebox.showwarning("Connection Error", "Failed to establish connection, check your internet connection")
    except requests.ConnectTimeout:
        messagebox.showinfo("Connection Timeout", "Connection timeout")
    except Exception:
        messagebox.showerror("Error","Something went wrong")

root.mainloop()

# Create a file to store favourite products
with open("favouriteProducts.txt", "w") as f:
    for product in favourite:
        f.write(product + ",")
    f.close()
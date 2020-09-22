import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import os
import smtplib

# Main Window
root = Tk()
root.title("Price Tracker")
root.geometry("620x450")

# Root frame
dataFrame = LabelFrame(root)
label_dataFrame = Label(dataFrame,text="Only works with PcComponentes, Worten and Mediamarkt")
label_dataFrame.grid()
dataFrame.grid(row=2, column=0, columnspan=3, sticky="WE")

# Menu
MainMenu = Menu(root)
root.config(menu=MainMenu)
def configureEmail():

    global configureEmailWindow
    configureEmailWindow = Toplevel(root)
    configureEmailWindow.title("Configure email")
    configureEmailWindow.geometry("360x250")

    # Field to write an email
    global inputField_email
    inputField_email = Entry(configureEmailWindow,width=38)
    inputField_email.grid(row=0, column=0, pady=5, padx=3, ipady=4)

    readEmailFile()

    # Save button
    button_saveEmail = Button(configureEmailWindow, text="Save", command=writeEmailToFile)
    button_saveEmail.grid(row=1, column=0, columnspan=2, padx=3, sticky="WE")

    # Delete button
    # Delete the content of the search field
    button_deleteFavourite = Button(configureEmailWindow, text="X", command=lambda: button_clear(inputField_email))
    button_deleteFavourite.grid(row=0, column=1, sticky="WE")

optionsMenu = Menu(MainMenu, tearoff=False)
MainMenu.add_cascade(label="Options", menu=optionsMenu)
optionsMenu.add_command(label="Send an email", command= lambda: sendEmail(emailToSend))
optionsMenu.add_checkbutton(label="Notify me lower price")
optionsMenu.add_command(label="Configure email", command=configureEmail)
optionsMenu.add_separator()
optionsMenu.add_command(label="About")
optionsMenu.add_command(label="Exit", command=root.quit)

# History of products to be tracked
history = []

# Favourite products
favourite = []

# Email to send
emailToSend = []

# write an email to a file
def writeEmailToFile():
    email = inputField_email.get()
    if (len(email)!= 0 and email.find(" ") == -1):
        with open("email.txt", "w") as f:
            f.write(email)
            f.close()
            for i in emailToSend:
                emailToSend.remove(i)
            emailToSend.append(email)
            messagebox.showinfo("Info", "Email "+email+" saved")
    else:
        messagebox.showwarning("Warning", "Don't leave it blank or type white spaces")
    

# check if the file where an email is going to be written is created
def readEmailFile():
    if os.path.isfile("email.txt"):
        with open("email.txt", "r") as f:
            for i in emailToSend:
                emailToSend.remove(i)
            
            emailToSend.append(f.readline())
            f.close()
            button_clear(inputField_email)
            inputField_email.insert(0,emailToSend[0])

# Send an email
def sendEmail(forwarder):
    try:
        if (len(forwarder) != 0):
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login("info.pricetracker@gmail.com", "ddhbjsbhoaizbgeu")

            subject = "Item: "
            body = "This is the price: "
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail(
                "info.pricetracker@gmail.com",
                forwarder[0],
                msg
            )
            messagebox.showinfo("Email sent", "Email to "+ forwarder[0] + " sent")
            server.quit()
        else:
            messagebox.showwarning("Email not set", "Please set an email to send the data")
    except smtplib.SMTPRecipientsRefused:
        messagebox.showerror("Email not valid", "Please write a valid email")
    except smtplib.SMTPDataError:
        pass




# Check if "favouriteProducts.txt" exists and append the items to a list
if os.path.isfile("favouriteProducts.txt"):
    with open("favouriteProducts.txt", "r") as f:
        tempProducts = f.read()
        tempProducts = tempProducts.split(",")
        favourite = [x for x in tempProducts if x.strip()]
        f.close()

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
            productTitle = soup.find(class_="product-price-value").get_text()
            
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
    except AttributeError:
        messagebox.showinfo("Info", "Product sold out or not trackable :(")
    except Exception:
       messagebox.showerror("Error","Something went wrong")

# Search field
inputField = Entry(root,width=38)
inputField.bind("<Return>",lambda event: checkPrice(URL= inputField.get())) 
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



root.mainloop()

# Create a file to store favourite products
with open("favouriteProducts.txt", "w") as f:
    for product in favourite:
        f.write(product + ",")
    f.close()
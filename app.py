import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import os
import smtplib
import csv
from ttkthemes import themed_tk as tk

# Main Window
root = tk.ThemedTk(theme="breeze")
root.title("Price Tracker")
root.geometry("530x250")

# Root frame
dataFrame = LabelFrame(root, bg="white")
dataFrame.grid(row=2, column=0, columnspan=3, sticky="WE")
label_dataFrame = Label(dataFrame,text="Only works with PcComponentes, Worten and Mediamarkt", bg="white")
label_dataFrame.grid()

# Menu
MainMenu = Menu(root)
root.config(menu=MainMenu)

def readFavouriteProducts():
    if os.path.isfile("favouriteProducts.csv"):
        with open("favouriteProducts.csv", "r") as csvFile:
            fieldnames= ["alias", "productName", "url"]
            csvReader = csv.DictReader(csvFile, fieldnames=fieldnames)
            csvReader.__next__()
            for line in csvReader:
                # Button that shows the url product
                button_favouriteProduct = Button(favouriteWindow, text=line["productName"], command=lambda line=line: checkPrice(line["url"]))
                button_favouriteProduct.grid(column=0)
            csvFile.close()

def addFavouriteProduct():
    urlToAdd = inputField_favouriteProduct.get()
    fieldnames= ["alias", "productName", "url"]
    if (len(urlToAdd)!= 0 and urlToAdd.find(" ") == -1):
        if os.path.isfile("favouriteProducts.csv"):
            with open("favouriteProducts.csv", "a+") as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
                csvWriter.writerow({"alias": "none", "productName": urlToAdd, "url": urlToAdd})
                csvFile.close()
        else:
            with open("favouriteProducts.csv", "w") as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
                csvWriter.writeheader()
                csvWriter.writerow({"alias": "none", "productName": urlToAdd, "url": urlToAdd})
                csvFile.close()

        button_favouriteProduct = Button(favouriteWindow, text=urlToAdd, command=lambda: checkPrice(urlToAdd))
        button_favouriteProduct.grid(column=0)
        button_clear(inputField_favouriteProduct)
    else:
        messagebox.showinfo("Empty field","You must write something")

def configureEmail():
    global configureEmailWindow
    configureEmailWindow = Toplevel(root)
    configureEmailWindow.title("Configure email")
    configureEmailWindow.geometry("360x250")

    # Field to write an email
    global inputField_email
    inputField_email = Entry(configureEmailWindow, width=38, bg="white")
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

# Email to send
emailToSend = []

# write an email to a file
def writeEmailToFile():
    email = inputField_email.get()
    if (len(email)!= 0 and email.find(" ") == -1):
        with open("email.txt", "w") as f:
            f.write(email)
            f.close()
            emailToSend.clear()
            emailToSend.append(email)
            messagebox.showinfo("Info", "Email "+email+" saved")
    else:
        messagebox.showwarning("Warning", "Don't leave it blank or type white spaces")
    
# check if the email file exists
def readEmailFile():
    if os.path.isfile("email.txt"):
        with open("email.txt", "r") as f:
            emailToSend.clear()
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

def checkPrice(URL):
    # Request all the data from the website
    try:
        page = requests.get(URL).text
        soup = BeautifulSoup(page, 'lxml')

        if (URL.find("mediamarkt") != -1):
            # WORKING
            # We get the product title and the price
            try:
                productTitle = soup.find("h1").text
                productPrice = soup.find('div', class_="price").text

                printProductData(productTitle.strip(), productPrice.strip())

                history.append(URL)

            except AttributeError:
                messagebox.showinfo("Info", "Product sold out or not trackable :(")
        
        elif (URL.find("worten") != -1):
            # WORKING
            # We get the product title and the price
            try:
                productTitle = soup.find("h1").text
                productPrice = soup.find('span', class_="w-product__price__current iss-product-current-price")["content"]

                printProductData(productTitle.strip(), productPrice.strip())

                history.append(URL)
            
            except TypeError:
                messagebox.showinfo("Info", "Product sold out or not trackable :(")

        elif (URL.find("pccomponentes") != -1):
            # WORKING
            # We get the product title and the price
            try:
                productTitle = soup.find("h1").text
                productPrice = soup.find('div',id="precio-main").text

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
    

def showFavourite():
    global favouriteWindow
    favouriteWindow = Toplevel(root)
    favouriteWindow.title("Favourite products")
    favouriteWindow.geometry("400x250")

    # Field to write an url
    global inputField_favouriteProduct
    inputField_favouriteProduct = Entry(favouriteWindow,width=38, bg="white")
    inputField_favouriteProduct.grid(row=0, column=0, pady=5, padx=3, ipady=4)

    # Add button
    button_Add = Button(favouriteWindow, text="Add", command=addFavouriteProduct, bg="#c9f9ff")
    button_Add.grid(row=0, column=2, sticky="WE")

    # Delete button
    # Delete the content of the search field
    button_deleteFavourite = Button(favouriteWindow, text="X", command=lambda: button_clear(inputField_favouriteProduct))
    button_deleteFavourite.grid(row=0, column=1, sticky="WE")

    readFavouriteProducts()


def clearHistory():
    history.clear()
    messagebox.showinfo("History","History cleared")

def button_clear(entryToClear):
    entryToClear.delete(0, END)

def printProductData(name, price):
    global label_productName
    global label_productPrice

    updateScreen(dataFrame)

    label_productName = Label(dataFrame, text="Product name: "+ name[:57]+"...", bg="white", font="Helvetica 10 bold")
    label_productPrice = Label(dataFrame, text="Price: "+ price, bg="white", font="Helvetica 10 bold")

    label_productName.grid(row=2, column=0)
    label_productPrice.grid(row=3, column=0)

# Delete button
    # Delete the content of the search field
button_delete = Button(root, text="X", command=lambda: button_clear(inputField))
button_delete.grid(row=0, column=1, sticky="WE")

# Search field
inputField = Entry(root,width=38, bg="white")
inputField.bind("<Return>",lambda event: checkPrice(URL= inputField.get())) 
inputField.grid(row=0, column=0, ipady=4, pady=5, padx=2, sticky="WE")

# Favourite urls button
button_favourite = Button(root, text="Favourite items", command=showFavourite)
button_favourite.grid(row=1, column=0, sticky="EW", padx=2)

# History button
button_history = Button(root, text="History", command=showHistory)
button_history.grid(row=1, column=1, sticky="EW")

# Clear history button
button_clearHistory = Button(root, text="Clear history", command=clearHistory)
button_clearHistory.grid(row=1, column=2, sticky="EW")

# Search button
button_Search = Button(root, text="Search", command=lambda: checkPrice(inputField.get()),bg="#c9f9ff")
button_Search.grid(row=0, column=2, sticky="EW")

root.mainloop()
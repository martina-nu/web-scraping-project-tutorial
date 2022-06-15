# your app code here

import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3

#print("Hello world")

#Step 3: Download the data using request library

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

resp = requests.get(url)

html_data = resp.text

#Step 4: Parse the html data using beautiful_soup

result = BeautifulSoup(html_data,"html.parser")

tables = result.find_all("table") #find all tables

for index,table in enumerate(tables): #get quarterly revenue table
    if "Tesla Quarterly Revenue" in str(table):
        my_index = index

#print(my_index)

df = pd.DataFrame(columns=["Date","Revenue"]) 

for row in tables[my_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if col != "":
        fecha = col[0].text
        rev = col[1].text.replace("$","").replace(",","")
        df = df.append({"Date":fecha, "Revenue":rev}, ignore_index=True)

print(df)






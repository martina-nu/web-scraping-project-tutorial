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

#print(df)


#Step 5: Clean rows (In exercise.ipynb)

df = df[df['Revenue'] != ""] #Filter empty strings out

# Step 6: Insert the data into sqlite3

# Insert the data into sqlite3 by converting the dataframe into a list of tuples

list_tuples = list(df.itertuples(index=False, name=None))


# Step 7: Connect to SQLite

conn = sqlite3.connect('Tesla.db')


# Step 8: Let's create a table in our database to store our revenue values

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE revenue
              (Date, Revenue)''')

# Insert values

c.executemany('INSERT INTO revenue VALUES (?,?)', list_tuples)


# Commit
conn.commit()


# Step 9: Retrieve data

for row in c.execute('SELECT * FROM revenue'):
    print(row)


# Step 10: Finally create a plot to visualize the data (In exercise.ipynb)










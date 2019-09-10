import re
from bs4 import BeautifulSoup as bs
import requests
from time import sleep
from random import randint
import _sqlite3
import sqlite3
from _sqlite3 import Error, DatabaseError
from decimal import Decimal
import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(30)

# try:
#     SCROLL_PAUSE_TIME = 0.5
#     driver.get("https://www.coinbase.com/price")
#
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     start=time.time()
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight-500);")
#         time.sleep(SCROLL_PAUSE_TIME)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             end=time.time()
#             print(end-start)
#             print("possible end")
#             break
#         last_height = new_height
#
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#
#     for c in soup("h2"):
#         print(c.get_text())
#
# finally:
#     driver.quit()

# import mysql.connector
# from mysql.connector import Error
# TAG_RE = re.compile('<[^>]+>')
#
# def remove_tags(text):
#     return TAG_RE.sub('', text)

# def cleanhtml(raw_html):
#     cleanr = re.compile('<.*?>')
#     cleantext = re.sub(cleanr, '', raw_html)
#     return cleantext

# def remove_html_tags(text):
#     """Remove html tags from a string"""
#     clean = re.compile('<.*?>')
#     newtext = re.sub(clean, '', text)
#     return newtext

def getHTML(url):
    html= requests.get(url)
    soup = bs(html.text,'lxml')
    return soup

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    sql_create_coin_data_table= """ CREATE TABLE IF NOT EXISTS CoinData (
                                    id integer PRIMARY KEY NOT NULL,
                                    Coinname text,
                                    acronym text,
                                    price double,
                                    market_cap double
                                ); """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    count=1
    URL="https://www.coinbase.com/price"
    r = requests.get(URL, timeout=5)
    data = r.text
    table = getHTML(URL).find('table')
    for row in table.find_all('h4'):
        cleantext = bs(row.text, "lxml").text
        print(cleantext,end=" ")
        if count%5==0:
            print()
        count+=1

    conn = create_connection("~/Documents/crypto/Stock/database.db")
    if conn is not None:
        create_table(conn, sql_create_coin_data_table)
    else:
        print('error creating connection')

import requests
import json
import csv

from bs4 import BeautifulSoup

url = "http://books.toscrape.com"

def scrapeBooks(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to load page")
        return []
    
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text,"html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    book_list=[]
    for book in books:
        title = book.h3.a['title']
        price_text= book.find('p',class_='price_color').text
        currency = price_text[0]
        price = float(price_text[1:]) 
        book_list.append({
            "title":title,
            "currency":currency,
            "price":price
        })
    return book_list

all_books = scrapeBooks(url)
with open ("book_list.json",'w',encoding="UTF-8") as f:
    json.dump(all_books,f,indent=4,ensure_ascii=False)

with open ("book_list.csv",'w',encoding="UTF-8") as c:
    all_books_csv = csv.DictWriter(c,fieldnames=["title","currency","price"])
    all_books_csv.writeheader()
    all_books_csv.writerows(all_books)

#importing required Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

page = 1
url = f'https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
prod_name = []
prod_price = []
prod_rating=[]
prod_review=[]
prod_url=[]

while True:
    if len(prod_name) > 200:
        break
    response = requests.get(url,headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    prod_data = soup.findAll('div', attrs= {'class': 's-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
    page+=1
    url = f'https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283'

    for store in prod_data:
        
        name = store.div.h2.a.span.text
        prod_name.append(name)

        try:
            price=store.div.find('span',class_='a-price-whole').text
        except:
            price = 'Null'
        prod_price.append(price)

        try:
            review=store.div.find('span',class_='a-size-base s-underline-text').text
        except:
            review = 'Null'
        prod_review.append(review)


        try:
            rating=store.div.find('span', class_='a-icon-alt').text
            rating = rating.split(" ")[0]
        except:
            rating = 'Null'
        prod_rating.append(rating)

        produrl=store.div.find('a')['href']
        prod_url.append('https://www.amazon.com'+produrl)
        
prod_DF = pd.DataFrame({'Name': prod_name,'Price':prod_price,'Rating':prod_rating,'Review':prod_review,'URL':prod_url})
prod_DF.head(7)
prod_DF.to_csv("Amazon.csv")
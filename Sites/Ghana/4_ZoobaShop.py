from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryZoobaShop():

    site = 'https://www.zoobashop.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.findAll("li",{"class":"parent"})
    urls = []

    for item in category[1:-2]:
        urlCategory = item.find('a',{"class":"dropdown-toggle"}).get("href") + "?limit=all"

        urls.append(
            urlCategory
        )

    return urls

#print(categoryZoobaShop())

def scrapZoobaShop(origin):

    site = 'https://www.zoobashop.com/'
    subUrls = categoryZoobaShop()
    produits = []

    for url in subUrls[0:1]:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/zooba.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/zoobashop.jpg'
        annonce = page_content.find_all("div", {"class": "wrap-item"})

        for item in annonce:
            try:
                url = item.find('div', {"class": "product-block"}).findAll("a")[0].get("href")
                lib = item.find('div', {"class": "product-block"}).find('div', {"class": "product-meta"}).find("h3").text
                img = item.find('div', {"class": "product-block"}).findAll("a")[0].find("img").get("src")
                try:
                    prix = int(float(
                    item.find('div', {"class": "product-price"}).find('span', {"class": "price"}).text.replace(u',',
                                                                                                               '').replace(
                        u'Ghs', '')))
                except:
                    prix=0

                produits.append(
                {
                'id': '',
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': prix,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                })

            except:
                continue

    return produits

#print(scrapZoobaShop(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapZoobaShop(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='ghana', produits=produits)

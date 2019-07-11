from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryMyGhMarket():

    site = 'https://www.myghmarket.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"id":"wide-nav"}).findAll("a",{"class":"nav-top-link"})
    categories_urls = []

    for item in category:
        urlCategory = item.get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryMyGhMarket())


def getAllPage():
    subUrl = categoryMyGhMarket()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('nav',{"class":"woocommerce-pagination"}).findAll('li')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "page/" + str(el)

                page.append(
                    link
                )
        except:

            link1 = url

            page.append(
                link1
            )

    return page

#print(getAllPage())

def scrapMyGhMarket(origin):

    site = 'https://www.myghmarket.com/'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/ghanamarket.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/myghanamarket.jpg'
        annonce = page_content.findAll('div', {"class": "product"})

        for item in annonce:
            try:
                url = item.find('div', {"class": "title-wrapper"}).find("p", {"class": "name"}).findAll("a")[0].get("href")
                lib = item.find('div', {"class": "title-wrapper"}).find("p", {"class": "name"}).text
                img = item.find('div', {"class": "box-image"}).findAll("a")[0].find("img").get("src")
                try:
                    prix = int(float(item.find('div', {"class": "price-wrapper"}).find('span', {
                    "class": "woocommerce-Price-amount"}).text
                                 .replace(u',', '').replace(u'₵', '')))
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

#print(scrapMyGhMarket(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapMyGhMarket(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='ghana', produits=produits)




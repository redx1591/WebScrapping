from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def subcategoryUzaPrice():

    site = 'http://www.uzaprice.com/for-sale'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"cat-tab"}).findAll("div",{"class":"link-wrap"})
    subUrl = []

    for item in category:
        urlCategory = item.find('a').get("href")

        subUrl.append(
            urlCategory
        )

    return subUrl

#print(subcategoryUzaPrice())


def getAllPage():
    subUrl = subcategoryUzaPrice()
    page = []
    maxPage = 5
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url +"/"+ str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())


def scrapUzaPrice(origin):
    site = 'http://www.uzaprice.com'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = ''
            logoS = ''
            annonce = page_content.find("div", {"class": "wrap"}).findAll("div",{"class":"simple-wrap"})
        except:
            pass

        for item in annonce:
            try:
                url = item.find('a',{"class": "img-link"}).get("href")
                lib = item.find_all("a", {"class": "title"})[0].text.strip()
                img = item.find('a',{"class": "img-link"}).find_all("img")[0].get("src")
                prix = item.find_all("div", {"class": "price"})[0].text.strip()

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
                }
                )

            except:
                continue

    return produits

#print(scrapUzaPrice(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapUzaPrice(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)
from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryEbeneMarket():

    site = 'https://www.ebenemarket.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"ul-box"}).findAll("li")
    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )


    return categories_urls

#print(categoryEbeneMarket())

def subCategoryEbeneMarket():
    categories_urls = categoryEbeneMarket()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('div', {"class": "cat-tab"}).find("div",{"class":"middle"}).findAll('a')

        for item in subCategories:
            subCategoryUrl = item.get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryEbeneMarket())

def getAllPage():
    subUrl = subCategoryEbeneMarket()
    page = []

    for url in subUrl:
        try:
            maxPage = 5
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url +"/"+ str(el)

                page.append({
                    'url': link
                }
                )
        except:
            continue

    return page
#print(getAllPage())

def scrapEbeneMarket(origin):
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        annonce = page_content.find("div",{"id":"list-view"}).find_all("div",{"class": "list-prod"})

        produits = []
        site = 'https://www.ebenemarket.com/'
        logo='http://137.74.199.121/img/logo/cm/ebene%20market.jpg'
        logoS='http://137.74.199.121/img/logo/cm/logoS/ebene%20market.jpg'

        for item in annonce:
            try:
                url = item.find('h3').find("a").get("href")
                lib = item.find('h3').find("a").text
                img = item.find('a',{"class":"big-img"}).find('img').get("src")

                try:
                    prix = int(float(item.find_all("div",{"class": "price"})[0].text.replace('FCFA','')))
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

#print(scrapEbeneMarket(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapEbeneMarket(origin=1)
insertProduct(user='root',passW='',host='localhost',dbname='cameroun', produits=produits)
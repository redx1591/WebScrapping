from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct,insertSubCat,insertCat

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryLocanto():

    site = 'https://www.locanto.cm/Achat-Vente/B/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.findAll("div",{"class":"nlp_categories__image_container"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryLocanto())


def subCategoryLocanto():

    categories_urls = categoryLocanto()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('ul', {"class": "left_nav__layer_2"}).findAll('li',{"class":"left_nav__layer_2_item"})

        for item in subCategories:
            subCategoryUrl = item.find('a').get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryLocanto())

def getAllPage():
    subUrl = subCategoryLocanto()
    page = []
    maxPage = 5
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())


def scrapLocanto(origin):
    site = 'https://www.locanto.cm'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/cm/locanto.jpg'
        logoS = 'http://137.74.199.121/img/logo/cm/logoS/locanto.jpg'
        annonce = page_content.find_all("div", {"class":"resultGallery"})

        for item in annonce:
            try:
                url = item.findAll('a')[0].get("href")
                lib = item.find_all("a")[0].find('div',{"class":"resultMain"}).find("div",{"class":"textHeader"}).text.replace('\n','').replace('\t','')
                img = item.find_all("a")[0].find('div',{"class":"resultImage"}).find("img").get("data-src")
                try:
                    prix = int(item.find_all("a")[0].find('div',{"class":"resultMain"}).find("div",{"class":"resultImage__add_info"}).text.replace('\n','').replace('  ','').replace('CFA','').replace(',',''))
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
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                })

            except:
                continue

    return produits

#print(scrapLocanto(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapLocanto(origin=1)
insertProduct(user='root',passW='',host='localhost',dbname='cameroun', produits=produits)
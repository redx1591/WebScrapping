from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryTonaton():

    site = 'https://tonaton.com'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.findAll("h4",{"class":"menu-item-header"})
    categories_urls = []


    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryTonaton())


"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryTonaton():

    categories_urls = categoryTonaton()
    subUrl = []
    site = 'https://tonaton.com'

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('ul', {"class": "ui-link-tree serp-category-links"}).findAll('li')

        for item in subCategories[2:-1]:
            try:
                subCategoryUrl = site + item.find('a').get("href")

            except:
                continue

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryTonaton())

def getAllPage():
    subUrl = subCategoryTonaton()
    page = []

    for url in subUrl:
        maxPage = 200+1
        id = list(range(maxPage))
        del id[0]
        for el in id:
            link = url + "?page=" + str(el)

            page.append({
                'url': link
            })

    return page

#print(getAllPage())

def scrapTonaton(origin):
    site = 'https://tonaton.com'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/tonaton.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/tonaton.jpg'
        try:
            annonce = page_content.find_all("div", {"class": "ui-item"})
        except:
            pass

        for item in annonce:
            try:
                url = item.find('div', {"class": "item-content"}).findAll("a")[0].get("href")
                lib = item.find('div', {"class": "item-content"}).findAll("a")[0].text.strip()
                img = item.findAll("a")[0].find("img").get("data-srcset").split(',')
                img = img[0].replace(' 1x','').replace('//','')
                try:
                    prix = int(
                    item.find('div', {"class": "item-content"}).find('p', {"class": "item-info"}).findAll("strong")[
                        0].text.replace(u',', '').replace(u'GH₵', ''))
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

#print(scrapTonaton(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapTonaton(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='ghana', produits=produits)

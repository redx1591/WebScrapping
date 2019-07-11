from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryPigiame():

    site = 'https://www.pigiame.co.ke'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"home-categories"}).findAll("a",{"class":"home-category__header"})
    categories_urls = []

    for item in category:
        urlCategory = item.get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryPigiame())

def subCategoryPigiame():
    categories_urls = categoryPigiame()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('ul', {"class": "filter__category-list--level-2"}).findAll('li',{"class":"filter__category-list-item--has-content"})

        for item in subCategories:
            subCategoryUrl = item.find('a').get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryPigiame())


def getAllPage():
    subUrl = subCategoryPigiame()
    page = []
    maxPage = 15
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url + "?p=" + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())


def scrapPigiame(origin):
    site = 'https://www.pigiame.co.ke'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''
        annonce = page_content.find_all("div", {"class":"listing-card--has-content"})

        for item in annonce:
            try:
                url = item.find('a', {"class": "listing-card__inner"}).get("href")
                lib = item.find("div", {"class": "listing-card__header__title"}).text.strip()
                img = item.find("img", {"class": "listing-card__image__resource"}).get("src")
                desc = item.find("p",{"class":"listing-card__description"}).text
                try:
                    prix = int(item.find("span", {"class": "listing-card__price__value"}).text.strip().replace(u'KSh','').replace(u',', ''))
                except:
                    prix=0

                produits.append(
                {
                'id': '',
                'libProduct': lib,
                'slug': '',
                'descProduct': desc,
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

#print(scrapPigiame(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapPigiame(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)
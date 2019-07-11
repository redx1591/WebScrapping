from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryEshopAfrica():

    site = 'http://www.eshopafrica.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"id":"vmenu"}).findAll('li',{"class":"menusep"})
    categories_urls = []

    for item in category[0:9]:
        try:
            catUrl = site + item.find('a').get("href")
        except:
            continue

        categories_urls.append(
            catUrl
        )

    return categories_urls

#print(categoryEshopAfrica())


def subCategoryEshopAfrica():

    categories_urls = categoryEshopAfrica()
    subUrl = []

    site = "http://www.eshopafrica.com/"

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            subCategories = page_content.find('div',{"class":"sectionsubcatlist"}).findAll('li')

            for item in subCategories:
                subCategoryUrl = item.find('a').get("href")

                subUrl.append(
                    site + subCategoryUrl
                )

        except:
            subCategoryUrl = el

            subUrl.append(
                site + subCategoryUrl
            )

    return subUrl

#print(subCategoryEshopAfrica())


def scrapEshopAfrica(origin):

    site = 'http://www.eshopafrica.com/'
    subUrls = subCategoryEshopAfrica()
    produits = []

    for el in subUrls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/eshopafrica.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/eshopafrica.jpg'
        annonce = page_content.find('tr', {"class": "viewItemList"}).findAll("div", {"class": "sectiondata"})


        for item in annonce:
            try:
                url = item.find('div', {"class": "PBItemName"}).findAll('a')[0].get("href")
                lib = item.find('div', {"class": "PBItemName"}).findAll('a')[0].find("h3").text
                img = item.find("div", {"class": "PBItemImg"}).find("a").find("img").get("src")
                desc = item.find("div", {"class": "PBItemImg"}).find('span', {"class": "PBShortTxt"}).text
                try:
                    prix = int(
                    item.find('div', {"class": "PBCurrency"}).find('span', {"class": "PBSalesPrice"}).text.replace(
                        u'.00', '').replace(u'$', ''))
                except:
                    prix=0

                produits.append(
                {
                'id': '',
                'libProduct': lib,
                'slug': '',
                'descProduct': desc,
                'priceProduct': prix,
                'imgProduct': site + img,
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

#print(scrapEshopAfrica(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapEshopAfrica(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='ghana', produits=produits)




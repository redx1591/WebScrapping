from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def subcategoryTheStar():
    site = 'https://www.the-star.co.ke/classifieds/home-living/'
    url = 'https://www.the-star.co.ke'
    subUrl = []

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subcategory = page_content.find('div',{"class":"popular-section-list"}).findAll('li')

    for item in subcategory:
        subCategoryUrl = url + item.find('a').get('href')

        subUrl.append(
            subCategoryUrl
        )

    return subUrl

#print(subcategoryTheStar())

def scrapTheStar(origin):

    site = 'https://www.the-star.co.ke/classifieds/home-living/'
    subUrls = subcategoryTheStar()
    produits = []

    for url in subUrls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''

        annonce = page_content.find_all("section", {"class": "home-living"})


        for item in annonce:
            try:
                url = item.find_all("a")[0].get("href")
                lib = item.find_all("h2", {"class": "product-title"})[0].text.strip()
                img = "https:" + item.find_all("img")[0].get('src')
                desc = item.find_all('p', {"class": "product-description"})[0].text.strip()


                try:
                    prix = int(item.find("div", {"class": "product-price"}).text.strip().replace(u',', '').replace(u'KSh', ''))
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

#print(scrapTheStar(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapTheStar(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)
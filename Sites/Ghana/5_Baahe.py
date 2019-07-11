from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def subcategoryBaahe():
    subUrl = []
    site = 'https://baahe.com/index.php'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"sf-menu"}).find_all('li')

    for item in category:
        try:
            catUrl = item.find('a').get("href")

        except:
            continue

        subUrl.append(
            catUrl
        )

    return subUrl
#print(subcategoryBaahe())

def getAllPage():

    subUrl = subcategoryBaahe()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('ul',{"class": "pagination"}).findAll('li')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "&p=" + str(el)

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

def scrapBaahe(origin):

    site = 'https://baahe.com/index.php'
    page = getAllPage()
    produits = []

    for el in page:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/baahe.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/bahoo.jpg'
        annonce = page_content.find_all("li", {"class": "ajax_block_product"})


        for item in annonce:
            try:
                url = item.find('div', {"class": "product-container"}).find("h5").find("a", {"class": "product-name"}).get(
                "href")
                lib = item.find('div', {"class": "product-container"}).find("h5").find("a", {
                "class": "product-name"}).text.strip()
                img = item.find("div", {"class": "product-image-container"}).find_all("img")[0].get("src")
                try:
                    prix = int(
                    item.find("div", {"class": "content_price"}).find("span", {"class": "price"}).text.strip().replace(
                        u'.00', '').replace(u'Ghc', '').replace(u',', ''))
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

#print(scrapBaahe(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapBaahe(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='ghana', produits=produits)
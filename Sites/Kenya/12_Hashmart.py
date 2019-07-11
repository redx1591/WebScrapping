from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryHashmart():

    site = 'https://hashmart.co.ke/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"mainmenu"}).findAll("a",{"class":"level-top"})
    categories_urls = []

    for item in category:
        urlCategory =  item.get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryHashmart())


def getAllPage():
    categories_urls = categoryHashmart()
    page = []

    for url in categories_urls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            maxPage = int(page_content.find('ul', {"class": "pages-items"}).findAll('li', {"class": "item"})[-2].findAll("span")[1].text) + 10
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?p=" + str(el)
                page.append({
                    'url': link
                })
        except:
            link1 = url
            page.append({
                'url': link1
            })

    return page

#print(getAllPage())


def scrapHashmart(origin):

    site = 'https://hashmart.co.ke/'
    page = getAllPage()
    produits = []
    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''

        annonce = page_content.find('ol',{"class":"product-items"}).findAll('li',{"class":"product-item"})

        for item in annonce:
            try:
                url = item.find("a",{"class":"product-item-photo"}).get("href")
                lib = item.find("strong", {"class": "product-item-name"}).text.strip()
                img = item.find("a",{"class":"product-item-photo"}).find('img').get("src")
                try:
                    prix = int(float(item.find("span", {"class": "price"}).text.replace('KES','').replace(',','')))
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
                'urlProduct':url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                })
            except:
                continue

    return produits

#print(scrapHashmart(origin=0))


"""INSERTION DES PRODUITS"""

produits = scrapHashmart(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)
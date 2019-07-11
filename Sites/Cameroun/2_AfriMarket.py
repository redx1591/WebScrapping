from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct


def categoryAfriMarket():

    site = 'https://afrimarket.cm/'

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"ms-topmenu"}).findAll("li",{"class":"topm"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a',{"class":"ms-label"}).get("href")

        categories_urls.append(
            urlCategory
        )

    del categories_urls[0]

    return categories_urls

#print(categoryAfriMarket())

def getAllPage():
    categories_urls = categoryAfriMarket()
    page = []

    for url in categories_urls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            sup = page_content.find('div', {"class": "pages"}).findAll('li', {"class": "item"})[-2].find('span',{"class":"label"}).text
            maxPage = int(page_content.find('div', {"class": "pages"}).findAll('li', {"class": "item"})[-2].text.replace(sup,'')) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?p=" + str(el)
                page.append({
                    'url': link
                }
                )
        except:

            link1 = url
            page.append({
                'url': link1
            })

    return page

#print(getAllPage())

def scrapAfriMarket(origin):

    site = 'https://afrimarket.cm/'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/cm/afrimArket.jpg"
        logoS="http://137.74.199.121/img/logo/cm/logoS/afrimarket.jpg"

        annonce = page_content.findAll("li", {"class": "item"})


        for item in annonce:
            try:
                url = item.find("div", {"class": "product-item-info"}).findAll('a', {"class": "product-item-link"})[0].get("href")
                lib = item.find("div", {"class": "product-item-info"}).findAll('a', {"class": "product-item-link"})[0].text.replace('\n','')
                img = item.findAll("img")[0].get("src")
                try:
                    prix = int(item.findAll("span", {"class": "price"})[0].text.replace(u'\xa0', '').replace(u'FCFA', ''))
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

#print(scrapAfriMarket(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapAfriMarket(origin=0)
insertProduct(user='root',passW='',host='localhost',dbname='cameroun', produits=produits)
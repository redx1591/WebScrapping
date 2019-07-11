from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryJumia():

    site = 'https://www.jumia.com.gh/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"menu-items"}).findAll("li",{"class":"menu-item"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryJumia())


def getAllPage():
    categories_urls = categoryJumia()
    page = []

    for url in categories_urls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('section',{"class":"pagination"}).findAll('li',{"class":"item"})[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?page=" + str(el)
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

def scrapJumia(origin):

    site = 'https://www.jumia.com.gh/'
    page = getAllPage()
    produits = []
    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/jumia.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/jumia.jpg'

        annonce = page_content.findAll('a', {"class": "link"})

        for item in annonce:
            try:
                url = item.get("href")
                lib = item.find_all("span", {"class": "name"})[0].text.strip()
                img = item.find('div', {"class": "image-wrapper default-state"}).find('img').get("data-src")
                try:
                    prix = int(
                    item.find_all("span", {"class": "price"})[0].text.strip().replace(u'GH₵', '').replace(u' ', ''))
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

#print(scrapJumia(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapJumia(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='ghana', produits=produits)



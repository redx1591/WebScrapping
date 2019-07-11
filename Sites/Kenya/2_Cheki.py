from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct


def subcategoryCheki():
    site = 'https://www.cheki.co.ke'
    subUrl = []

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subcategory = page_content.find('ul',{"class":"vehicleIcons"}).findAll('li')

    for item in subcategory:
        subCategoryUrl = item.find('a').get('href')

        subUrl.append(
            subCategoryUrl
        )

    return subUrl

#print(subcategoryCheki())


def getAllPage():
    subUrl = subcategoryCheki()
    page = []
    maxPage = 16
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url + "?page=" + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())

def scrapCheki(origin):

    site = 'https://www.cheki.com.ng'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS=''

        annonce = page_content.find_all("li", {"class": "listing-unit"})

        for item in annonce:
            try:
                url = item.get("data-url").replace('\n','').replace('  ','')
                lib = item.find('div', {"class": "listing-unit__title"}).find("a").text.replace('\n','')
                img = item.find('div', {"class": "listing-unit__image-container"}).findAll("img")[0].get("data-lazy")
                desc = item.find('div', {"class": "listing-unit__detail-container"}).text.replace('\n','')
                try:
                    prix = int(item.find("div", {"class": "listing-unit__price"}).text.replace(u',', '').replace(u'KSh', ''))
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
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                })

            except:
                continue

    return produits

#print(scrapCheki(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapCheki(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)

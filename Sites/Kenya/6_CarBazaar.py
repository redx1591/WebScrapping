from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def getAllPage():
    subUrl = "https://kenyacarbazaar.com/used-cars/"
    page = []
    maxPage = 15
    id = list(range(maxPage))
    del id[0]
    for item in id:
        link = subUrl + "page/" + str(item)
        page.append({
            'url': link
        })
    return page

#print(getAllPage())

def scrapCarBazaar(origin):

    site = 'https://kenyacarbazaar.com'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''

        annonce = page_content.find('div',{"id": "listings-result"}).findAll('div',{"class":"stm-isotope-listing-item"})

        for item in annonce:
            try:
                url = item.find('a').get("href")
                lib = item.find('a').find('div',{"class":"car-title"}).text.replace('\n','').replace('  ','')
                img = item.find('a').findAll('img')[0].get("src")
                prix = int(item.find('a').find('div', {"class": "normal-price"}).text.replace('Ksh. ','').replace(',',''))

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
                }
                )

            except:
                continue

    return produits

#print(scrapCarBazaar(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapCarBazaar(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)

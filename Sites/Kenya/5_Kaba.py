from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def getAllPage():
    subUrl = "http://www.kaba.co.ke/browse/recent"
    page = []
    maxPage = 4
    id = list(range(maxPage))
    del id[0]

    for item in id:
        link = subUrl + "?page=" + str(item)
        page.append({
            'url': link
        })
    return page

#print(getAllPage())

def scrapKaba(origin):

    site = 'http://www.kaba.co.ke'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''

        annonce = page_content.find('div',{"class": "listings"}).findAll('div',{"class":"list"})

        for item in annonce:
            try:
                url = item.find('h3').find('a').get("href")
                lib = item.find('h3').find('a').text
                img = site + item.find('div',{"class":"image"}).find('img').get('data-src')
                prix = int(item.find('div',{"class":"price"}).find('span', {"class": "buyout-amount"}).text.replace('KSHS ','').replace(',',''))

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

#print(scrapKaba(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapKaba(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)
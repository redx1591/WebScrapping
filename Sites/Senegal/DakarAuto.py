from bs4 import BeautifulSoup
import requests

def scrapDakarAuto(origin):

    site = 'http://www.dakar-auto.com/'

    subUrl = ['http://www.dakar-auto.com/senegal/voiture/occasion/recherche-tous.html#r231',
              'http://www.dakar-auto.com/senegal/moto-scooter/occasion/recherche-tous.html#r231']
    subName = ['Auto','Moto']

    produits = []

    for url,name in zip(subUrl,subName):
        try:
            page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = 'http://137.74.199.121/img/logo/sn/dakarauto.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/dakarauto.jpg'
            annonce = page_content.find("div", {"id": "results"}).findAll("a")
        except:
            continue

        for item in annonce:
            try:
                url = item.get("href")
                lib = item.find('div', {"class": "rc"}).find("h2").text
                img = item.find('div', {"class": "rc"}).find("img").get("src")
                try:
                    prix = item.find('div', {"class": "rc"}).text.split(' ')
                    price = int(prix[-4].replace(u'.', ''))
                except:
                    price=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': price,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                "country": "sn",
                "subcategory":name
                })

            except:
                continue


    return produits

#print(scrapDakarAuto(origin=1))

"""INSERTION DES CATEGORIES, SOUS-CATEGORIES ET DES PRODUITS"""

produits = scrapDakarAuto(origin=1)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

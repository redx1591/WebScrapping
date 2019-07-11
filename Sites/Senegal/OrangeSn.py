from bs4 import BeautifulSoup
import requests

def scrapOrangeSn(origin):

    site = 'https://www.orange.sn'
    subUrl = ["https://boutique.orangebusiness.sn/?_ga=2.179543847.2053783743.1545047841-576526551.1542638349"]
    produits = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/sn/orangesn.jpg'
        logoS = 'http://137.74.199.121/img/logo/sn/logoS/orangesn.jpg'

        annonce = page_content.findAll("div",{"class":"product-layouts"})


        for item in annonce:
            try:
                url = item.find("h4").find('a').get("href")
                lib = item.find("h4").text
                img = item.find("img").get("src")

                try:
                    prix = int(item.find("div", {"class": "price"}).text.replace("\r\n","").replace("  ","").replace("FCFA","").replace(" ",""))
                except:
                    prix=0

                produits.append(
                {
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
                "country": "sn",
                "subcategory":"smartphone"
                })

            except:
                continue

    return produits

#print(scrapOrangeSn(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapOrangeSn(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass


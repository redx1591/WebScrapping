from bs4 import BeautifulSoup
import requests

def scrapTigoSn(origin):
    site = 'https://tigo.sn'
    subUrl = ["https://www.tigo.sn/telephones",
              "https://www.tigo.sn/telephones?start=20",
              "https://www.tigo.sn/telephones?start=40"]
    produits = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/sn/tigosn.jpg'
        logoS = 'http://137.74.199.121/img/logo/sn/logoS/tigosn.jpg'
        annonce = page_content.findAll("div", {"class": "phone-box"})


        for item in annonce:
            try:
                url = item.find('a').get("href")
                lib = item.find("div",{"class":"phone-details"}).find("h4").text
                img = item.find('a').find("img").get("src")
                try:
                    prix = int(item.find("div",{"class":"phone-details"}).find("p").text.replace('CFA','').replace(',',''))
                except:
                    prix=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': prix,
                'imgProduct': site + img,
                'numSeller': '',
                'src': site,
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                'country':"sn",
                'subcategory':'smartphone'
                })

            except:
                continue

    return produits

#print(scrapTigoSn(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapTigoSn(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass


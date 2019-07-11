from bs4 import BeautifulSoup
import requests

def senShopScrap(origin):
    site = 'http://senshop.sn/'
    produits = []
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    logo = 'http://137.74.199.121/img/logo/sn/senshop1.png'
    logoS = 'http://137.74.199.121/img/logo/sn/senshop1.png'

    annonce = page_content.findAll('div', {"class": "product-list"})

    for item in annonce:
        try:
                url = item.find('h2').find('a').get("href")
                lib = item.find('h2').find('a').text.strip()
                img = item.find("div",{"class":"img-container"}).find_all("img")[0].get('src')
                try:
                    prix = int(item.find("div", {"class":"price"}).find("span", {"class":"underline"}).find_all("span")[0].text.replace('FCFA','').replace(',',''))
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
                "subcategory":"informatique"
                })


        except:
                continue

    return produits

produits = senShopScrap(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass
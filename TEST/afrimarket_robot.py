from bs4 import BeautifulSoup
import requests


def getAllPage():

    subUrl = {
        "url":"https://afrimarket.sn/electromenager3/petit-electromenager3.html?cat=609",
        "name": "Mixeurs et Robots"
    }
    page = []

    page_response = requests.get(subUrl['url'], headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    try:
        sup = page_content.find('div', {"class": "pages"}).findAll('li', {"class": "item"})[-2].find('span',{"class":"label"}).text
        maxPage = int(page_content.find('div', {"class": "pages"}).findAll('li', {"class": "item"})[-2].text.replace(sup,'')) + 1
        id = list(range(maxPage))
        del id[0]

        for el in id:
            link = subUrl['url'] + "?p=" + str(el)

            page.append({
                'url':link,
                'name':subUrl['name']
            })
    except:

        link1 = subUrl['url']

        page.append({
            'url':link1,
            'name':subUrl['name']
        })

    return page

#print(getAllPage())

def scrapAfriMarket(origin):

    site = 'https://afrimarket.sn/'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = "http://137.74.199.121/img/logo/sn/afrimArket.jpg"
            logoS = "http://137.74.199.121/img/logo/sn/logoS/afrimarket.jpg"
            annonce = page_content.findAll("li", {"class": "item"})
        except:
            continue

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
                "subcategory":link['name'],
                "custom_category_id": 6
                }
                )

            except:
                continue

    return produits

#print(scrapAfriMarket(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapAfriMarket(origin=0)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

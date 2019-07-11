from bs4 import BeautifulSoup
import requests

def categoryOkaidi():
    site = "https://www.okaidi.fr/"
    category = []

    page_response = requests.get(site, headers={'User-Agent':'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content,'html.parser')

    cat = page_content.find('nav',{'id':'navigation'}).findAll("li",{"class":"level-0"})

    for item in cat:
        catName = item.find("a",{"class":"label-n0"}).text.strip()
        catUrl = "https://www.okaidi.fr" + item.find("a",{"class":"label-n0"}).get("href")

        category.append({
            'url':catUrl,
            'name':catName
        })

    return category

print(categoryOkaidi())


def ScrapOkaidi(origin):
    site = "https://www.okaidi.fr"
    produits = []

    link = categoryOkaidi()

    for item in link:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, 'html.parser')

        post = page_content.find("ul",{"id":"inject-items"}).findAll("li",{"class":"item-box"})

        logo = 'http://137.74.199.121/img/logo/inter/okaidi.jpg'
        logoS = 'http://137.74.199.121/img/logo/inter/logoS/okaidi.jpg'

        for elem in post:
            try:
                lib = elem.find('div',{'class':'details'}).find('span',{"class":"product-title-txt"}).text
                url = elem.find('div',{'class':'details'}).find('a',{"class":"product-title"}).get("href")
                img = elem.find('div',{"class":"picture"}).find('img').get("src")
                prix = float(elem.find('div',{'class':'prices'}).find("span",{"class":"actual-price"}).text.replace(',','.').replace('€','')) * 655.8

                produits.append({
                    'libProduct': lib,
                    'slug': '',
                    'descProduct': '',
                    'size': 1,
                    'unit': 'Kg',
                    'priceProduct': int(prix),
                    'imgProduct': img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': site + url,
                    'logo': logo,
                    'logoS': logoS,
                    'origin': origin,
                    "country": "",
                    'subcategory': item['name'],
                })
            except:
                continue
    return produits

"""produits = ScrapOkaidi(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass"""
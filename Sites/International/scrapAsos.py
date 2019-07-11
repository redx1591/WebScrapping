from bs4 import BeautifulSoup
import requests
from decimal import *

def categoryAsos():
    urls = ["https://www.asos.fr/homme/?crd=true","https://www.asos.fr/femme/?crd=true"]
    names = ["Homme","Femme"]
    category = []
    for url,name in zip(urls,names):
        category.append({
            "name": name,
            "url" : url
        })

    return category

#print(categoryAsos())

def subcategoryAsos():
    cat = categoryAsos()
    subCat = []
    for item in cat:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        category = page_content.find('article',{'class':'productCat'}).find("ul",{"class":"carousel__list"}).findAll("li")

        for item in category:
            catName = item.find("a").find('span',{'class':'carousel__labelText'}).text
            catUrl = item.find('a').get("href")

            subCat.append({
            "name":catName,
            "url": "https://www.asos.fr" + catUrl
            })

    return subCat


def getAllPage():
    subCat = subcategoryAsos()
    page = []
    for item in subCat:
        try:
            maxPage = 10
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = item['url'] + "?page=" + str(el)
                name = item['name']
                page.append({
                    'url': link,
                    'name':name
                }
                )
        except:
            continue

    return page


#print(getAllPage())


def scrapAsos(origin):
    site = 'https://www.asos.fr'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/inter/asos.jpg'
        logoS = 'http://137.74.199.121/img/logo/inter/logoS/asos.jpg'

        annonce = page_content.findAll('article',{"class":"_2oHs74P"})

        for item in annonce:
            try:
                url = item.find("a").get("href")
                lib = item.find("div", {"class": "_2Raol8i"}).text.strip()
                img = item.find("img").get('src')
                try:
                    prix = float(item.find("span", {"class": "_342BXW_"}).text.strip().replace(" €","").replace(",","."))
                except:
                    prix = 0

                produits.append(
                    {
                        'libProduct': lib,
                        'slug': '',
                        'descProduct': '',
                        'size': 1,
                        'unit': 'Kg',
                        'priceProduct': int(prix) * 657,
                        'imgProduct': img.replace("//","http://"),
                        'numSeller': '',
                        'src': site,
                        'urlProduct': url,
                        'logo': logo,
                        'logoS': logoS,
                        'origin': origin,
                        "country": "asos",
                        'subcategory': link['name'],
                    })


            except:
                continue

    return produits

#print(scrapAsos(origin=0))

produits = scrapAsos(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())

    except:
        pass


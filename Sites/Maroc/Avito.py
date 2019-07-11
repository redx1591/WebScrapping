from bs4 import BeautifulSoup
import requests


"""Fontion pour récupérer les urls de toutes les catégories """

def categoryAvito():

    site = 'https://www.avito.ma/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"categories"}).findAll("a")
    categories_urls = []

    for item in category:
        urlCategory = item.get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryAvito())

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryAvito():
    categories_urls = categoryAvito()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.findAll('td', {"class": "span4 panel-item"})

        for item in subCategories:
            subCategoryUrl = item.findAll('a')[0].get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryAvito())

def getAllPage():
    subUrl = subCategoryAvito()
    page = []
    maxPage = 5
    id = list(range(maxPage))
    del id[0]
    for url in subUrl[0:1]:
        for item in id:
            link = url + "?o=" + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())

def scrapAvito(origin):
    site = 'https://www.avito.ma'
    page = getAllPage()
    produits = []
    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        logo = 'http://137.74.199.121/img/logo/ma/avito.jpg'
        logoS = 'http://137.74.199.121/img/logo/ma/logoS/avito.jpg'
        annonce = page_content.findAll('div', {"class": "item"})

        for item in annonce:
            try:
                url = item.findAll('a')[0].get("href")
                lib = item.findAll('h2', {"class": "fs14"})[0].text.strip()
                img = item.find_all('div', {"class": "item-img"})[0].find("img").get("data-original")

                try:
                    prix = int(item.find_all("span", {"class": "price_value"})[0].text.strip().replace(' ', ''))
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
                    'logo':logo,
                    'logoS':logoS,
                    'origin': origin,
                    "country": "ma",
                })

            except:
                continue

    return produits

"""produits = scrapAvito(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())"""






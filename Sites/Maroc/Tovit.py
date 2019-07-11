from bs4 import BeautifulSoup
import requests

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryTovit():

    site = 'http://www.tovit.ma/'
    subUrl = []
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subCategories = page_content.find('ul',{"id":"menu-header"}).findAll('ul',{"role":"menu"})

    for item in subCategories:
        links = item.find_all('a')
        for link in links:
            subCategoryUrl = link.get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryTovit())

def getAllPage():
    subUrl = subCategoryTovit()
    page = []

    for url in subUrl:
        try:
            maxPage = 5
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "page/" + str(el)

                page.append(
                    link
                )
        except:

            link1 = url

            page.append(
                link1
            )

    return page

#print(getAllPage())

def scrapTovit(origin):
    site = 'http://www.tovit.ma/'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        logo = 'http://137.74.199.121/img/logo/ma/tovit.jpg'
        logoS  = 'http://137.74.199.121/img/logo/ma/logoS/tovit.jpg'
        annonce = page_content.findAll('div', {"class": "wrap-item"})

        for item in annonce:
            try:
                url = item.findAll('h4')[0].find('a').get("href")
                lib = item.findAll('h4')[0].text.strip()
                img = item.findAll('img')[0].get("src")
                desc = item.findAll('p', {"class": "item-desc"})[0].text.strip()

                try:
                    prix = int(item.findAll('p', {"class": "post-price"})[0].text.replace(u' ', '').replace(u'DH', ''))
                except:
                    prix=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': desc,
                'priceProduct': prix,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                'country':'ma'
                }
                )
            except:
                continue

    return produits

"""produits = scrapTovit(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())"""



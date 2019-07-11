from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct
def categoryJumiaDeals():

    site = 'https://deals.jumia.co.ke/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"list-group"}).findAll("li",{"class":"list-group-item"})
    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryJumiaDeals())


def subCategoryJumiaDeals():

    site = 'https://deals.jumia.co.ke'
    categories_urls = categoryJumiaDeals()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('nav', {"class": "category-links"}).findAll('li')

        for item in subCategories:
            subCategoryUrl = site + item.find('a').get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryJumiaDeals())

def getAllPage():
    subUrl = subCategoryJumiaDeals()
    page = []
    maxPage = 9
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url + "?page=" + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())

def scrapJumiaDeal(origin):
    site = 'https://deals.jumia.co.ke'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''
        annonce = page_content.find_all("div", {"class": "post"})

        for item in annonce:
            try:
                url = item.findAll('a', {"class": "post-link"})[0].get("href")
                lib = item.find_all("a", {"class": "post-link"})[0].findAll("span")[0].text.strip()
                img = item.find_all("div", {"class": "alignleft"})[0].find_all("img", {"class": "product-images"})[0].get(
                "data-src")
                try:
                    prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace(u'KES','').replace(u',', ''))
                except:
                    prix=0

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
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                })

            except:
                continue

    return produits

#print(scrapJumiaDeal(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapJumiaDeal(origin=1)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)

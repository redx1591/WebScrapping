from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from DataInsertion.database import  insertProduct

def categoryAfrimalin():

    site = "https://www.afrimalin.cm"
    req = Request(site, headers={'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
    page_html = urlopen(req).read()
    urlopen(req).close()
    parsed_page = soup(page_html, "html.parser")

    category = parsed_page.find('div',{"class":"adListsCategoriesWrapper"}).findAll("div",{"class":"singleAdListCategory"})

    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryAfrimalin())

def subCategoryAfrimalin():

    categories_urls = categoryAfrimalin()
    subUrl = []

    site = "https://www.afrimalin.cm"

    for el in categories_urls:
        req = Request(el, headers={'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        parsed_page = soup(page_html, "html.parser")

        subCategories = parsed_page.find('div', {"class": "adListsCategoriesWrapper"}).findAll('li')

        for item in subCategories:
            subCategoryUrl = site + item.find('a').get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryAfrimalin())

def getAllPage():
    subUrl = subCategoryAfrimalin()
    page = []

    for url in subUrl:
        try:
            maxPage = 5
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?sort=creationDate&direction=desc&page=" + str(el)
                page.append({
                    'url': link
                })
        except:
            continue

    return page

#print(getAllPage())


def afrimalinScrap(origin):
    site = "https://www.afrimalin.sn"
    page = getAllPage()
    produits = []

    for link in page:
        req = Request(link["url"], headers={'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        logo = 'http://137.74.199.121/img/logo/cm/afrimalin.jpg'
        logoS = 'http://137.74.199.121/img/logo/cm/logoS/1.jpg'

        parsed_page = soup(page_html, "html.parser")
        products_container = parsed_page.find('div',{"class":"adListsWrapper"}).findAll('div',{"class":"singleAdWrapper"})

        for item in products_container:
            try:
                url = item.find("h2").findAll('a')[0].get("href")
                lib = item.find("h2").findAll('a')[0].text
                img = item.find('div',{"class":"singleAdPhoto"}).findAll("img")[0].get("src")
                try:
                    prix = int(item.findAll("p", {"class": "green-color"})[0].text.replace(u'FCFA', '').replace(' ',''))
                except:
                    prix = 0

                produits.append({
                'id': '',
                'libProduct':lib,
                'slug':'',
                'descProduct':'',
                'priceProduct': prix,
                'imgProduct':img,
                'numSeller':'',
                'src':site,
                'urlProduct':site + url,
                'logo':logo,
                'logoS':logoS,
                'origin': origin,
                })

            except:
                continue

    return produits

#print(afrimalinScrap(origin=1))

"""INSERTION DES PRODUITS"""

produits = afrimalinScrap(origin=1)
insertProduct(user='root',passW='',host='localhost',dbname='cameroun', produits=produits)
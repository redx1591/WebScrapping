from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryCoinAfrique():
    site = "https://cm.coinafrique.com"
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"categories"}).findAll('div',{"class":"collection-item collapsible-body"})
    categories_urls = []

    for item in category :
        urlCategory = site + item.findAll('a')[-1].get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryCoinAfrique())

def subcategoryCoinAfrique():
    categories_urls = categoryCoinAfrique()
    subUrl = []

    site = "https://cm.coinafrique.com"

    for url in categories_urls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        index = categories_urls.index(url)
        element = page_content.find('ul',{"class":"collection"}).findAll('div',{"class":"collection-item collapsible-body"})[index]
        subcategory = element.findAll('a')

        for item in subcategory[0:-2]:
            subCategoryUrl = site + item.get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subcategoryCoinAfrique())

def getAllPage():
    subUrl = subcategoryCoinAfrique()
    page = []

    for url in subUrl:
        maxPage = 5
        id = list(range(maxPage))
        del id[0]

        for el in id:
            link = url + "?page=" + str(el)
            page.append({
                'url': link
            }
            )
    return page

#print(getAllPage())

def coinAfriqueComScrap(origin):
    site = "https://cm.coinafrique.com"
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        products_container = page_content.find_all("div", {"class":"card round"})

        logo = "http://137.74.199.121/img/logo/cm/coin%20afrique.jpg"
        logoS = "http://137.74.199.121/img/logo/cm/logoS/coin%20afrique.jpg"

        for elem in products_container:
            try:
                product_img = elem.find_all("div", {"class":"card-image"})[0].find_all("a")[0].find_all("img")[0].get("src")
            except:
                product_img = ""
            try:
                product_name = elem.find_all("div", {"class":"card-content"})[0].find_all("p", {"class":"card-desc"})[0].find_all("a")[0].text.strip()
            except:
                product_name = ""
            try:
                product_url = elem.find_all("div", {"class":"card-content"})[0].find_all("p", {"class":"card-desc"})[0].find_all("a")[0].get("href")
                product_url = site + product_url
            except:
                product_url = ""
            try:
                product_price = int(elem.find_all("div", {"class":"card-content"})[0].find_all("p")[0].text.replace(u'\xa0','').replace(u'CFA', '').replace(u' ',''))
            except:
                product_price = 0

            produits.append({
                'id':"",
                'libProduct':product_name,
                'slug':'',
                'descProduct':'',
                'priceProduct': product_price,
                'imgProduct':product_img,
                'numSeller':'',
                'src':site,
                'urlProduct':product_url,
                'logo':logo,
                'logoS':logoS,
                'origin': origin,
                })

    return produits

#print(coinAfriqueComScrap(origin=1))

"""INSERTION DES PRODUITS"""

produits = coinAfriqueComScrap(origin=1)
insertProduct(user='root',passW='',host='localhost',dbname='cameroun', produits=produits)
from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def categoryKiliMall():

    site = 'https://www.kilimall.co.ke/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"category"}).findAll("h4")
    categories_urls = []

    for item in category:
        urlCategory =  item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryKiliMall())

def subCategoryKiliMall():

    categories_urls = categoryKiliMall()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('div', {"class": "nav-list-item"}).find('dl',{"id":"mytree"}).findAll('a')

        for item in subCategories:
            subCategoryUrl = item.get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryKiliMall())

def getAllPage():
    subUrl = subCategoryKiliMall()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            newUrl = page_content.find('div',{"class":"new-pagination"}).findAll('li')[3].find('a').get("href")
            part = newUrl.split('.h')
            part1=part[0]

            maxPage = page_content.find('div',{"class":"new-pagination"}).findAll('li')[-1].find('a').get('href')
            p = maxPage.split('.h')
            p1 = p[0]
            num = p1.split("-")
            last = int(num[-1])
            id = list(range(last))
            del id[0]

            for el in id:
                link = part1.replace(part1[-1],str(el))+'.html'

                page.append({
                    'url': link
                }
                )
        except:

            link1 = url

            page.append({
                'url': link1
            }
            )


    return page

#print(getAllPage())

def scrapKiliMall(origin):

    site = 'https://www.kilimall.co.ke/'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ''
        logoS = ''
        annonce = page_content.find("ul", {"class": "list_pic"}).findAll('li', {"class": "item"})


        for item in annonce:
            try:
                url = item.find('a', {"class": "lazyload"}).get("href")
                lib = item.find('div', {"class": "goods-info"}).find('h2', {"class": "goods-name"}).text.replace('\n\n\n','').replace('  ','')
                img = item.find('div', {"class": "goods-pic"}).find("a").get("data-src")
                try:
                    prix = int(item.find("div", {"class": "goods-price"}).find("em").text.replace('KSh ','').replace(',',''))
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
                'urlProduct': url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                }
                )

            except:
                continue

    return produits

#print(scrapKiliMall(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapKiliMall(origin=0)
insertProduct(user='root', passW='', host='localhost', dbname='kenya', produits=produits)



from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryMarocAnnonces():

    site = 'https://www.marocannonces.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"categories"}).findAll("li",{"class":"category_title"})
    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryMarocAnnonces())

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryMarocAnnonces():

    categories_urls = categoryMarocAnnonces()
    subUrl = []
    site = 'https://www.marocannonces.com/'

    for el in categories_urls[0:-3]:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('ul', {"class": "categoriesdec"}).findAll('li',{"class":"category_title"})

        for item in subCategories:
            try:
                subCategoryUrl = site + item.find('a').get("href")

                subUrl.append(
                    subCategoryUrl
                )

            except:
                continue

    return subUrl

#print(subCategoryMarocAnnonces())

def getAllPage():
    subUrl = subCategoryMarocAnnonces()
    page = []

    for url in subUrl:
        try:
            maxPage = 5
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url.replace(".html","") + "/" + str(el) + ".html"

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

def scrapMarocAnnonces(origin):

    site = 'https://www.marocannonces.com/'
    page = getAllPage()
    produits = []

    for url in page :
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ma/marocannonces.jpg'
        logoS = ''
        annonce = page_content.find_all("div", {"class": "content_box"})[0].findAll('li')


        for item in annonce:
            try:
                url = item.findAll('a')[0].get("href")
                lib = item.findAll('h3')[0].text.strip()
                img = item.find_all('a')[0].find("img", {"class": "lazy"}).get("data-original")
                try:
                    prix = int(item.find_all("strong", {"class": "price"})[0].text.strip().replace(u' ', '').replace(u'DH', ''))
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

"""produits = scrapMarocAnnonces(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())"""






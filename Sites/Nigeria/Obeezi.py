from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryObeezi():

    site = 'https://www.obeezi.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"groupmenu"}).findAll("li",{"class":"parent"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryObeezi())

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryObeezi():

    categories_urls = categoryObeezi()
    subUrl = []

    for el in categories_urls[0:-1]:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('div', {"class": "filter-options-content"}).findAll('li',{"class":"item"})

        for item in subCategories:
            subCategoryUrl = item.find('a').get("href")

            subUrl.append(
                subCategoryUrl + '&product_list_limit=all'
            )
    url = 'https://www.obeezi.com/women-fashion.html?product_list_limit=all'

    subUrl.append(
        url
    )


    return subUrl

#print(subCategoryObeezi())

def obeeziScrap(origin):

    site = 'https://www.obeezi.com/'
    subUrls = subCategoryObeezi()
    produits = []

    for url in subUrls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ng/obeezi.jpg"
        logoS = "http://137.74.199.121/img/logo/ng/logoS/obeezi.jpg"

        annonce = page_content.find('div',{"id":"category-products-grid"}).findAll('li', {"class": "product-item"})


        for item in annonce:
            try:
                url = item.find('a').get("href")
                lib = item.find("div", {"class": "product-item-details"}).find('strong').text.strip()
                img = item.find('span',{"class":"product-image-wrapper"}).find("img").get('src')
                try:
                    prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace(',','').replace('₦',''))
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
                'country':'ng'
                }
                )

            except:
                continue

    return produits


produits = obeeziScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())
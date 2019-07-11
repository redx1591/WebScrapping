from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests

"""Fonction pour récupérer les noms et les urls de toutes les catégories"""

def subcategoryChoix():

    subUrl = []
    site = "http://www.choix.ma/store/"

    req = Request(site, headers={'User-agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    urlopen(req).close()

    parsed_page = soup(page_html, "html.parser")
    subCategories = parsed_page.find('ul',{"class":"sub-menu"}).findAll('li')

    for item in subCategories:
        subCategoryUrl = item.find("a").get("href")

        subUrl.append(
            subCategoryUrl
        )

    return subUrl

#print(subcategoryChoix())

def getAllPage():

    subUrl = subcategoryChoix()
    page = []

    for url in subUrl:
        req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        parsed_page = soup(page_html, "html.parser")

        try:
            maxPage = int(
                parsed_page.find('nav', {"class": "woocommerce-pagination"}).findAll('li')[-2].find("a").text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "page/" + str(el) + "/"
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

def choixScrap (origin):
    site = "http://choix.ma/store/"
    page = getAllPage()
    produits = []

    for url in page:
        req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        parsed_page = soup(page_html, "html.parser")

        logo = "http://137.74.199.121/img/logo/ma/choixma.jpg"
        logoS = "http://137.74.199.121/img/logo/ma/logoS/choixma.jpg"

        try:
            products_container = parsed_page.find_all("li", {"class":"type-product"})

            for elem in products_container:
                product_img = elem.find_all("img", {"class":"attachment-shop_catalog size-shop_catalog wp-post-image"})[0].get("src")
                product_name = elem.find_all("div", {"class":"shop_items_text_holder"})[0].find_all("h3")[0].text.strip()
                product_url = elem.find_all("div", {"class":"shop_items_text_holder"})[0].find_all("a")[0].get("href")
                product_desc = elem.find_all("div", {"class":"shop_items_text_holder"})[0].find_all("a", {"class":"product_category_title"})\
                [0].text.strip()
                try:
                    product_price = int(elem.find_all("span", {"class":"price"})[0].find_all("ins")[0].\
                    find_all("span", {"class":"amount"})[0].text.strip().replace(u',', '').replace(u'.', ''))
                except:
                    product_price = 0
                    pass


                produits.append({
                'libProduct': product_name,
                'slug':'',
                'descProduct': product_desc,
                'priceProduct': product_price,
                'imgProduct': product_img,
                'numSeller':'',
                'src': site,
                'urlProduct': product_url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                'country':'ma'
                })

        except:
            continue

    return produits

"""produits = choixScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())"""

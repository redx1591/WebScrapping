from bs4 import BeautifulSoup
import requests


def category2arly():
    site = "http://www.2arly.com/categorie-produit/2arly-co-informatique/"

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find("section",{"id":"woocommerce_product_categories-5"}).find("ul",{"class":"product-categories"}).findAll("ul",{"class":"children"})

    categories_urls = []

    for item in category:
        subcategory = item.findAll("li")

        for el in subcategory:
            catUrl = el.find("a").get("href")
            catName = el.find("a").text

            categories_urls.append({
            "url":catUrl,
            "name":catName
            })

    return categories_urls

#print(category2arly())


def getAllPage():

    subUrl = category2arly()
    page = []

    for url in subUrl:
        page_response = requests.get(url['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(
                    page_content.find('nav', {"class":"woocommerce-pagination"}).findAll('li')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url['url'] + "page/" + str(el)

                page.append({
                    'url': link,
                    'name': url['name']
                })
        except:

            link1 = url['url']

            page.append({
                'url': link1,
                'name': url['name']
            })

    return page

#print(getAllPage())

def scrap2ary(origin):
    site = "http://www.2arly.com/"
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")
            logo = 'http://137.74.199.121/img/logo/sn/2arly.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/2arly.jpg'

            products = page_content.find("main",{"id":"main"}).find("ul",{"class":"products"}).findAll("li")
        except:
            continue


        for item in products:
            try:
                url = item.find("div",{"class":"product-item-details"}).find('a').get("href")
                lib = item.find("div",{"class":"product-item-details"}).find('a').text.strip()
                img = item.find('div', {"class": "product-item"}).find("img").get("src")
                try:
                    prix = int(item.find("span", {"class": "price"}).text.replace(",00CFA","").replace(".",""))
                except:
                    prix = 0

                produits.append({
                    'libProduct': lib,
                    'slug': '',
                    'descProduct': '',
                    'priceProduct': prix,
                    'imgProduct': img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': url,
                    'logo': logo,
                    'logoS': logoS,
                    'origin': origin,
                    "country": "sn",
                    "subcategory": link['name']
                })
            except:
                continue

    return produits

produit = scrap2ary(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produit:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

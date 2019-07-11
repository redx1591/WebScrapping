from bs4 import BeautifulSoup
import requests

def categoryNovaSn():
    url = "https://nova.sn/12-homme"
    page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    categories = page_content.find('div',{"class":"left-categories"}).findAll('li',{"data-depth":"0"})

    categories_urls = []

    for item in categories[0:-1]:
        urlCategory = item.find('a').get("href")
        nameCategory = item.find('a').text

        categories_urls.append({
            'url':urlCategory,
            'name':nameCategory
        })

    return categories_urls

#print(categoryNovaSn())

def subCategoryNovaSn():
    categoy_url = categoryNovaSn()
    subUrl = []

    for url in categoy_url:
        page_response = requests.get(url["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subcategory = page_content.find('div',{"class":"subcategories-wrapper"}).findAll('h5',{"class":"subcategory-name"})

        for item in subcategory:
            url = item.find('a').get("href")
            name = item.find('a').text

            subUrl.append({
                'url':url,
                'name':name
            })
    return subUrl

#print(subCategoryNovaSn())


def getAllPage():

    categories_urls = subCategoryNovaSn()
    page = []

    for url in categories_urls:
        page_response = requests.get(url['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(
                page_content.find('ul', {"class": "page-list"}).findAll('a')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url['url'] + "?page=" + str(el)
                page.append({
                    'url': link,
                    'name':url['name']
                })
        except:
            link1 = url['url']

            page.append({
                'url': link1,
                'name': url['name']
            })

    return page

#print(getAllPage())

def novaSnScrap(origin):
    site = "https://www.nova.sn"
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            products_container = page_content.find("div", {"class":"product-list"}).findAll('article',{"class":"product-miniature"})

            logo = 'http://137.74.199.121/img/logo/sn/novs.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/nova.jpg'
        except:
            continue

        for elem in products_container:
            try:
                product_img = elem.find_all("div", {"class":"product-thumbnail"})[0].find_all("a", {"class":"product-cover-link"})[0].find_all("img")[0].get("src")
                product_name = elem.find_all("div", {"class":"second-block"})[0].find_all("h5", {"class":"product-name"})[0].find_all("a")[0].text.strip()
                product_url = elem.find_all("div", {"class":"product-thumbnail"})[0].find_all("a", {"class":"product-cover-link"})[0].get("href")
                try:
                    product_price = elem.find_all("div", {"class":"first-prices d-flex flex-wrap align-items-center"})[0].find_all("span", {"class":"price product-price"})[0].get("content")
                except:
                    product_price = 0

                produits.append({
                    'libProduct':product_name,
                    'slug': '',
                    'descProduct': '',
                    'priceProduct': product_price,
                    'imgProduct': product_img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': product_url,
                    'logo': logo,
                    'logoS': logoS,
                    'origin': origin,
                    "country": "sn",
                    "subcategory": link['name']
                })
            except:
                continue

    return produits

#print(novaSnScrap(origin=0))

"""INSERTION DES PRODUITS"""

produits = novaSnScrap(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass
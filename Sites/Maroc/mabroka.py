from bs4 import BeautifulSoup
import requests

def categoryMabroka():
    url = 'https://www.mabroka.ma/fr'
    page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    categories = page_content.findAll('div',{"class":"col-xs-6"})

    categories_urls = []


    for item in categories:
        try:
            urlCategory = 'https://www.mabroka.ma'+item.find('a').get("href")
        except:
            continue

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryMabroka())

def subCategoryMabroka():
    categories_urls = categoryMabroka()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('div',{"class":"body"}).findAll('a',{"class":"sub-cat"})

        for item in subCategories:
            subCategoryUrl = 'https://www.mabroka.ma'+ item.get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryMabroka())

def getAllPage():
    subUrl = subCategoryMabroka()
    page = []

    for url in subUrl:
        try:
            maxPage = 5
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?page=" + str(el)
                page.append(
                    link
                )
        except:

            link1 = url
            page.append(
                link1
            )

    return page

print(getAllPage())

def mabrokaScrap(origin):
    site = "https://www.mabroka.ma/"
    page = getAllPage()
    produits = []

    for url in page :
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            products_container = page_content.find_all("div", {"class":"row ad"})
            logo = "http://137.74.199.121/img/logo/ma/mabroka.jpg"
            logoS= "http://137.74.199.121/img/logo/ma/logoS/mabroka.jpg"

            for elem in products_container:
                try:
                    product_img = elem.find_all("img", {"class":" img-responsive"})[0].get("src").strip()
                except:
                    product_img = ""
                product_name = elem.find_all("h3")[0].find_all("a")[0].text.strip()
                product_url = elem.find_all("h3")[0].find_all("a")[0].get("href")
                try:
                    product_price = int(elem.find_all("span", {"class":"price"})[0].text.replace(u' ', '').replace(u',', '').replace(u'DH', '').strip())
                except:
                    product_price = 0
                    pass


                produits.append({
                    'libProduct': product_name,
                    'slug':'',
                    'descProduct': '',
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

"""produits = mabrokaScrap(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())
    except:
        continue"""


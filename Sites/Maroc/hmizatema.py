from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests

def categoryHmizatema():
    url = 'http://mall.hmizate.ma/'
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    urlopen(req).close()
    parsed_page = soup(page_html, "html.parser")

    categories = parsed_page.find('div',{"id":"dropdown_507"}).findAll('li')
    categories_urls = []

    for item in categories[1:-1]:
        try:
            urlCategory = item.find('a',{"class":"ty-menu__item-link"}).get("href")
        except:
            continue

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryHmizatema())

def getAllPage():
    subUrl = categoryHmizatema()
    page = []

    for url in subUrl:
        req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        parsed_page = soup(page_html, "html.parser")

        try:
            maxPage = int(
                parsed_page.find('div', {"class": "ty-pagination__items"}).findAll('a',{"class":"cm-history"})[-1].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "page-" + str(el) + "/"
                page.append({
                    'url': link
                })
        except:

            link1 = url
            page.append({
                'url': link1
            })

    return page

#print(getAllPage())


def scrapHmizate(origin):
    page = getAllPage()
    produits = []
    site = 'http://mall.hmizate.ma'

    for link in page:
        req = Request(link["url"], headers={'User-agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()

        parsed_page = soup(page_html, "html.parser")
        products_container = parsed_page.find_all("div", {"class":"ty-grid-body"})
        logo = "http://137.74.199.121/img/logo/ma/hmizatemall.jpg"
        logoS = "http://137.74.199.121/img/logo/ma/logoS/hmizatemall.jpg"

        for elem in products_container:
            try:
                product_name = elem.find_all("a", {"class":"product-title"})[0].get("title")
                product_img = elem.find_all("img", {"class":"ty-pict cm-image"})[0].get("src").strip()
                product_url = elem.find_all("a", {"class":"product-title"})[0].get("href")
                try:
                    product_price = int(elem.find_all("span", {"class":"ty-price-num"})[0].text.strip().replace(',', ''))
                except:
                    product_price = 0

                produits.append({
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
                'country':'ma'
                })
            except:
                pass

    return produits

"""produits = scrapHmizate(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())"""



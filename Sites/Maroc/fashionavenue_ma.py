from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests

def categoryFashion():
    url = 'http://fashionavenue.ma/index.php/'
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    urlopen(req).close()
    parsed_page = soup(page_html, "html.parser")

    categories = parsed_page.find('ul',{"id":"nav"}).findAll('li',{"class":"level0"})

    categories_urls = []

    for item in categories[0:-1] :
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryFashion())

def subCategoryFashion():
    categories_urls = categoryFashion()
    subUrl = []

    for el in categories_urls:
        req = Request(el, headers={'User-agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        parsed_page = soup(page_html, "html.parser")

        subCategories = parsed_page.find('dd').findAll('li')

        for item in subCategories:
            subCategoryUrl = item.findAll('a')[0].get("href") + "&limit=all"

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryFashion())

def fashionScrap (origin):
    site = "http://fashionavenue.ma/"
    subUrls = subCategoryFashion()
    produits = []

    for url in subUrls :
        req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        parsed_page = soup(page_html, "html.parser")

        logo = "http://137.74.199.121/img/logo/ma/fashionavenue.jpg"
        logoS = "http://137.74.199.121/img/logo/ma/logoS/fashionavenue.jpg"

        try:
            products_container = parsed_page.find_all("li", {"class":"item"})


            for elem in products_container:
                product_img = elem.find_all("a", {"class":"product-image"})[0].find_all("img")[0].get("src")
                product_name = elem.find_all("a", {"class":"product-image"})[0].get("title")
                product_url = elem.find_all("a", {"class":"product-image"})[0].get("href")
                product_desc = elem.find_all("div", {"class":"desc_grid"})[0].text.strip().replace('\n','').replace('\xa0','').replace('\r','')
                try:
                    product_price = int(elem.find_all("span", {"class":"price"})\
                    [0].text.replace(u' ', '').replace(u',', '').replace(u'Dhs', '').strip())
                except:
                    product_price = 0

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

"""produits = fashionScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())"""
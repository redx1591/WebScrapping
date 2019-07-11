from bs4 import BeautifulSoup
import requests

def categoryCoinAfrique():
    site = "https://sn.coinafrique.com"
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"categorires-list-container"}).findAll('li',{"class":"category"})

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

    site = "https://sn.coinafrique.com"

    for url in categories_urls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        element = page_content.find('div',{"class":"sub-categories-box"}).findAll('li',{"class":"category"})

        for item in element:
            subCategoryUrl = site + item.find("a").get("href")
            subCategoryName = item.find("a").text

            subUrl.append({
                'url':subCategoryUrl,
                'name': subCategoryName
            })

    return subUrl

#print(subcategoryCoinAfrique())

def getAllPage():
    subUrl = subcategoryCoinAfrique()
    page = []
    maxPage = 9
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url['url'] + "?page=" + str(item)
            page.append({
                'url': link,
                'name':url['name']
            })
    return page

#print(getAllPage())

def coinAfriqueComScrap(origin):
    site = "https://sn.coinafrique.com"
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")
            products_container = page_content.find_all("div", {"class":"card round"})

            logo = 'http://137.74.199.121/img/logo/sn/coinafrique.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/coinafrique.jpg'
        except:
            continue

        for elem in products_container:
            try:
                product_img = elem.find_all("div", {"class":"card-image waves-effect waves-block waves-light"})[0].find_all("a")[0].find_all("img")[0].get("src")
                product_name = elem.find_all("div", {"class":"card-content"})[0].find_all("p", {"class":"card-desc"})[0].find_all("a")[0].text.strip()
                product_url = elem.find_all("div", {"class":"card-content"})[0].find_all("p", {"class":"card-desc"})[0].find_all("a")[0].get("href")
                product_url = site + product_url

                try:
                    product_price = int(elem.find_all("div", {"class":"card-content"})[0].find_all("p")[0].text.replace(u'\xa0','').replace(u'CFA', '').replace(u' ','').strip())
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
                    "country": "sn",
                    "subcategory":link["name"]
                })
            except:
                continue

    return produits

#print(coinAfriqueComScrap(origin=1))


"""INSERTION DES PRODUITS"""

produits = coinAfriqueComScrap(origin=1)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass


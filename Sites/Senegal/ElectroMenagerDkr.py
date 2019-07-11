from bs4 import BeautifulSoup
import requests

def categoryElectroMenagerDkr():

    site = 'https://www.electromenager-dakar.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    links = page_content.findAll('div',{"class":"product-category"})
    data = []
    categories_urls = []

    for link in links:
        url = link.find('a').get("href")

        data.append(
            url
        )

    for url in data:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        category = page_content.findAll('div',{"class":"product-category"})
        for item in category:
            urlCategory = item.find('a').get("href")

            categories_urls.append(
                urlCategory
            )

    return categories_urls

#print(categoryElectroMenagerDkr())

def subcategoryElectroMenagerDkr():

    categories_urls = categoryElectroMenagerDkr()
    subUrl = []

    for url in categories_urls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subcategoy = page_content.findAll('div',{"class":"product-category"})

        for item in subcategoy:
            subCategoryUrl = item.find('a').get("href")
            subCategoryName = item.find('a').find('h5').text

            subUrl.append({
                'url' : subCategoryUrl,
                'name': subCategoryName
            })

    return subUrl

#print(subcategoryElectroMenagerDkr())

def getAllPage():

    subUrl = subcategoryElectroMenagerDkr()
    page = []

    for url in subUrl:
        page_response = requests.get(url['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('nav', {"class": "woocommerce-pagination"}).findAll('li')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url['url'] + "page/" + str(el)
                page.append({
                    'url': link,
                    'name':url['name']
                }
                )
        except:

            link1 = url["url"]
            page.append({
                'url': link1,
                'name':url['name']
            }
            )

    return page

#print(getAllPage())

def scrapElectroMenagerDkr(origin):

    site = 'https://www.electromenager-dakar.com/'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/sn/electromenager.jpg'
        logoS = 'http://137.74.199.121/img/logo/sn/logoS/electromengerdakar.jpg'

        try:
            annonce = page_content.findAll("div", {"class": "box"})
        except:
            continue


        for item in annonce:
            try:
                url = item.find("div", {"class": "box-text"}).find('p', {"class": "name"}).find("a").get("href")
                lib = item.find("div", {"class": "box-text"}).find('p', {"class": "name"}).text
                img = item.find("div", {"class": "box-image"}).find('a').find('img').get("data-lazy-src")
                try:
                    prix = int(item.find("div", {"class": "box-text"}).find('span', {"class": "price"}).text.replace(u'.','').replace(u'CFA', ''))
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
                'urlProduct': url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                "country": "sn",
                "subcategory":link["name"]
                })

            except:
                continue

    return produits

#print(scrapElectroMenagerDkr(origin=0))


"""INSERTION DES PRODUITS"""

produits = scrapElectroMenagerDkr(origin=0)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

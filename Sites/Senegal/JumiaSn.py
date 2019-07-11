from bs4 import BeautifulSoup
import requests


def categoryJumia():

    site = 'https://www.jumia.sn/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"flyout-w"}).findAll("a",{"class":"itm"})

    categories_urls = []

    for item in category:
        urlCategory = "https://www.jumia.sn" + str(item.get("href"))

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryJumia())

def subcategoryJumia():
    categories_urls = categoryJumia()
    subCat = []

    for url in categories_urls:
        try:
            page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")
        except:
            continue

        try:
            subCategories = page_content.find('ul', {"class": "osh-subcategories"}).findAll('li',{"class": "osh-subcategory"})

            for item in subCategories:
                subCategoryName = item.find('a').find('span', {"class": "-name"}).text
                subCategoryUrl = item.find('a').get("href")

                subCat.append({
                'url':subCategoryUrl,
                'name':subCategoryName
                })
        except:
            continue

    return subCat

#print(subcategoryJumia())


def getAllPage():
    subCat = subcategoryJumia()
    page = []

    for item in subCat:
        page_response = requests.get(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            maxPage = int(page_content.find('section',{"class":"pagination"}).findAll('li',{"class":"item"})[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = item['url'] + "?page=" + str(el)
                name = item['name']
                page.append({
                    'url': link,
                    'name':name
                }
                )
        except:
            link1 = item['url'] + "?page=" + str(el)
            name1 = item['name']
            page.append({
                'url': link1,
                'name':name1
            })

    return page

#print(getAllPage())

def jumiaScrap(origin):

    site = 'https://www.jumia.sn'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = 'http://137.74.199.121/img/logo/sn/jumia.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/Jumia.jpg'

            annonce = page_content.findAll('a', {"class": "link"})
        except:
            continue

        for item in annonce:
            try:
                url = item.get("href")
                lib = item.find_all("span", {"class": "name"})[0].text.strip()
                img = item.find("div",{"class":"image-wrapper"}).find_all("img")[0].get('data-src')
                try:
                    prix = int(item.find_all("div", {"class":"price-container clearfix"})[0].find_all("span", {"class":"price"})[0].find_all("span")[0].get("data-price"))
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
                'subcategory': link['name'],
                })


            except:
                continue

    return produits

#print(jumiaScrap(origin=0))

"""INSERTION DES PRODUITS"""

produits = jumiaScrap(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

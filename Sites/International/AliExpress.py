from bs4 import BeautifulSoup
import requests


"""Fontion pour récupérer les urls de toutes les catégories """
def categoryAliExpress():

    site = 'https://fr.aliexpress.com/?spm=a2g0w.10010108.100004.1.5b464880cJYUyZ'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")
    try:
        category = page_content.find('div',{"class":"categories-list-box"}).findAll('dl',{"class":"cl-item"})

        categories_urls = []

        for item in category:
            urlCategory = item.find('a').get("href").replace('//','https://')

            categories_urls.append(
                urlCategory

            )
    except:
        pass

    return categories_urls

print(categoryAliExpress())

def subcategoryAliExpress():
    categories_urls = categoryAliExpress()
    subCat = []

    for url in categories_urls[0:1]:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        subCategories = page_content.find('dl', {"class": "son-category"}).find('ul').findAll('li')
        print(subCategories)

        """try:
            subCategories = page_content.find('dl', {"class": "son-category"}).find('ul').findAll('li')

            for item in subCategories:
                subCategoryName = item.find('a').text
                subCategoryUrl = item.find('a').get("href").replace('//','https://')

                subCat.append({
                'url':subCategoryUrl,
                'name':subCategoryName
                })
        except:
            continue"""

    return subCat

print(subcategoryAliExpress())

def getAllPage():
    subCat = subcategoryAliExpress()
    page = []

    for item in subCat:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        page.append({
            "url":item["url"],
            "name":item["name"]
        })

        try:
            pageLink = page_content.find('div', {"class": "ui-pagination-navi"}).findAll("a")

            for elm in pageLink[0:-1]:
                url = elm.get("href").replace('//','https://')

                page.append({
                    "url":url,
                    "name":item["name"]
                })

        except:
            continue
    return page

#print(getAllPage())



def getUrl():
    page = getAllPage()
    url = []

    for item in page:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            productLink = page_content.find('div',{"id":"list-items"}).findAll("li",{"class":"list-item"})

            for el in productLink :
                urlLink = el.find("h3").find('a').get("href").replace('//','https://')

                url.append({
                    'url':urlLink,
                    'category': item["name"]
                })

        except:
            continue

    return url

#print(getUrl())

def scrapAliExpress(origin):
    site = "https://fr.aliexpress.com/?spm=a2g0w.search0203.2.1.5f3e72d1LlaqHu"
    url = getUrl()
    produits = []

    for item in url[0:1]:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ali.jpg"
        logoS = "http://137.74.199.121/img/logo/aliS.jpg"

        annonce = page_content.find('div',{"id":"j-detail-page"})
        try :
            name = annonce.find("h1",{"class":"product-name"}).text.strip()
            url = item["url"]
            img = annonce.find('div',{"class":"ui-image-viewer-thumb-wrap"}).find("img").get("src")
            poids = annonce.find('ul',{"class":"product-packaging-list"}).findAll("li",{"class":"packaging-item"})[1].find("span",{"class":"packaging-des"}).text

            try:
                prix = int(float(annonce.find('div',{"class":"p-price-content"}).find('span',{"class":"p-price"}).text.strip().replace(',','.')) * 656.07)
            except:
            #prix = int(float(annonce.find('div',{"class":"p-price-content"}).find('span',{"class":"p-price"}).find('span',{"itemprop":"highPrice"}).text.strip().replace(',','.')) * 656.07)
                prix = 0
            produits.append(
            {
                'libProduct': name,
                'slug': '',
                'size': poids,
                'priceProduct': prix,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': url,
                'logo': logo,
                'logoS': logoS,
                'origin': origin,
                "country": "ali",
                'subcategory': item['category'],
            })

        except:
            continue

    return produits

#print(scrapAliExpress(origin=0))

produits = scrapAliExpress(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())
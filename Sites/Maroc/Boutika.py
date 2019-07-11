from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """
def categoryBoutika():
    site = 'https://www.boutika.co.ma/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category_urls = page_content.find('ul', {"class": "nav"}).findAll("li", {"class": "parent"})
    categories_urls = []

    for item in category_urls:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    url1 = 'https://www.boutika.co.ma/8-tv-home-cinema'
    url2 = 'https://www.boutika.co.ma/226-photo-et-video'

    categories_urls.append(url1)
    categories_urls.append(url2)

    return categories_urls

#print(categoryBoutika())

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""
def subCategoryUrl():
    categories_urls = categoryBoutika()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.findAll('div', {"class": "subcategories"})

        for item in subCategories:
            subCategoryUrl = item.find('h5', {"class": "cat-name"}).findAll('a')[0].get("href") + "#"

            subUrl.append(
                    subCategoryUrl
            )

    return subUrl

#print(subCategoryUrl())


"""Fonction pour récupérer les informations de tous les produits """
def scrapBoutika(origin):

    site = 'https://www.boutika.co.ma/'
    subUrls = subCategoryUrl()
    produits = []

    for url in subUrls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ma/boutika.jpg'
        logoS = 'http://137.74.199.121/img/logo/ma/logoS/boutika.jpg'

        annonce = page_content.find_all("div", {"class": "product-container"})

        for item in annonce:
            try:
                url = item.findAll('h2', {"class": "name"})[0].find_all("a")[0].get("href")
                lib = item.find_all("h2", {"class": "name"})[0].text.strip()
                img = item.find_all("img")[0].get('src')
                desc = item.find_all('div', {"class": "product-desc"})[0].text.strip().replace('\xa0','')


                try:
                    prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace(u' ', '').replace(u'Dhs', ''))
                except:
                    prix=0

                produits.append(
                {
                    'libProduct': lib,
                    'slug': '',
                    'descProduct': desc,
                    'priceProduct': prix,
                    'imgProduct': img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': url,
                    'logo': logo,
                    'logoS':logoS,
                    'origin': origin,
                    'country':'ma'
                })
            except:
                continue

    return produits

"""produits = scrapBoutika(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())"""



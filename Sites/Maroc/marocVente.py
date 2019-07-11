from bs4 import BeautifulSoup
import requests

"""Fonction pour récupérer les noms et les urls de toutes les catégories"""

def categoryMarocVente():

    site = 'http://marocvente.com'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('table', {"id": "My_DataList1"}).findAll("td")
    categories_urls = []

    for item in category :
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryMarocVente())


"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryMarocVente():

    categories_urls= categoryMarocVente()
    subUrl = []

    site = 'http://www.marocventes.com'

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('table', {"id": "sub-categories"}).findAll('td')

        for item in subCategories:
            try:

                subCategoryUrl = site + item.find('div',{"class":"category-name"}).find('a').get("href")

                subUrl.append(
                    subCategoryUrl
                )

            except:
                continue

    return subUrl

#print(subCategoryMarocVente())

def marocVenteScrap(origin):
    site = 'http://marocvente.com'
    subUrls = subCategoryMarocVente()
    produits = []

    for url in subUrls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ma/marocvente.jpg'
        logoS = 'http://137.74.199.121/img/logo/ma/logoS/marocvente.jpg'

        annonce = page_content.findAll('div', {"class": "product-line"})

        for item in annonce:
            try:
                url =  site + item.find_all('p')[0].find_all('a')[0].get("href")
                lib = item.find_all('div', {"class": "right-list"})[0].find_all('p')[0].text.strip()
                img = site + item.find_all("img")[0].get('src')
                desc = item.find_all('div', {"class": "right-list"})[0].find_all('p')[4].text.strip().replace('\n',' ')
                try:
                    prix = int(float(
                    item.find_all("p", {"class": "your-price"})[0].text.strip().replace(u'Votre Prix :', '').replace(
                        u' Dh TTC', '').replace(u' ', '').replace(u',', '.')))
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
                }
                )

            except:
                continue

    return produits

produits = marocVenteScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())




from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct,insertSubCat,insertCat


"""Fontion pour récupérer les urls de toutes les catégories """
def categoryBoutika():
    site = 'https://www.boutika.co.ma/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category_names = page_content.find('ul', {"class": "nav"}).findAll("li", {"class": "parent"})
    category_urls = page_content.find('ul', {"class": "nav"}).findAll("li", {"class": "parent"})

    categories_urls = []
    categories_names = []

    compteur = 0

    for item in category_urls:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    url1 = 'https://www.boutika.co.ma/8-tv-home-cinema'
    url2 = 'https://www.boutika.co.ma/226-photo-et-video'

    categories_urls.append(url1)
    categories_urls.append(url2)

    for item in category_names:
        urlName = item.find('a').find('span', {"class": "menu-title"}).text
        categories_names.append({
            'id': 0,
            'libCategory': urlName
        })

    categories_names.append({'id':0,'libCategory':"Téléviseurs / Son & HIFI"})
    categories_names.append({'id':0,'libCategory':"Photo et video"})

    while compteur < len(categories_names):
        categories_names[compteur]["id"] = compteur
        compteur = compteur + 1

    return categories_urls,categories_names



"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""
def subCategoryUrl():
    categories_urls, categories_names = categoryBoutika()

    '''A ajouter'''
    subName = []
    subUrl = []

    compteur = len(categories_names)
    i = 0

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.findAll('div', {"class": "subcategories"})

        for item in subCategories:
            subCategoryName = item.find('h5', {"class": "cat-name"}).findAll('a')[0].text
            subCategoryUrl = item.find('h5', {"class": "cat-name"}).findAll('a')[0].get("href") + "#"

            subUrl.append(
                    subCategoryUrl
            )

            '''A ajouter '''
            subName.append({
                'id':compteur,
                'libSubCategory': subCategoryName,
                'category_id': categories_names[i]["id"]
            })
            compteur = compteur + 1

        i = i + 1

    return subUrl,subName



"""Fonction pour récupérer les informations de tous les produits """
def scrapBoutika(origin):

    site = 'https://www.boutika.co.ma/'
    subUrls, subName = subCategoryUrl()
    i = 0
    produits = []

    for url in subUrls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = page_content.find("head").find("link", {"type": "image/jpeg"}).get("href")

        annonce = page_content.find_all("div", {"class": "product-container"})

        """try:
            subName = page_content.find('h1',{"class":"page-heading product-listing"}).text
        except:
            subName=''"""

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
                    'id': '',
                    'libProduct': lib,
                    'slug': '',
                    'descProduct': desc,
                    'priceProduct': prix,
                    'imgProduct': img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': url,
                    'logo': logo,
                    'origin': origin,
                    'subcategory_id': subName[i]["id"]
                })
            except:
                continue
        i = i + 1

    return produits




"""INSERTION DES CATEGORIES, SOUS-CATEGORIES ET DES PRODUITS"""

"""Pour les categories"""
categories_urls,categories_names = categoryBoutika()
insertCat('ibou', 'ibou', '192.168.64.4', 'linki_db', categories_names)

"""Pour les sous-categories"""
subUrls,subNames = subCategoryUrl()
insertSubCat('ibou', 'ibou', '192.168.64.4', 'linki_db', subNames)

"""Pour les produits"""
produits = scrapBoutika(origin=0)
insertProduct('ibou', 'ibou', '192.168.64.4', 'linki_db', produits)


'''"""Pour les produits"""
for el in subUrls:
    try:
        produits = scrapBoutika(url=el,origin=0)
        print(produits[0])
        insertProduct('ibou', 'ibou', '192.168.64.3', 'comparez', produits,'maroc')

    except:
        pass


'''

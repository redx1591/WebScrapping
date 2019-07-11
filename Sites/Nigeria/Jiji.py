from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryJiji():

    site = 'https://jiji.ng'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")
    #print(page_content)

    category = page_content.find('div',{"class":"b-list-category"}).findAll("h2",{"class":"b-list-category__item"})
    categories_urls = []

    for item in category[0:-1]:
        urlCategory = site + item.find('a').get("href")
        nameCategory= item.find('a').find('span',{"class":"b-list-category__item-title__name"}).text


        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryJiji())

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryJiji():
    site = 'https://jiji.ng'
    categories_urls = categoryJiji()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        #print(page_content)
        try :
            subCategories = page_content.find('div', {"class": "b-list-subcategory"}).findAll('h2',{"class":"b-list-subcategory__item"})

            for item in subCategories:
                subCategoryUrl = site + item.find('a').get("href")

                subUrl.append(
                subCategoryUrl
                )

        except:
            pass

    return subUrl
#print(subCategoryJiji())

def getAllPage():
    subUrl  = subCategoryJiji()
    page = []
    maxPage = 9
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url + "/page" + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())


def jijiScrap(origin):
    site = 'https://jiji.ng'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ng/jiji.jpg'
        logoS = 'http://137.74.199.121/img/logo/ng/logoS/jiji.jpg'

        annonce = page_content.findAll('div', {"class": "b-list-advert__item"})



        for item in annonce:
            try:
                url = item.find('a',{"class":"b-list-advert__item-image"}).get("href")
                lib = item.find_all("h4", {"class": "b-list-advert__item-title"})[0].text.strip()
                img = item.find('a',{"class":"b-list-advert__item-image"}).find_all("img")[0].get('src')
                try:
                    prix = int(item.find_all("p", {"class": "b-list-advert__item-price"})[0].text.strip().replace(',','').replace('₦',''))
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
                'country':'ng',
                }
                )

            except:
                continue

    return produits


produits = jijiScrap(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())
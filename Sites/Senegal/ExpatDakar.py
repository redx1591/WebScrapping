from bs4 import BeautifulSoup
import requests


def subcategoryExpatDakar():

    subUrl = []
    site = 'https://www.expat-dakar.com'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find("div",{"class":"top-categories-container"}).findAll('div',{"class":"col-sm-3"})

    for el in category :
        url = el.findAll('li',{"class":"fleft"})

        for item in url :
            try:
                subCategoryUrl = item.find('a',{"class":"link-relatedcategory"}).get("href")
                subCategoryName = item.find('a',{"class":"link-relatedcategory"}).text.strip()
            except:
                continue

            subUrl.append({
                'url':subCategoryUrl,
                'name':subCategoryName
            })

    return subUrl

#print(subcategoryExpatDakar())

def getAllPage():
    subUrl = subcategoryExpatDakar()
    page = []
    maxPage = 6
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url['url'] + "?page=" + str(item)
            page.append({
                'url': link,
                'name': url['name']
            })
    return page


def scrapExpatDakar(origin):

    site = 'https://www.expat-dakar.com'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = 'http://137.74.199.121/img/logo/sn/expat.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/expat.jpg'
            annonce = page_content.findAll("div",{"class": "listing-card"})
        except:
            continue

        for item in annonce:
            try:
                url = item.find("div",{"class":"listing-details-content"}).find("h2").find("a").get("href")
                lib = item.find("div",{"class":"listing-details-content"}).find("h2").text.strip().replace('\t','').replace('\n','-')
                img = item.find("div", {"class": "listing-thumbnail"}).find("img").get("data-src")
                desc = item.find('div', {"class": "description-block"}).text.strip()

                try:
                    prix = int(item.find("span", {"class": "prix"}).text.replace(' ','').replace('FCFA',''))
                except:
                    prix=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': desc,
                'priceProduct': prix,
                'imgProduct': site + img,
                'numSeller': '',
                'src': site,
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                "country": "sn",
                "subcategory":link['name']
                })

            except:
                continue

    return produits

#print(scrapExpatDakar(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapExpatDakar(origin=1)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

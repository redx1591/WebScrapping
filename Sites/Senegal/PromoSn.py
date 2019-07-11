from bs4 import BeautifulSoup
import requests

def subcategoryPromoSn():

    subUrl = []

    site = 'https://www.promo.sn/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subcategory = page_content.findAll('ul',{"class":"nav-level2"})

    for item in subcategory:
        element = item.findAll('li')

        for el in element :
            subCategoryUrl = el.find('a').get("href")
            subCategoryName = el.find('a').text
            subUrl.append({
                'url':subCategoryUrl,
                'name':subCategoryName
            })

    return subUrl

#print(subcategoryPromoSn())

def getAllPage():
    subUrl = subcategoryPromoSn()
    page = []

    for url in subUrl:
        page_response = requests.get(url["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('ul',{"class": "page-numbers"}).findAll('li')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url["url"] + "page/" + str(el)

                page.append({
                    'url': link,
                    'name':url['name']
                })
        except:

            link1 = url["url"]

            page.append({
                'url': link1,
                'name':url['name']
            })

    return page

#print(getAllPage())

def scrapPromoSn(origin):

    site = 'https://www.promo.sn/'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = 'http://137.74.199.121/img/logo/sn/promosn.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/promosn.jpg'
            annonce = page_content.findAll("li", {"class": "item"})
        except:
            continue

        for item in annonce:
            try:
                url = item.find("div", {"class": "item-detail"}).findAll('a')[0].get("href")
                lib = item.find("div", {"class": "item-content"}).findAll('h4')[0].find('a').text
                img = item.find("div", {"class": "item-detail"}).findAll('a')[0].find("img").get("src")
                try:
                    prix = int(
                    item.findAll("span", {"class": "item-price"})[0].findAll('span')[0].text.replace(u' ', '').replace(
                        u'CFA', '').replace(u'.', ''))
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
                "subcategory":link['name']
                })

            except:
                continue

    return produits

#print(scrapPromoSn(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapPromoSn(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass


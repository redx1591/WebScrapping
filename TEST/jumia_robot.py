from bs4 import BeautifulSoup
import requests


def getAllPage():
    subCat = "https://www.jumia.sn/jeux-videos-consoles/?q=jeux"
    page = []

    page_response = requests.get(subCat, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")
    try:
        maxPage = int(page_content.find('section',{"class":"pagination"}).findAll('li',{"class":"item"})[-2].text) + 1
        id = list(range(maxPage))
        del id[0]

        for el in id:
            link = subCat + "&page=" + str(el)
            name = "manettes"
            page.append({
                'url': link,
                'name':name
            }
            )
    except:
        link1 = subCat + "&page=" + str(el)
        name1 = "manette"
        page.append({
            'url': link1,
            'name':name1
        })

    return page

print(getAllPage())

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
                "custom_category_id": 27
                })


            except:
                continue

    return produits

#print(jumiaScrap(origin=0))

"""INSERTION DES PRODUITS"""

produits = jumiaScrap(origin=0)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

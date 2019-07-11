from bs4 import BeautifulSoup
import requests

def subCategoryDecathlon():

    site = 'https://www.decathlon.ma/'
    subUrl = []

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"menu-categories"}).findAll("li")

    for item in category:
        try:
            subCategory = item.find("ul").findAll("a",{"class":"js-search"})

            for el in subCategory:
                urlCategory = el.get("href")

                subUrl.append(
                urlCategory
                )

        except:
            continue


    return subUrl

#print(subCategoryDecathlon())


def getAllPage():

    subUrl= subCategoryDecathlon()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(
                page_content.find('ul', {"class": "pagination"}).findAll('a')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?p=" + str(el)
                page.append(
                    link
                )
        except:

            link1 = url
            page.append(
                link1
            )

    return page

def scrapDecathlon(origin):

    site = 'https://www.decathlon.ma/'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ma/deccathlon.jpg'
        logoS = 'http://137.74.199.121/img/logo/ma/logoS/deccathlon.jpg'

        annonce = page_content.findAll('div', {"class": "box-product__container"})

        for item in annonce:
            try:
                url = item.find_all('a', {"class": "product-name"})[0].get("href")
                lib = item.find_all('a', {"class": "product-name"})[0].text.strip()
                img = item.find_all("img")[0].get('src')

                try:
                    prix = int(item.find_all("div", {"class": "sticker-price"})[0].text.strip().replace(u' ', '').replace(u'Dhs',''))
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
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                'country':'ma'
                }
                )

            except:
                continue

    return produits

"""produits = scrapDecathlon(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    print(response.json())"""





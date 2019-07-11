from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryPayPorte():

    site = 'https://fashion.payporte.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")
    category = page_content.find('ul',{"class":"top-navigation"}).findAll("li",{"class":"level-top"})
    categories_urls = []

    for item in category[0:-2]:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryPayPorte())

def getAllPage():
    subUrl = categoryPayPorte()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('div',{"class":"pages"}).findAll('li')[-2].text) + 1
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
#print(getAllPage())


def PayPorteScrap(origin):
    site = 'https://fashion.payporte.com/'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ng/payporte.jpg"
        logoS = "http://137.74.199.121/img/logo/ng/logoS/payporte.jpg"

        annonce = page_content.find('ul',{"class":"products-grid"}).findAll('li', {"class": "item"})


        for item in annonce:
            try:
                url = item.find_all('h3',{"class":"product-name"})[1].find('a').get("href")
                lib = item.find_all('h3',{"class":"product-name"})[1].find('a').text.strip()
                img = item.find_all("img")[0].get('data-srcx2')
                try:
                    prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace('GH₵','').replace('.00',''))
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
                'country':'ng'
                }
                )

            except:
                continue

    return produits

produits = PayPorteScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())
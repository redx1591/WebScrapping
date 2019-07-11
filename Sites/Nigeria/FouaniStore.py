from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryFouani():

    site = 'https://www.fouanistore.com'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"id":"vmenu_40"}).findAll("li",{"class":"adropdown-vertical_li"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryFouani())


def getAllPage():
    subUrl = categoryFouani()

    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            maxPage = int(page_content.find('div',{"class":"pagination-bottom"}).findAll('a')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "page-" + str(el)

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


def fouaniScrap(origin):
    site = 'https://www.fouanistore.com/'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ng/fouanigroup.jpg"
        logoS = "http://137.74.199.121/img/logo/ng/logoS/fouanigroup.jpg"

        annonce = page_content.find('div',{"class":"vs-grid-table-wrapper"}).findAll('div', {"class": "ty-column4"})


        for item in annonce:
            try:
                url = item.find('div',{"class":"title-price-wrapper"}).find('a').get("href")
                lib = item.find('div',{"class":"title-price-wrapper"}).find('a').text.strip()
                img = item.find('div',{"class":"scroll-image"}).find("img").get('data-src')
                try:
                    prix = int(item.find("span", {"class": "price"}).text.strip().replace(',','').replace('₦',''))
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
                'country':'ng'
                }
                )

            except:
                continue

    return produits

#print(fouaniScrap(origin=1))

produits = fouaniScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())
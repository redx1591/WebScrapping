from bs4 import BeautifulSoup
import requests

def categoryKara():
    site = 'http://www.kara.com.ng/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul', {"id": "navigationpro-top"}).findAll("li", {"class": "level0"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryKara())


def getAllPage():
    subUrl = categoryKara()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('div',{"class":"pager"}).findAll('li')[-2].text) + 1
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

def scrapKara(origin):
    site = 'http://www.kara.com.ng/'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ng/kara.jpg"
        logoS= "http://137.74.199.121/img/logo/ng/logoS/kara.jpg"

        annonce = page_content.find("div", {"class": "category-products"}).findAll('li', {"class": "item"})

        for item in annonce:
            try:
                url = item.find('h2', {"class": "product-name"}).find('a').get("href")
                lib = item.find('h2', {"class": "product-name"}).find('a').text
                img = item.findAll("img")[0].get("src")
                try:
                    prix = int(
                    item.find("span", {"class": "price"}).text.replace(u'.00', '').replace(u',', '').replace(u'₦', ''))
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

produits = scrapKara(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())

from bs4 import BeautifulSoup
import requests

def categoryBentigos():
    site = 'https://www.bentigos.ng'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"id":"main-nav"}).findAll('li',{"class":"dropdown"})
    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryBentigos())

def getAllPage():
    subUrl = categoryBentigos()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('div',{"id":"pagination"}).findAll('a')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?page=" + str(el)

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


def scrapBentigos(origin):
    site = 'https://www.bentigos.ng'
    page = getAllPage()
    produits = []
    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ng/bentigos.jpg"
        logoS = "http://137.74.199.121/img/logo/ng/logoS/bentigos.jpg"
        annonce = page_content.findAll("div", {"class": "product-index"})

        for item in annonce:
            try:
                url = item.find('div', {"class": "product-info"}).findAll("a")[0].get("href")
                lib = item.find('div', {"class": "product-info"}).findAll("a")[0].find("span").text
                img = item.find('div', {"class": "prod-image"}).find("img").get("src").replace(u'//', '')
                try:
                    try:
                        prix = int(
                        item.find("div", {"class": "prod-price"}).text.replace(u'.00', '').replace(u',', '').replace(
                            u'₦', ''))
                    except:
                        prix = int(
                        item.find('div', {"class": "onsale"}).text.replace(u'.00', '').replace(u',', '').replace(u'₦',
                                                                                                                 ''))
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


produits = scrapBentigos(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        continue

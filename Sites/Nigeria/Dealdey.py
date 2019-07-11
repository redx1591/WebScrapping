from bs4 import BeautifulSoup
import requests

def subcategoryDealdey():
    site = 'https://www.dealdey.com'
    subUrl = []

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subCategory = page_content.find('div',{"class":"side-menu"}).findAll('li')

    for item in subCategory:
        subCategoryUrl = site + item.find('a').get('href')

        subUrl.append(
            subCategoryUrl
        )

    return subUrl

#print(subcategoryDealdey())


def scrapDealdey(origin):

    site = 'https://www.dealdey.com/'
    subUrl = subcategoryDealdey()
    produits = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ng/dealdey.jpg'
        logoS = 'http://137.74.199.121/img/logo/ng/logoS/dealdey.jpg'
        annonce = page_content.findAll('li', {"class": "deal-detail-box"})


        for item in annonce:
            try:
                url = item.get("data-url")
                lib = item.find('div', {"class": "deal-detail"}).find("p", {"class": "deal-name"}).text
                img = item.find("figure", {"class": "img-block"}).find("a").find("img").get("src")
                try:
                    prix = int(
                    item.find('div', {"class": "deal-detail"}).find('span', {"class": "deal-price"}).text.replace(u',',
                                                                                                                  '').replace(
                        u'₦', ''))
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


produits = scrapDealdey(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())
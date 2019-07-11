from bs4 import BeautifulSoup
import requests

def subcategoryCheki():
    site = 'https://www.cheki.com.ng'
    subUrl = []

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subcategory = page_content.find('ul',{"class":"vehicleIcons"}).findAll('li')

    for item in subcategory:
        subCategoryUrl = item.find('a').get('href')

        subUrl.append(
            subCategoryUrl
        )

    return subUrl

#print(subcategoryCheki())


def getAllPage():
    subUrl = subcategoryCheki()
    page = []
    maxPage = 16
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url + "?page=" + str(item)
            page.append({
                'url': link
            })
    return page

#print(getAllPage())

def scrapCheki(origin):

    site = 'https://www.cheki.com.ng'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ng/cheki.jpg'
        logoS='http://137.74.199.121/img/logo/ng/logoS/cheki.jpg'

        annonce = page_content.find_all("li", {"class": "listing-unit"})

        for item in annonce:
            try:
                url = item.get("data-url").replace('\n','').replace('  ','')
                lib = item.find('div', {"class": "listing-unit__title"}).find("a").text.replace('\n','')
                img = item.find('div', {"class": "listing-unit__image-container"}).findAll("img")[0].get("data-lazy")
                desc = item.find('div', {"class": "listing-unit__detail-container"}).text.replace('\n','')
                try:
                    prix = int(item.find("div", {"class": "listing-unit__price"}).text.replace(u',', '').replace(u'₦', ''))
                except:
                    prix=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': desc,
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

produits = scrapCheki(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())

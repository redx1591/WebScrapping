from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryJumia():

    site = 'https://www.jumia.ma/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"menu-items"}).findAll("li",{"class":"menu-item"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")


        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryJumia())

def getAllPage():
    subUrl = categoryJumia()
    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            maxPage = int(page_content.find('section',{"class":"pagination"}).findAll('li',{"class":"item"})[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?page=" + str(el)

                page.append({
                    'url': link
                }
                )
        except:
            link1 = url
            page.append({
                'url': link1
            })

    return page

#print(getAllPage())

def jumiaScrap(origin):

    site = 'https://www.jumia.ma/'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        logo = 'http://137.74.199.121/img/logo/ma/jumia.jpg'
        logoS = 'http://137.74.199.121/img/logo/ma/logoS/jumia.jpg'
        annonce = page_content.findAll('a', {"class": "link"})

        for item in annonce:
            try:
                url = item.get("href")
                lib = item.find_all("span", {"class": "name"})[0].text.strip()
                img = item.find_all("img")[0].get('data-src')
                try:
                    prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace(u'Dhs', '').replace('\xa0',''))
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
                'country':'ma'
                }
                )
            except:
                continue

    return produits

"""produits = jumiaScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())"""








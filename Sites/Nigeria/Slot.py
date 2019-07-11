from bs4 import BeautifulSoup
import requests

"""Fontion pour récupérer les urls de toutes les catégories """

def categorySlot():

    site = 'https://slot.ng/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"id":"shop_department1"}).findAll("li",{"class":"dropdown"})
    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categorySlot())


def getAllPage():
    subUrl = categorySlot()

    page = []

    for url in subUrl:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            maxPage = int(page_content.find('nav',{"class":"woocommerce-pagination"}).findAll('li')[-2].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "page/" + str(el)

                page.append({
                    'url': link
                }
                )
        except:

            link1 = url

            page.append({
                'url': link1
            }
            )

    return page
#print(getAllPage())

def slotScrap(origin):

    site = 'https://slot.ng/'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ng/slot.jpg'
        logoS = 'http://137.74.199.121/img/logo/ng/logoS/slot.jpg'

        try:
            annonce = page_content.find('ul', {"class": "products"}).findAll('li',{"class":"product"})
        except:
            continue


        for item in annonce:
            try:
                url = item.find('h2').find('a').get("href")
                lib = item.find('h2').find('a').text.strip()
                img = item.find_all("img")[0].get('data-original')
                try:
                    prix = int(float(item.find_all("span", {"class": "price"})[0].find('span',{"class":"woocommerce-Price-amount"}).text.strip().replace(',','').replace('₦','')))
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

#print(slotScrap(origin=0))


produits = slotScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())



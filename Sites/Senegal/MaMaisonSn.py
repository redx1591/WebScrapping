from bs4 import BeautifulSoup
import requests


def categoryMaMaison():
    site = 'https://www.mamaison.sn/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"footer"}).findAll("div",{"class":"col-sm-3"})[0].findAll('li')

    categories_urls = []

    for item in category[:3]:
        urlCategory = item.find('a').get("href")
        nameCategory = item.find('a').text

        categories_urls.append({
            'url':site + urlCategory,
            'name':nameCategory
        })

    return categories_urls

#print(categoryMaMaison())


def getAllPage():
    subUrl = categoryMaMaison()
    page = []
    maxPage = 10
    id = list(range(maxPage))
    del id[0]
    for url in subUrl:
        for item in id:
            link = url['url'] + "?page=" + str(item)
            page.append({
                'url': link,
                'name':url['name']
            })
    return page

#print(getAllPage())


def scrapMaMaison(origin):

    site = 'https://www.mamaison.sn'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = 'http://137.74.199.121/img/logo/sn/mamaisonsn.jpg'
            logoS = 'http://137.74.199.121/img/logo/sn/logoS/mamaisonsn.png'
            annonce = page_content.findAll('div',{"class":"result-card-item"})
        except:
            continue

        for item in annonce:
            try:
                url = item.find("div",{"class":"carousel-inner"}).find("a",{"class":"item"}).get("href")
                lib = item.find('h2',{"class":"property-title"}).text.strip()
                img = item.find("div",{"class":"carousel-inner"}).find("a",{"class":"item"}).find("img").get('data-src')
                desc = item.find('address', {"class": "property-address"}).text.strip()

                try:
                    prix = item.find('div', {"class": "price"}).find("a", {"class": "item-price"}).text.split('FCFA')
                    prix = int(prix[0].replace('\n','').replace(' ',''))
                except:
                    prix=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': desc,
                'priceProduct': prix,
                'imgProduct': site + img,
                'numSeller': '',
                'src': site,
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                "country": "sn",
                "subcategory":link['name']
                })

            except:
                continue

    return produits

#print(scrapMaMaison(origin=0))

produits = scrapMaMaison(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass
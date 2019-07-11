from bs4 import BeautifulSoup
import requests


def categorySomef():
    site = 'https://somef.net/fr/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"container_lab_vegamenu"}).find('ul',{"class":"menu-content"}).findAll('li',{"class":"level-1"})

    categories_urls = []

    for item in category:
        urlCategory = item.find('a').get("href")
        nameCategory = item.find('a').text.strip()

        categories_urls.append({
            "url":urlCategory,
            "name":nameCategory
        })
    del categories_urls[0]

    return categories_urls

#print(categorySomef())


def subCategorySomef():

    categories_urls = categorySomef()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            subCategories = page_content.find('div', {"class": "block-categories"}).find('ul',{"class":"category-sub-menu"}).findAll('li')
            #print(subCategories)


            for item in subCategories:
                subCategoryName = item.find('a').text
                subCategoryUrl = item.find('a').get("href")

                subUrl.append({
                    'url':subCategoryUrl,
                    'name': subCategoryName
                })
        except:
            subUrl.append({
                'url': el["url"],
                'name': el["name"]
            })

    return subUrl

#print(subCategorySomef())


def scrapSomef(origin):

    site = 'https://somef.net/fr/'
    page = subCategorySomef()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/sn/somef.jpg"
        logoS = "http://137.74.199.121/img/logo/sn/logoS/somef.jpg"

        try:
            annonce = page_content.find('div',{"class":"laberProductGrid"}).findAll("article", {"class": "product-miniature"})
        except:
            continue


        for item in annonce:
            try:
                url = item.find("h2", {"class": "productName"}).find('a').get("href")
                lib = item.find("h2", {"class": "productName"}).find('a').text.strip()
                img = item.findAll("img")[0].get("src")
                try:
                    prix = int(item.findAll("span", {"class": "price"})[0].text.strip().replace('\xa0','').replace('CFA','').replace(',00',''))
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
                "country": "sn",
                "subcategory" : link["name"]
                }
                )

            except:
                continue

    return produits

produits = scrapSomef(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass


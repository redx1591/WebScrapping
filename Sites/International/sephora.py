from bs4 import BeautifulSoup
import requests

def categorySephora():
    site = "https://www.sephora.fr/"
    category = []

    page_response = requests.get(site, headers={'User-Agent':'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content,'html.parser')

    cat = page_content.find('div',{'class':'nav-level-2-wrapper'}).findAll('li',{"class":"nav-level-2-item"})

    for item in cat:
        catName = item.find("a").text.strip()
        catUrl = item.find("a").get("href")

        category.append({
            "url":catUrl,
            "name":catName
        })

    return category

#print(categorySephora())


def subcategorySephora():
    category = categorySephora()
    subcat = []

    for item in category:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, 'html.parser')

        try:
            subcategory = page_content.find('div',{'class':'subcategories-content'}).findAll('div',{'class':'subcategory-tile'})
            for elem in subcategory:
                subcatName = elem.find("a").text.strip()
                subcatUrl = elem.find("a").get("href")

                subcat.append({
                    'url':subcatUrl,
                    'name':item["name"] + "-" + subcatName
                })
        except:
            continue

    return subcat

#print(subcategorySephora())


def scrapSephora(origin):
    site = "https://www.sephora.fr/"
    link = subcategorySephora()
    produits = []

    for item in link:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, 'html.parser')

        logo = 'http://137.74.199.121/img/logo/inter/sephora.jpg'
        logoS = 'http://137.74.199.121/img/logo/inter/logoS/sephora.jpg'

        annonce = page_content.find("ul",{"id":"search-result-items"}).findAll("div",{"class":"product-tile"})
        for elem in annonce:
            try:
                url = elem.find("div", {"class": "product-info"}).find("a",{"class":"product-tile-link"}).get("href")
                lib = elem.find("div", {"class": "product-info"}).find("a",{"class":"product-tile-link"}).text.strip()
                img = elem.find('div',{'class':'product-image'}).find("a",{"class":"product-tile-link"}).find('img').get('data-src')
                try:
                    prix = float(elem.find("div",{"class":"product-info"}).find("div",{"class":"product-pricing"}).text.strip().replace(',','.').replace('€','')) * 656.00
                except:
                    prix = 0

                produits.append(
                    {
                        'libProduct': lib,
                        'slug': '',
                        'descProduct': '',
                        'size': 200,
                        'unit': 'g',
                        'priceProduct': int(prix),
                        'imgProduct': img,
                        'numSeller': '',
                        'src': site,
                        'urlProduct': url,
                        'logo': logo,
                        'logoS': logoS,
                        'origin': origin,
                        "country": "sephora",
                        'subcategory': item['name'],
                    })


            except:
                continue

    return produits

#print(scrapSephora(origin=0))

produits = scrapSephora(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())

    except:
        pass
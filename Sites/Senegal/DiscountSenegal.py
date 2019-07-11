from bs4 import BeautifulSoup
import requests

def subcategoryDiscountSn():

    categories_url = 'https://discount-senegal.com/categorie-produit/maison-et-deco/maison-meuble-tv/'
    subUrl = []

    page_response = requests.get(categories_url, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul', {"class": "product-categories"}).find("ul",{"class":"children"}).findAll('li',{"class":"cat-item"})

    for item in category:
        urlCategory = item.findAll('a')[0].get("href")
        nameCategory = item.findAll('a')[0].text.split('(')
        name = nameCategory[0]

        subUrl.append({
            'url':urlCategory,
            'name':name
        })

    return subUrl

#print(subcategoryDiscountSn())

def scrapDiscountSn(origin):

    site = 'https://discount-senegal.com/'
    subUrls = subcategoryDiscountSn()
    produits = []

    for url in subUrls:
        try:
            page_response = requests.get(url['url'], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")
            name = url['name']

            logo = 'http://137.74.199.121/img/logo/sn/discountsn.jpg'
            logoS  ='http://137.74.199.121/img/logo/sn/logoS/discountsenegal.jpg'
            annonce = page_content.find("div", {"id": "mf-shop-content"}).findAll('li',{'class':'product'})
        except:
            continue


        for item in annonce:
            try:
                url = item.find("div", {"class": "mf-product-details-hover"}).find("h2").find('a').get("href")

                lib = item.find("div", {"class": "mf-product-details-hover"}).find("h2").text

                img = item.find("div", {"class": "mf-product-thumbnail"}).findAll('a')[0].find("img").get("data-original")

                try:
                    prix = int(item.findAll("span", {"class": "price"})[0].find('span',{'class':'amount'}).text.replace(u' ', '').replace(u'FCFA', '').replace('\xa0',''))
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
                "subcategory" : name,
                })

            except:
                continue

    return produits

#print(scrapDiscountSn(origin=0))

produits=scrapDiscountSn(origin=0)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

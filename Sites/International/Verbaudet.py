from bs4 import BeautifulSoup
import requests

def categoryVerbaudet():
    site = "https://www.vertbaudet.com/fr/"
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul', {"class": "main_nav"}).findAll("a", {"class": "main_nav__item"})

    categories_urls = []

    for item in category:
        urlCategory = item.get("href")
        nameCategory = item.text

        categories_urls.append({
            'name':nameCategory,
            'url' : 'https://www.vertbaudet.com' + urlCategory
        })

    return categories_urls




def subcategoryVerbaudet():
    categories_urls = categoryVerbaudet()
    subcat = []

    for item in categories_urls:
        try:
            page_response = requests.get(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            cat = page_content.find('div',{'class':'guidednavigation'}).find("li",{"class":"dcategories"}).findAll('ul',{'class':'refinement-level-2'})

            for el in cat :
                urlCat = el.find("a").get("href")
                exclude = el.find('a').find('span').text
                nameCat = el.find("a").text.strip().replace(exclude,'')

                subcat.append({
                "name":nameCat + ' - ' + item['name'],
                "url": 'https://www.vertbaudet.com' + urlCat
                })
        except:
            continue

    return subcat


def scrapVerbaudet(origin):
    site = "https://www.vertbaudet.com/fr/"
    linkProduct = subcategoryVerbaudet()
    produits = []

    for item in linkProduct:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/inter/verbaudet.jpg"
        logoS = "http://137.74.199.121/img/logo/inter/logoS/verbaudet.jpg"

        post = page_content.find('div',{"class":"products"}).findAll('div',{'class':'product'})

        for el in post :
            try:
                lib = el.find('div',{'class':'product-content'}).find("h2",{"class":"title"}).text.strip()
                url = el.find('div',{'class':'product-content'}).find("h2",{"class":"title"}).find('a').get("href")
                img = el.find('div',{'class':'product-content'}).find("div",{"class":"picture"}).find("img").get("src").replace('//','')
                prix = int(float(el.find("div",{"class":"product-content"}).find("div",{"class":"pricecontainer"}).find('a',{"class":"price"}).get('data-price').replace(',','.')) * float(656.1))

                produits.append({
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': prix,
                'size':1,
                'unit':'Kg',
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': 'https://www.vertbaudet.com' + url,
                'logo': logo,
                'logoS': logoS,
                'origin': origin,
                "country": "verbaudet",
                'subcategory': item['name'],
            })

            except:
                continue
    return produits

produits = scrapVerbaudet(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass

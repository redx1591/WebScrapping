from bs4 import BeautifulSoup
import requests

def categoryBoulanger():
    site = "https://www.boulanger.com"
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul', {"class": "o-header_arch_list"}).findAll("li", {"class": "o-header_arch_items"})

    categories_urls = []

    for item in category:
        urlCategory = item.find('a',{"class":"o-header_arch_link"}).get("href")

        categories_urls.append(
            site + urlCategory
        )

    return categories_urls

#print(categoryBoulanger())


def subcategoryBoulanger():
    categories_urls = categoryBoulanger()
    subcat = []

    for item in categories_urls:
        page_response = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        cat = page_content.findAll("div",{"class":"cat"})

        for el in cat :
            urlCat = el.find("a").get("href")
            nameCat = el.find("a").text.strip()

            subcat.append({
                "name":nameCat,
                "url":urlCat
            })
    return subcat

#print(subcategoryBoulanger())


def linkBoulanger():
    subcat = subcategoryBoulanger()
    linkProduct = []
    site = "https://www.boulanger.com"

    for item in subcat:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            post = page_content.find("div",{"class":"productListe"}).findAll("div",{"class":"product"})

            for el in post:
                linkUrl = site + el.find('a').get("href")
                linkName = item["name"]

                linkProduct.append({
                    "url":linkUrl,
                    "name":linkName
                    })
        except:
            continue

    return linkProduct

#print(linkBoulanger())


def scrapBoulanger(origin):
    site = "https://www.boulanger.com"
    linkProduct = linkBoulanger()
    produits = []

    for item in linkProduct:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/inter/boulanger.jpg"
        logoS = "http://137.74.199.121/img/logo/inter/logoS/boulanger.jpg"

        try:
            lib = page_content.find("div",{"id":"pp"}).find("h1").text.strip()
            url = item["url"]
            img = page_content.find("div",{"id":"pp_pictureD"}).find("img").get("src")
            prix = int(page_content.find("div",{"class":"price"}).find("span",{"class":"exponent"}).text) * 656
            try:
                desc = page_content.find("table",{"class":"characteristic"}).text
                clean_size = None
                clean_unit = None
                word_list = desc.split(' ')
                unit_list = ['kilogrammes', 'kilogramme', 'grammes', 'gramme', 'kg', 'g']
                for word in word_list:
                    for unit in unit_list:
                        if word.startswith(unit):
                            size_index = word_list.index(word) - 1
                            if word_list[size_index].replace('.', '').replace(',', '').isdigit():
                                clean_size = word_list[size_index]
                                clean_unit = unit
                            break
            except:
                clean_unit = ""
                clean_size = 0

            produits.append({
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': prix,
                'size':int(float(clean_size.replace(',','.'))),
                'unit':clean_unit,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': url,
                'logo': logo,
                'logoS': logoS,
                'origin': origin,
                "country": "boulanger",
                'subcategory': item['name'],
            })

        except:
            continue

    return produits

produits = scrapBoulanger(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        print(item)
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass



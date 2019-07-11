from bs4 import BeautifulSoup
import requests

def categoryIKEA():
    site = "https://www.ikea.com/fr/fr/"
    category = []

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    cat = page_content.find("div",{"class":"departmentLinkBlock"}).findAll("li")

    for item in cat:
        urlCat = "https://www.ikea.com" + item.find("a").get("href")
        nameCat = item.find("a").text.strip()

        category.append({
            'name':nameCat,
            'url':urlCat
        })

    return category

print(categoryIKEA())

def subcategoryIKEA():
    category = categoryIKEA()
    subcat = []

    for item in category[0:1]:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            subcategory = page_content.findAll("div",{"class":"visualNavContainer"})
            for elem in subcategory:
                subcatUrl = "https://www.ikea.com" + elem.find("a",{"class":"categoryName"}).get("href")
                subcatName = elem.find("a",{"class":"categoryName"}).text

                subcat.append({
                    "url":subcatUrl,
                    "name":subcatName
                })
        except:
            continue

    return subcat

#print(subcategoryIKEA())


def linkProduit():
    subcat = subcategoryIKEA()
    links = []

    for item in subcat[0:1]:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            post = page_content.find('div',{'id':'productLists'}).findAll('a',{"class":"productLink"})
            for elem in post:
                url = "https://www.ikea.com" + elem.get("href")

                links.append({
                    'url':url,
                    'cat':item["name"]
                })
        except:
            continue

    return links

#print(linkProduit())


def scrapIKEA(origin):
    site = "https://www.ikea.com/fr/fr/"
    products = linkProduit()
    produits = []

    for link in products[0:1]:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = ""
        logoS = ""

        try:
            lib = page_content.find('div',{"id":"productInfoWrapper1"}).find("h1").text.strip()
            url = link["url"]
            img = "https://www.ikea.com" + page_content.find('img',{"id":"productImg"}).get("src")
            prix = page_content.find('div',{"id":"prodPrice"}).find("span",{"id":"price1"}).text.strip()
            desc = page_content.find("div",{"id":"productInfo1"})

            produits.append(
                {
                    'libProduct': lib,
                    'slug': '',
                    'descProduct': desc,
                    'priceProduct': prix,
                    'imgProduct': img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': url,
                    'logo': logo,
                    'logoS': logoS,
                    'origin': origin,
                    "country": "",
                    'subcategory': link['cat'],
                })

        except:
            continue

    return produits

print(scrapIKEA(origin=0))
from bs4 import BeautifulSoup
import  requests

def subcategoryMDM():
    cat = ["https://www.maisonsdumonde.com/FR/fr/e/meubles","https://www.maisonsdumonde.com/FR/fr/e/decoration","https://www.maisonsdumonde.com/FR/fr/e/mobilier-decoration-jardin"]
    subcat = []
    site = "https://www.maisonsdumonde.com"

    for item in cat:
        page_response = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            subcategory = page_content.find("div",{"class":"tag-list"}).findAll("div",{"class":"tag-badge"})
            for el in subcategory:
                url = el.find("a").get("href")
                name = el.find("a").text

                subcat.append({
                    "url":site + url,
                    "name":name
                })
        except:
            continue

    return subcat


def subcategoryMDM1():
    cat = ["https://www.maisonsdumonde.com/FR/fr/s/luminaires.htm"]
    subcat = []
    site = "https://www.maisonsdumonde.com"

    for item in cat:
        page_response = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            subcategy = page_content.findAll("a", {"class": "bt-chip"})
            for elem in subcategy:
                url = elem.get("href").replace('..','')
                name = elem.text

                subcat.append({
                    "url": site + url,
                    "name": name
                })
        except:
            continue

    return subcat

def subcategoryMDM2():
    cat = ["https://www.maisonsdumonde.com/FR/fr/meubles-decoration-enfant.htm"]
    subcat = []
    site = "https://www.maisonsdumonde.com"

    for item in cat:
        page_response = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            subcategory = page_content.findAll("a", {"class": "badge"})
            for elem in subcategory:
                url = elem.get("href")
                name = elem.text

                subcat.append({
                    "url": site + url,
                    "name": name
                })
        except:
            continue

    return subcat

#print(subcategoryMDM()+subcategoryMDM1()+subcategoryMDM2())


def linkProduits():
    subcat = subcategoryMDM()+subcategoryMDM1()+subcategoryMDM2()
    links = []
    site = "https://www.maisonsdumonde.com"

    for item in subcat:
        page_response = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content,"html.parser")

        try:
            post = page_content.findAll("article",{"class":"product-item"})
            for elem in post :
                url= elem.find("a",{"class":"link"}).get("href")
                name = elem.find("a",{"class":"link"}).text.strip()
                cat = item["name"]

                links.append({
                    'url': site + url,
                    'name':name,
                    'subcat':cat
                })

        except:
            continue

    return links

#print(linkProduits())

def scrapMDM(origin):
    site = "https://www.maisonsdumonde.com"
    products = linkProduits()
    produits = []

    for link in products:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/inter/maisons.jpg"
        logoS = "http://137.74.199.121/img/logo/inter/logoS/maisons.jpg"

        try:
            lib = link["name"]
            url = link["url"]
            img = page_content.find("img",{"class":"carousel-image"}).get("data-src")
            try:
                prix = int(str(page_content.find('p',{'class':'unit-price'}).find("b",{"class":"price"}).text.replace('€','').replace(',00','')).replace('\xa0','')) * 656
            except:
                prix = 0

            try:
                desc = page_content.find("div",{"id":"panelCharacteristics"}).find("div",{"class":"details-block"}).text
                word_list = desc.split('(kg)')
                bloc_poids = str(word_list[1])
                clean_unit = "Kg"
                clean_size = int(bloc_poids[:4].replace(':','').replace(' ',''))
            except:
                clean_unit = ""
                clean_size = 0

            produits.append(
                {
                    'libProduct': lib,
                    'slug': '',
                    'descProduct': '',
                    'size': clean_size,
                    'unit': clean_unit,
                    'priceProduct': prix,
                    'imgProduct': img,
                    'numSeller': '',
                    'src': site,
                    'urlProduct': url,
                    'logo': logo,
                    'logoS': logoS,
                    'origin': origin,
                    "country": "mdm",
                    'subcategory': link['subcat'],
                })

        except:
            continue

    return produits


produits = scrapMDM(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())

    except:
        pass


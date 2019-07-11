from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def categoryMysma():
    site = ['https://www.mysmacloset.com/univers-femme','https://www.mysmacloset.com/univers-homme']
    name = ['mode femme','mode homme']
    cat = []

    for el,li in zip(site,name):
        cat.append({
            'url':el,
            'name':li
        })

    return cat

#print(categoryMysma())

def scrapMysma(origin):
    category = categoryMysma()
    produits = []

    for link in category:
        site = "https://www.mysmacloset.com"
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="/Users/mac/PycharmProjects/comparez/Sites/International/chromedriver")
        driver.get(link['url'])

        logo = "http://137.74.199.121/img/logo/sn/mysma.jpg"
        logoS = "http://137.74.199.121/img/logo/sn/logoS/mysma.jpg"
        try:
            code = driver.find_element_by_class_name('_1RkJr').get_attribute("innerHTML")
            page_content = BeautifulSoup(code, "html.parser")
            li = page_content.findAll('li')

            for annonce in li:
                try:
                    name = annonce.find("h3", {"class": "cZv4d"}).text.strip()
                    url = annonce.find('a',{'class':'_3aG1r'}).get("href")
                    img = annonce.find('img', {"class": "_1d2tc"}).get("src")
                    try:
                        prix = int(annonce.find('div',{"class":"_1_AL6"}).find('span',{'class':'_2wyxs'}).text.strip().replace('FCFA','').replace(' ','').replace('\xa0',''))
                    except:
                        prix = 0

                    produits.append(
                        {
                            'libProduct': name,
                            'slug': '',
                            'priceProduct': prix,
                            'imgProduct': img,
                            'numSeller': '',
                            'src': site,
                            'urlProduct': url,
                            'logo': logo,
                            'logoS': logoS,
                            'origin': origin,
                            "country": "sn",
                            "subcategory": link['name']
                        })

                except:
                    continue

            driver.quit()
        except:
            continue

    return produits

produits = scrapMysma(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())
    except:
        pass

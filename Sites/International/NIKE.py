from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def categoryNike():
    site = "https://www.nike.com/fr/"
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
    driver.get(site)

    category = driver.find_element_by_class_name("merchMenuWrapper").get_attribute("innerHTML")
    driver.quit()

    page_content = BeautifulSoup(category, "html.parser")
    cat_element = page_content.findAll("a",{"class":"body-baseline-base"})

    categories_urls = []

    for item in cat_element:
        urlCategory = item.get("href")
        nameCategory = item.text

        categories_urls.append({
            "name": nameCategory,
            "url" :  urlCategory
        })

    return categories_urls

#print(categoryNike())


def scrapNike(origin):
    category = categoryNike()
    produits = []

    for link in category:
        site = "https://www.nike.com/fr/"
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(link['url'])

        logo = "http://137.74.199.121/img/logo/inter/nike.jpg"
        logoS = "http://137.74.199.121/img/logo/inter/nike.jpg"


        try:
            code = driver.find_element_by_class_name('exp-product-wall').get_attribute("innerHTML")
            page_content = BeautifulSoup(code, "html.parser")
            li = page_content.findAll('div',{"class":"grid-item"})

            for annonce in li:
                try:
                    name = annonce.find("div",{"class": "product-name"}).text.strip()
                    url = annonce.get("data-pdpurl")
                    img = annonce.find('div', {"class": "grid-item-image-wrapper"}).find("img").get("src")
                    try:
                        prix = int(annonce.find('div', {"class": "prices"}).find('span', {"class":"local"}).text.strip().replace('€','')) * 656
                    except:
                        prix = 0

                    produits.append(
                        {
                            'libProduct': name,
                            'slug': '',
                            'descProduct': '',
                            'size': 1,
                            'unit': 'Kg',
                            'priceProduct': prix,
                            'imgProduct': img,
                            'numSeller': '',
                            'src': site,
                            'urlProduct': url,
                            'logo': logo,
                            'logoS': logoS,
                            'origin': origin,
                            "country": "nike",
                            "subcategory": link['name']
                        })

                except:
                    continue

            driver.quit()
        except:
            print("no produits")

    return produits

produits = scrapNike(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())

    except:
        pass


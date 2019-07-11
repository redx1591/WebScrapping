from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def categoryCdiscount():
    site = "https://www.cdiscount.com/"
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
    driver.get(site)
    categories_urls = []
    try:
        category = driver.find_element_by_xpath("//*[@id='olMain']").get_attribute("innerHTML")
        driver.quit()
        page_content = BeautifulSoup(category, "html.parser")
        cat_element = page_content.findAll("li",{"class":"olMag"})



        for item in cat_element:
            urlCategory = item.find('a').get("href")
            nameCategory = item.find('a').text

            categories_urls.append({
                "name": nameCategory,
                "url": urlCategory
            })
        del categories_urls[0]
        del categories_urls[4]
        del categories_urls[9]
        del categories_urls[9]
        del categories_urls[12]
        del categories_urls[12]

    except:
        driver.quit()
        pass


    return categories_urls

#print(categoryCdiscount())

def subcatCdiscount():
    categories = categoryCdiscount()
    subcat = []
    for item in categories[1:-1]:
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(item["url"])
        try:
            subcategory = driver.find_element_by_class_name("hubHorizontalNavImgList").get_attribute("innerHTML")
            driver.quit()
            page_content = BeautifulSoup(subcategory, "html.parser")
            cat_element = page_content.findAll("li")
            for el in cat_element:
                subcatName = el.find('a').text
                subcatUrl = el.find('a').get("href")

                subcat.append({
                    'name':subcatName,
                    'url':subcatUrl
                })
        except:
            driver.quit()
            pass

    return subcat

#print(subcatCdiscount())

def linkCdiscount():
    link = subcatCdiscount()
    urlProduct = []

    for item in link:
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(item["url"])

        try:
            annonce = driver.find_element_by_class_name("jsUl").get_attribute("innerHTML")
            driver.quit()
            page_content = BeautifulSoup(annonce, "html.parser")
            cat_element = page_content.findAll("li",{"class":"cPdtItem"})

            for el in cat_element :
                url = el.find("a").get("href")
                name = item["name"]

                urlProduct.append({
                    'url':url,
                    'name':name
                })
        except:
            driver.quit()
            pass

    return urlProduct

#print(linkCdiscount())

def extract_size_and_unit(arg):
    clean_size = None
    clean_unit = None
    word_list = arg.split(' ')
    unit_list = ['kilogrammes', 'kilogramme', 'grammes', 'gramme', 'kg', 'g']
    for word in word_list:
        for unit in unit_list:
            if word.startswith(unit):
                size_index = word_list.index(word) - 1
                if word_list[size_index].replace('.', '').replace(',', '').isdigit():
                    clean_size = word_list[size_index]
                    clean_unit = unit
                break
    return clean_size, clean_unit


def scrapCdiscount(origin):
    site = "https://www.cdiscount.com/"
    urlProduct = linkCdiscount()
    produits = []

    for item in urlProduct:
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(item["url"])
        logo = "http://137.74.199.121/img/logo/inter/cdiscount.jpg"
        logoS = "http://137.74.199.121/img/logo/inter/cdiscount.jpg"

        try:
            lib = driver.find_element_by_xpath("//*[@id='fpZnPrdMain']/div[2]/div[3]/h1").text
            url = item["url"]
            img = driver.find_element_by_xpath("//*[@id='picture0']").get_attribute("src")
            try:
                prix = int(float(driver.find_element_by_xpath("//*[@id='addForm']/div[1]/span").get_attribute("content")))
            except:
                prix=0
            try:
                desc = driver.find_element_by_class_name("fpDescTb").text
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
                'size':clean_size,
                'unit':clean_unit,
                'priceProduct': prix * 656,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': url,
                'logo': logo,
                'logoS': logoS,
                'origin': origin,
                "country": "cdiscount",
                'subcategory': item['name'],
            })

        except:
            driver.quit()
            pass

        url = 'http://api.comparez.co/api/v1/ads/legacy/'
        for item in produits:
            try:
                print(item)
                response = requests.post(url, data=item)
                # api response
                print(response.json())
            except:
                pass

    return produits

produits = scrapCdiscount(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        print(response.json())

    except:
        pass



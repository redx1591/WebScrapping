from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def categoryBienici():
    site = "https://www.bienici.com/achat-appartement"
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
    driver.get(site)

    category = driver.find_element_by_class_name("searchLinks").get_attribute("innerHTML")
    driver.quit()

    page_content = BeautifulSoup(category, "html.parser")
    cat_element = page_content.findAll("a")

    categories_urls = []

    for item in cat_element:
        urlCategory = item.get("href")
        nameCategory = item.text

        categories_urls.append({
            "name": nameCategory,
            "url" :  "https://www.bienici.com" + urlCategory
        })

    return categories_urls

#print(categoryBienici())


def getAllPage():
    subCat = categoryBienici()
    page = []

    for item in subCat:
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(item["url"])
        try:
            maxPage = int(driver.find_element_by_xpath("//*[@id='searchResultsContainer']/div[3]/div/div[2]/a[10]").text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = item['url'] + "?page" + str(el)
                name = item['name']
                page.append({
                    'name':name,
                    'url': link

                })
            driver.quit()
        except:
            link1 = item['url']
            name1 = item['name']
            page.append({
                'url': link1,
                'name':name1
            })

    return page

#print(getAllPage())

def getAllPost():
    page = getAllPage()
    postLink = []

    for item in page:
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(item["url"])

        try:
            content = driver.find_element_by_class_name("resultsListContainer").get_attribute("innerHTML")
            page_content = BeautifulSoup(content, "html.parser")
            link = page_content.findAll("article",{"class":"sideListItem"})

            for el in link:
                linkUrl = el.find('a').get("href")
                typePost = item["name"]

                postLink.append({
                    'url':"https://www.bienici.com"+linkUrl,
                    'type':typePost
                })
            driver.quit()
        except:
            continue

    return postLink

#print(getAllPost())

def getPostDetail():
    postLink = getAllPost()
    post = []

    for item in postLink:
        options = Options()
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
        driver.get(item["url"])

        try:
            name = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[3]/div[1]/div[1]/h1").text
            url = item["url"]
            price = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div/div/span[1]").text
            typeBien = item["type"]
            contenu = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[3]/section[1]/div").text

            post.append({
                'nom': name,
                'url' : url,
                'prix':price,
                'type' : typeBien,
                'contenu':contenu
            })
        except:
            continue


    return post

print(getPostDetail())
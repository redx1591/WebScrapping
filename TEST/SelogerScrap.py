from bs4 import BeautifulSoup
import requests


def categorySeloger():
    site = 'https://www.seloger.com/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('div',{"class":"SeoLinksstyled__SeoBlocks-n3mtu0-3"}).findAll("a")
    categories_urls = []

    for item in category:
        urlCategory = item.get("href")
        nameCategory = item.text

        categories_urls.append({
            "name":nameCategory,
            "url":urlCategory
        })

    return categories_urls

#print(categorySeloger())

def getAllPage():
    subCat = categorySeloger()
    page = []

    for item in subCat:
        page_response = requests.get(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            maxPage = int(page_content.find('div',{"class":"pagination-number"}).findAll('a')[-1].text) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = item['url'] + "?LISTING-LISTpg=" + str(el)
                name = item['name']
                page.append({
                    'name':name,
                    'url': link

                })
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
        page_response = requests.get(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            link = page_content.find("section",{"class":"liste_resultat"}).findAll('div',{"class":"c-pa-list"})

            for el in link:
                linkUrl = el.find('a').get("href")
                typePost = item["name"]

                postLink.append({
                    'url':linkUrl,
                    'type':typePost
                })
        except:
            continue

    return postLink

#print(getAllPost())

def getPostDetail():
    postLink = getAllPost()
    post = []

    for item in postLink:
        page_response = requests.get(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            name = page_content.find('div',{'class':'c-main'}).find('h1',{"class","detail-title"}).text.strip().replace('\xa0','')
            url = item["url"]
            price = page_content.find('div',{'class':'c-main'}).find('div',{"class":"detail__resume"}).find('a',{"class":"price"}).text.strip()
            typeBien = item["type"]
            tailleBien = page_content.find('div',{'class':'c-main'}).find('div',{"class":"detail__resume"}).find('ul',{'class':'criterion'}).findAll('li')[2].text.strip()
            nombreChambre = page_content.find('div',{'class':'c-main'}).find('div',{"class":"detail__resume"}).find('ul',{'class':'criterion'}).findAll('li')[1].text.strip()
            contenu = page_content.find('div',{'class':'c-main'}).find('div',{"class":"js_anchorZone_start"}).find('input',{'name':'description'}).get("value")

            post.append({
                'nom': name,
                'url' : url,
                'prix':price,
                'type' : typeBien,
                'taille':tailleBien,
                'nombreChambre':nombreChambre,
                'contenu':contenu
            })
        except:
            continue


    return post

print(getPostDetail())




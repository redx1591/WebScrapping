from bs4 import BeautifulSoup
import requests

def categoryChutku():

    site = 'http://www.chutku.com.ng/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"home_categories"}).findAll("li")
    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryChutku())


def subCategoryChutku():

    site = 'http://www.chutku.com.ng/'
    categories_urls = categoryChutku()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")
        try:
            subCategories = page_content.find('ul', {"class": "left_subcate"}).findAll('li')

            for item in subCategories:
                subCategoryUrl = site + item.find('a').get("href")


                subUrl.append(
                    subCategoryUrl
                )

        except:
            url = el

            subUrl.append(
                url
            )

    return subUrl

#print(subCategoryChutku())


def getAllPage():
    subUrl = subCategoryChutku()
    page = []

    for url in subUrl:
        try:
            maxPage = 5
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?page=" + str(el)
                page.append(
                    link
                )
        except:

            link1 = url
            page.append(
                link1
            )

    return page

#print(getAllPage())


def scrapChutku(origin):
    site = 'http://www.chutku.com.ng'
    page = getAllPage()
    produits = []

    for url in page:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = "http://137.74.199.121/img/logo/ng/chutku.jpg"
        logoS = "http://137.74.199.121/img/logo/ng/logoS/chutku.jpg"
        annonce = page_content.find_all("div", {"class": "cl_listblock"})


        for item in annonce:
            try:
                url = item.find('a', {"class": "cl_tricky_link"}).get("href")
                lib = item.find('a', {"class": "cl_tricky_link"}).text
                img = item.find('div', {"class": "cl_listblock_img"}).findAll("img")[0].get("src")
                desc = item.find('div', {"class": "cl_list_des"}).text
                try:
                    prix = int(item.find("div", {"class": "cl_price"}).text.replace(u',', '').replace(u'₦', ''))
                except:
                    prix=0

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
                'logoS':logoS,
                'origin': origin,
                'country':'ng'
                }
                )
            except:
                continue

    return produits


produits = scrapChutku(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())
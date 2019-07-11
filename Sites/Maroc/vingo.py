from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests

"""Fonction pour récupérer les noms et les urls de toutes les catégories"""

def categoryVingo():
	site = 'http://www.vingo.ma'
	req = Request(site, headers={'User-agent': 'Mozilla/5.0'})
	page_html = urlopen(req).read()
	urlopen(req).close()
	parsed_page = soup(page_html, "html.parser")
	category = parsed_page.find('div', {"class": "contentmain"}).findAll("ul",{"class":"parent"})
	categories_urls = []

	for item in category :
		urlCategory = site + item.find('li',{"class":"node"}).find("a").get("href")

		categories_urls.append(
            urlCategory
        )

	return categories_urls

#print(categoryVingo())

"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryVingo():

	categories_urls = categoryVingo()
	subUrl = []
	site = 'http://www.vingo.ma'

	for el in categories_urls:
		req = Request(el, headers={'User-agent': 'Mozilla/5.0'})
		page_html = urlopen(req).read()
		urlopen(req).close()
		parsed_page = soup(page_html, "html.parser")

		subCategories = parsed_page.find('div', {"class": "_listCat"}).findAll('li')

		for item in subCategories:
			subCategoryUrl = site + item.find('a').get("href") + "?lang=fr&limit=60&limitstart=0"

			subUrl.append(
                    subCategoryUrl
                )

	return subUrl

#print(subCategoryVingo())

def vingoScrap(origin):
	site = "http://www.vingo.ma/"
	subUrls = subCategoryVingo()
	produits = []

	for url in subUrls:
		req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
		page_html = urlopen(req).read()
		urlopen(req).close()
		#parsing page into object
		parsed_page = soup(page_html, "html.parser")
		logo = "http://137.74.199.121/img/logo/ma/vingo.jpg"
		logoS = "http://137.74.199.121/img/logo/ma/logoS/vingo.jpg"

		try:
			products_container = parsed_page.find_all("div", {"class":"jomcltoprow"})
			products_price = parsed_page.find_all("meta", {"itemprop":"price"})
			i = 0
			for elem in products_container:
				try:
					product_img = elem.find_all("div", {"class":"jomclimgthumbnils"})[0].find_all("img")[0].get("src").strip()
				except:
					product_img = ""
				product_name = elem.find_all("div" ,{"class":"titleblock"})[0].find_all("a")[0].find_all("strong")[0].text.strip()
				product_url = elem.find_all("div" ,{"class":"titleblock"})[0].find_all("a")[0].get("href").strip()
				try:
					product_price = int(products_price[i].get("content").replace(u' ', '').replace(u'.', '').replace(u'Dhs', '').strip())
				except:
					product_price = 0
					pass

				produits.append({
				'libProduct': product_name,
				'slug':'',
				'descProduct': '',
				'priceProduct': product_price,
				'imgProduct': product_img,
				'numSeller':'',
				'src': site,
				'urlProduct': product_url,
				'logo': logo,
				'logoS':logoS,
				'origin': origin,
				'country':'ma'
				})
				i += 1
		except:
			continue

	return produits

""""produits = vingoScrap(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
	response = requests.post(url, data=item)
	# api response
	print(response.json())"""

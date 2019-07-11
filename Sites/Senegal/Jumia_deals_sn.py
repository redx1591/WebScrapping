from bs4 import BeautifulSoup
import requests

def categoryJumiaDeals():
	site = 'https://deals.jumia.sn/'
	page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
	page_content = BeautifulSoup(page_response.content, "html.parser")

	category = page_content.find('ul',{"class":"list-group"}).findAll("li",{"class":"list-group-item"})

	categories_urls = []

	for item in category:
		urlCategory = site + item.find('a').get("href")

		categories_urls.append(
			urlCategory
		)

	return categories_urls

#print(categoryJumiaDeals())

def subCategoryJumiaDeals():

	categories_urls = categoryJumiaDeals()
	subUrl = []

	site = 'https://deals.jumia.sn'

	for el in categories_urls:
		page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
		page_content = BeautifulSoup(page_response.content, "html.parser")

		subCategories = page_content.find('nav', {"class": "category-links"}).findAll('li')

		for item in subCategories:
			subCategoryUrl = site + item.find('a').get("href")
			subCategoryName = item.find('a').text

			subUrl.append({
				'url':subCategoryUrl,
				'name':subCategoryName
			})

	return subUrl

#print(subCategoryJumiaDeals())

def getAllPage():
	subUrl = subCategoryJumiaDeals()
	page = []
	maxPage = 9
	id = list(range(maxPage))
	del id[0]
	for url in subUrl:
		for item in id:
			link = url['url'] + "?page=" + str(item)
			page.append({
				'url': link,
				'name': url['name']
			})
	return page

#print(getAllPage())

def dealsJumiaSnScrap(origin):
	site = "https://deals.jumia.sn"
	page = getAllPage()
	produits = []

	for link in page:
		try:
			page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
			page_content = BeautifulSoup(page_response.content, "html.parser")

			products_container = page_content.find_all("div", {"class":"post"})
			logo = 'http://137.74.199.121/img/logo/sn/jumiadeals.jpg'
			logoS = 'http://137.74.199.121/img/logo/sn/logoS/jumiadeals.jpg'
		except:
			continue

		for item in products_container:
			try:
				url = item.findAll('a', {"class": "post-link"})[0].get("href")
				lib = item.find_all("a", {"class": "post-link"})[0].findAll("span")[0].text.strip()
				img = item.find_all("img", {"class": "product-images"})[0].get("data-src")

				try:
					prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace('\xa0','').replace('FCFA',''))
				except:
					prix = 0

				produits.append({
					'libProduct':lib,
					'slug':'',
					'descProduct':'',
					'priceProduct': prix,
					'imgProduct':img,
					'numSeller':'',
					'src':site,
					'urlProduct':site + url,
					'logo':logo,
					'logoS':logoS,
					'origin': origin,
					"country": "sn",
					"subcategory":link['name']

				})
			except:
				continue

	return produits

#print(dealsJumiaSnScrap(origin=1))

"""INSERTION DES CATEGORIES, SOUS-CATEGORIES ET DES PRODUITS"""

produits = dealsJumiaSnScrap(origin=1)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
	try:
		response = requests.post(url, data=item)
		# api response
		print(response.json())
	except:
		pass

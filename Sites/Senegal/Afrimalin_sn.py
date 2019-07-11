from bs4 import BeautifulSoup
import requests

def categoryAfrimalinSn():
	site = "https://www.afrimalin.sn"
	page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
	page_content = BeautifulSoup(page_response.content, "html.parser")

	category = page_content.find('div',{"class":"adListsCategoriesWrapper"}).findAll("div",{"class":"singleAdListCategory"})

	categories_urls = []

	for item in category:
		urlCategory = site + item.find('a').get("href")

		categories_urls.append(
			urlCategory
		)

	return categories_urls

#print(categoryAfrimalinSn())

def subCategoryAfrimalin():

	categories_urls = categoryAfrimalinSn()
	subUrl = []

	site = "https://www.afrimalin.sn"

	for el in categories_urls:
		page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
		page_content = BeautifulSoup(page_response.content, "html.parser")

		subCategories = page_content.find('div', {"class": "adListsCategoriesWrapper"}).findAll('li')

		for item in subCategories:
			subCategoryUrl = site + item.find('a').get("href")
			subCategoryName = item.find('a').text.strip()
			name = subCategoryName.split('(')

			subUrl.append({
				'url':subCategoryUrl,
				'name':name[0]
			}
			)

	return subUrl

#print(subCategoryAfrimalin())

def getAllPage():
	subUrl = subCategoryAfrimalin()
	page = []
	maxPage = 5
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


def afrimalinSnScrap(origin):
	site = "https://www.afrimalin.sn"
	page = getAllPage()
	produits = []

	for link in page:
		try:
			page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
			page_content = BeautifulSoup(page_response.content, "html.parser")
			logo = 'http://137.74.199.121/img/logo/sn/afrimalin.jpg'
			logoS = 'http://137.74.199.121/img/logo/sn/logoS/afrimalin.jpg'

			products_container = page_content.find('div',{"class":"adListsWrapper"}).findAll('div',{"class":"singleAdWrapper"})
		except:
			continue

		for item in products_container:
			try:
				url = item.find("h2").findAll('a')[0].get("href")
				lib = item.find("h2").findAll('a')[0].text
				img = item.find('div',{"class":"singleAdPhoto"}).findAll("img")[0].get("src")
				try:
					prix = int(item.findAll("p", {"class": "green-color"})[0].text.replace(u'FCFA', '').replace(' ',''))
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

#print(afrimalinSnScrap(origin=1))

"""INSERTION DES PRODUITS"""

produits = afrimalinSnScrap(origin=1)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
	try:
		print(item)
		response = requests.post(url, data=item)
		# api response
		print(response.json())
	except:
		pass
from bs4 import BeautifulSoup
import requests

def categoryCcbm():
	site = "https://www.ccbme.sn"
	page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
	page_content = BeautifulSoup(page_response.content, "html.parser")

	category = page_content.find('ul',{"id":"menu-products-onelev"}).findAll('li')
	categories_urls = []

	for item in category:
		urlCategory = item.find('a').get("href")
		nameCategory = item.find('a').text

		categories_urls.append({
			'url':urlCategory,
			'name':nameCategory
		})

	return categories_urls

#print(categoryCcbm())

def subcategoryCcbm():

	categories_urls = categoryCcbm()
	subUrl = []

	for url in categories_urls:
		page_response = requests.get(url["url"], headers={'User-Agent': 'Mozilla/5.0'})
		page_content = BeautifulSoup(page_response.content, "html.parser")

		subcategoy = page_content.find('ul',{"class":"product-categories"}).find("li",{"class":"current-cat"}).find("ul",{"class":"children"}).findAll("li")

		for item in subcategoy:
			subCategoryUrl = item.find('a').get("href")
			subCategoryName = item.find('a').text

			subUrl.append({
                'url' : subCategoryUrl,
                'name': subCategoryName
			})

	return subUrl

#print(subcategoryCcbm())

def getAllPage():
	categories_urls = subcategoryCcbm()
	page = []

	for url in categories_urls:
		page_response = requests.get(url['url'], headers={'User-Agent': 'Mozilla/5.0'})
		page_content = BeautifulSoup(page_response.content, "html.parser")

		try:
			maxPage = int(
				page_content.find('nav', {"class": "woocommerce-pagination"}).findAll('a')[-2].text) + 1
			id = list(range(maxPage))
			del id[0]

			for el in id:
				link = url['url'] + "page/" + str(el)
				page.append({
					'url': link,
					'name':url['name']
				}
				)
		except:
			link1 = url['url']

			page.append({
				'url': link1,
				'name':url['name']
			})

	return page


#print(getAllPage())

def ccbmeSnScrap(origin):
	site = "https://www.ccbme.sn"
	page = getAllPage()
	produits = []

	for link in page:
		try:
			page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
			page_content = BeautifulSoup(page_response.content, "html.parser")

			products_container = page_content.find_all("div", {"class":"product-grid-item"})
			logo = 'http://137.74.199.121/img/logo/sn/ccbm.jpg'
			logoS = 'http://137.74.199.121/img/logo/sn/logoS/ccbm.jpg'
		except:
			continue


		for elem in products_container:
			product_img = elem.find_all("div", {"class":"product-grid-img"})[0].find_all("img")[0].get("src")
			product_name = elem.find_all("h3")[0].text.strip()
			product_url = elem.find_all("a")[0].get("href")

			try:
				product_price = int(elem.find_all("span", {"class":"price"})[0].find_all("ins")[0].find_all("span", {"class":"amount"})[0].text.replace(u'\xa0','').replace(u'FCFA', '').replace(u' ','').strip())
			except:
				try:
					product_price = int(elem.find_all("span", {"class":"price"})[0].find_all("span", {"class":"amount"})[0].text.replace(u'\xa0','').replace(u'FCFA', '').replace(u' ','').strip())
				except:
					product_price = 0


			produits.append({
				'libProduct':product_name,
				'slug':'',
				'descProduct':'',
				'priceProduct': product_price,
				'imgProduct':product_img,
				'numSeller':'',
				'src':site,
				'urlProduct':product_url,
				'logo':logo,
				'logoS':logoS,
				'origin': origin,
				"country": "sn",
				"subcategory":link['name']
			})

	return produits

#print(ccbmeSnScrap(origin=0))

"""INSERTION DES PRODUITS"""

produits = ccbmeSnScrap(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
	try:
		print(item)
		response = requests.post(url, data=item)
		# api response
		print(response.json())
	except:
		pass
from bs4 import BeautifulSoup
import requests

def categoryDiayma():
	site = "http://diayma.com/"
	page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
	page_content = BeautifulSoup(page_response.content, "html.parser")

	fils = page_content.find("ul",{"class":"tree"}).findAll('li')
	categories_urls = []

	for item in fils :
		urlCategory = item.find("a").get("href")
		nameCategory = item.find("a").text

		categories_urls.append({
			'url':urlCategory,
			'name':nameCategory
		})

	del categories_urls[:3]

	return categories_urls

#print(categoryDiayma())


def diaymaComScrap(origin):
	site = "http://diayma.com/"
	page = categoryDiayma()
	produits = []

	for link in page:
		try:
			page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
			page_content = BeautifulSoup(page_response.content, "html.parser")
			products_container = page_content.find_all("li", {"class":"ajax_block_product"})
			logo = 'http://137.74.199.121/img/logo/sn/diama.jpg'
			logoS = 'http://137.74.199.121/img/logo/sn/logoS/dya.jpg'
		except:
			continue

		for elem in products_container:
			try:
				product_img = elem.find_all("div", {"class":"center_block"})[0].find_all("a", {"class":"product_img_link"})[0].find_all("img")[0].get("src")
				product_name = elem.find_all("div", {"class":"center_block"})[0].find_all("h3")[0].find_all("a")[0].text.strip()
				product_url = elem.find_all("div", {"class":"center_block"})[0].find_all("h3")[0].find_all("a")[0].get("href")
				product_desc = elem.find_all("div", {"class":"center_block"})[0].find_all("p", {"class":"product_desc"})[0].find_all("a")[0].text.strip().replace('\xa0',' ').replace('\r\n',' ')
				try:
					product_price = elem.find_all("div", {"class":"right_block"})[0]\
					.find_all("span", {"class":"price"})[0].text.strip().replace(u' ','').replace(u'FCFA', '')
				except:
					product_price = 0

				produits.append({
				'libProduct':product_name,
				'slug':'',
				'descProduct':product_desc,
				'priceProduct': product_price,
				'imgProduct':product_img,
				'numSeller':'',
				'src':site,
				'urlProduct':product_url,
				'logo':logo,
				'logoS':logoS,
				'origin': origin,
				"country": "sn",
				"subcategory": link['name']
				})
			except:
				continue


	return produits

#print(diaymaComScrap(origin=0))

"""INSERTION DES PRODUITS"""

produits = diaymaComScrap(origin=0)
url = 'http://api.comparez.co/api/v1/ads/legacy/'
for item in produits:
	try:
		response = requests.post(url, data=item)
		# api response
		print(response.json())
	except:
		pass
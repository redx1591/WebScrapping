from bs4 import BeautifulSoup
import requests

def getAllPage():
	category = ['https://www.decathlon.sn/1001-tous-les-sports', 'https://www.decathlon.sn/793-homme',
				'https://www.decathlon.sn/501-femme', 'https://www.decathlon.sn/16666-accessoires']
	name = ['tous les sports', 'mode homme', 'mode femme', 'accessoires mode']

	page = []

	for url,name in zip(category,name):
		page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		page_content = BeautifulSoup(page_response.content, "html.parser")

		try:
			maxPage = int(page_content.find('ul', {"class": "pagination"}).findAll('a')[-2].text) + 1
			id = list(range(maxPage))
			del id[0]

			for el in id:
				link = url + "?p=" + str(el)
				page.append({
					'url': link,
					'name':name
				}
				)
		except:

			link1 = url
			name1=name
			page.append({
				'url': link1,
				'name':name1
			}
			)

	return page

#print(getAllPage())

def scrapDecathlon(origin):
	site = "https://www.decathlon.sn"
	page = getAllPage()

	produits = []

	for link in page:
		try:
			page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
			page_content = BeautifulSoup(page_response.content, "html.parser")
			products_container = page_content.find_all("div", {"class":"box-product"})

			logo = 'http://137.74.199.121/img/logo/sn/decathlon.jpg'
			logoS = 'http://137.74.199.121/img/logo/sn/logoS/decathlon.jpg'
		except:
			continue

		for elem in products_container:
			try:
				product_img = elem.find_all("div", {"class":"product-image-container"})[0].find_all("a")[0].find_all("img")[0].get("src")
				product_name = elem.find_all("div", {"class":"resume"})[0].find_all("span", {"class":"title"})[0].find_all("a")[0].text.strip()
				product_url = elem.find_all("div", {"class":"resume"})[0].find_all("span", {"class":"title"})[0].find_all("a")[0].get("href")

				try:
					product_price = int(elem.find_all("div", {"class":"box-product__header"})[0].find_all("div", {"class":"sticker-price sticker-price--normal"})[0].text.replace(u'\xa0','').replace(u'CFA', '').replace(u' ','').strip())
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
					"subcategory":link["name"]
				})
			except:
				continue

	return produits

#print(scrapDecathlon(origin=0))
produits = scrapDecathlon(origin=0)
# api call
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
	try:
		response = requests.post(url, data=item)
		# api response
		print(response.json())
	except:
		pass
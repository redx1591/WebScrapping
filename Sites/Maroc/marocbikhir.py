from bs4 import BeautifulSoup
import requests


def subcategoryMarocBikhir():
	site = 'http://www.marocbikhir.com/'
	page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
	page_content = BeautifulSoup(page_response.content, "html.parser")

	subcategory = page_content.find('div', {"class": "container"}).findAll("li")
	subUrl = []

	for item in subcategory:
		cat = item.findAll('ul',{"class":"menu-dropdown"})
		for el in cat:
			links = el.findAll('li')
			for link in links:
				urlCategory = link.find('a').get('href')

				subUrl.append(
					urlCategory
				)

	return subUrl

print(subcategoryMarocBikhir())

def getAllPage():
	subUrl = subcategoryMarocBikhir()
	page = []

	for url in subUrl:
		try:
			maxPage = 5
			id = list(range(maxPage))
			del id[0]

			for el in id:
				link = url + "/" + str(el)
				page.append(
					link
				)
		except:

			link1 = url
			page.append(
				link1
			)

	return page
print(getAllPage())

def bikhirScrap(origin):

	site = "http://www.marocbikhir.com/"
	page = getAllPage()
	produits = []

	for url in page:
		page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		page_content = BeautifulSoup(page_response.content, "html.parser")
		logo = "http://137.74.199.121/img/logo/ma/marocbi.jpg"
		logoS = "http://137.74.199.121/img/logo/ma/logoS/marocbi.jpg"

		try:
			products_container = page_content.find_all("div", {"class":"line span11 columns"})

			for elem in products_container:
				try:
					product_img = elem.find_all("div", {"class":"photo"})[0].find_all("img")[0].get("src").strip()
				except:
					product_img = ""
				product_name = elem.find_all("div" ,{"class":"description"})[0].find_all("h3")[0].find_all("a")[0].text.strip()
				product_url = elem.find_all("div" ,{"class":"description"})[0].find_all("h3")[0].find_all("a")[0].get("href").strip()
				product_desc = elem.find_all("div", {"class":"description"})[0].find_all("p")[2].text.strip()
				try:
					product_price = int(elem.find_all("div", {"class":"description"})[0].find_all("small")[0].find_all("strong")[0].text.replace(u' ', '').replace(u'.', '').replace(u'DH', '').strip())
				except:
					product_price = 0
					pass

				produits.append({
				'libProduct': product_name,
				'slug':'',
				'descProduct': product_desc,
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

		except:
			continue

	return produits

produits = bikhirScrap(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
	response = requests.post(url, data=item)
	print(response.json())

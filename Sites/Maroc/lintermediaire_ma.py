from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests

def categoryLintermediare():
	url = 'http://lintermediaire.ma/search'
	req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
	page_html = urlopen(req).read()
	urlopen(req).close()
	parsed_page = soup(page_html, "html.parser")

	category = parsed_page.find('div',{"class":"categories-list"}).find('ul', {"class":"list-unstyled"}).findAll("li", {"class": "dropdown"})
	categories_urls = []


	for item in category:
		urlCategory = item.find('a').get("href")

		categories_urls.append(
			urlCategory
		)


	return categories_urls

#print(categoryLintermediare())

def getAllPage():
	page = []
	subUrl= categoryLintermediare()
	for url in subUrl:
		try:
			maxPage = 5
			id = list(range(maxPage))
			del id[0]

			for el in id:
				link = url + "/" +str(el)
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


def intermediaireScrap(origin):
	site = "http://lintermediaire.ma/"
	page = getAllPage()
	produits = []

	for url in page:
		try:
			req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
			page_html = urlopen(req).read()
			urlopen(req).close()

			#parsing page into object
			parsed_page = soup(page_html, "html.parser")
			products_container = parsed_page.find_all("div", {"class":"item-list"})
			prices_container = parsed_page.find_all("h3", {"class":"item-price"})
		except:
			continue

		logo = "http://137.74.199.121/img/logo/ma/lintermediaire.jpg"
		logoS = "http://137.74.199.121/img/logo/ma/logoS/lintermediaire.jpg"
		i=0
		for elem in products_container:
			try:
				product_img = elem.find_all("div", {"class":"add-image"})[0].find_all("img")[0].get("src").strip()
			except:
				product_img = ""
			product_name = elem.find_all("div" ,{"class":"add-details"})[0].find_all("a")[0].text.strip()
			product_url = elem.find_all("div" ,{"class":"add-details"})[0].find_all("a")[0].get("href").strip()
			try:
				product_price = int(prices_container[i].text.replace(u' ', '').replace(u'.', '').replace(u'Dhs', '').strip())
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
			i+=1

	return produits

"""produits = intermediaireScrap(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
	response = requests.post(url, data=item)
	print(response.json())"""
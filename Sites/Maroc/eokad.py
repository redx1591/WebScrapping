from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests

def categoryEokad():
	site = "https://eokad.ma/"
	req = Request(site, headers={'User-agent': 'Mozilla/5.0'})
	page_html = urlopen(req).read()
	urlopen(req).close()
	parsed_page = soup(page_html, "html.parser")
	categories = parsed_page.find('ul',{"class":"super-menu"}).findAll('li',{"class":"mega-menu-categories"})

	categories_urls = []

	for item in categories[1:-1] :
		urlCategory = item.findAll('a')[0].get("href")

		categories_urls.append(
			urlCategory
		)

	return categories_urls


#print(categoryEokad())

def subCategoryEokad():
	categories_urls = categoryEokad()
	subUrl = []

	for el in categories_urls:
		req = Request(el, headers={'User-agent': 'Mozilla/5.0'})
		page_html = urlopen(req).read()
		urlopen(req).close()
		parsed_page = soup(page_html, "html.parser")

		try:
			subCategories = parsed_page.find('div',{"class":"swiper-container"}).findAll('div',{"class":"refine-image swiper-slide xs-33 sm-25 md-25 lg-20 xl-20"})
		except :
			continue

		for item in subCategories:
			urlCat = item.findAll('a')
			for url in urlCat:
				subCategoryUrl = url.get("href") + "#"


			subUrl.append(
				subCategoryUrl
			)

	return subUrl

#print(subCategoryEokad())



def eokadScrap(origin):
	site = 'https://eokad.ma/'
	subUrls = subCategoryEokad()
	produits = []

	for url in subUrls :
		req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
		page_html = urlopen(req).read()
		urlopen(req).close()
		parsed_page = soup(page_html, "html.parser")
		logo = "http://137.74.199.121/img/logo/ma/eokad.jpg"
		logoS = "http://137.74.199.121/img/logo/ma/logoS/eokad.jpg"

		products_container = parsed_page.find_all("div", {"class":"product-grid-item xs-50 sm-50 md-25 lg-25 xl-25"})

		#getting informations by looping into the all the products containers tag
		for elem in products_container:
			try:
				product_img = elem.find_all("img", {"class":"lazy first-image"})[0].get("src").strip()
				product_name = elem.find_all("h4", {"class":"name"})[0].find("a").text.strip()
				product_url = elem.find_all("h4", {"class":"name"})[0].find("a").get("href").strip()
				product_desc = elem.find_all("p", {"class":"description"})[0].text.strip().replace('\xa0','').replace('  ','')
				try:
					product_price = int(elem.find_all("span", {"class":"price-new"})\
					[0].text.strip().replace(u' ', '').replace(u'Dhs', ''))
				except:
					product_price = 0
					pass

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
					'country':'ma'
				})
			except:
				pass

	return produits

"""produits = eokadScrap(origin=0)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
	response = requests.post(url, data=item)
	print(response.json())"""

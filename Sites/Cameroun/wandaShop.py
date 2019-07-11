from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

def subCategoryWandaShop():

    subUrl = []
    site = 'https://wandashops.com/'

    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    subCategories = page_content.find('ul', {"class": "osh-subcategories"}).findAll('li',{"class":"osh-subcategory"})

    for item in subCategories:
        subCategoryUrl = item.find('a').get("href")

        subUrl.append(
            subCategoryUrl
        )

    return subUrl

print(subCategoryWandaShop())


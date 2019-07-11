from bs4 import BeautifulSoup
import requests



def scrapVoitureAuMaroc(origin):

    site = 'http://www.voitureaumaroc.com'
    subUrls  = ["http://www.voitureaumaroc.com/auto/miseajour.asp",
                "http://www.voitureaumaroc.com/auto/miseajour.asp?page=75&ob=&obp=&obm=&oby=&marque=Land Rover&model=&ville=&carburation=&photo=&boitevitesse=",
                "http://www.voitureaumaroc.com/auto/miseajour.asp?page=150&ob=&obp=&obm=&oby=&marque=Land Rover&model=&ville=&carburation=&photo=&boitevitesse=",
                "http://www.voitureaumaroc.com/auto/miseajour.asp?page=225&ob=&obp=&obm=&oby=&marque=Land Rover&model=&ville=&carburation=&photo=&boitevitesse=",
                ]
    produits = []

    for url in subUrls:
        page_response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/ma/voituresmaroc.jpg'
        logoS = 'http://137.74.199.121/img/logo/ma/logoS/voituresaumaroc.jpg'
        annonce = page_content.findAll('table', {"class": "srlcomplinesbot"})


        for item in annonce:
            try:
                url = item.findAll('strong')[0].find('a').get("href")
                lib = item.findAll('strong')[0].text.strip()

                if (lib.endswith("dhs")):
                    price = lib.split(" ")
                    prix = price[-2]
                    names = price[0:-2]
                    name = (" ").join(names)
                elif (lib.endswith("Précisé")):
                    nom = lib.split(":")
                    name = nom[0].replace(u'Prix', '')
                    prix = 0

                img = item.findAll('img')[0].get("src")
                desc = item.findAll('p', {"class": "wrapping"})[0].text.strip()

                produits.append(
                {
                'libProduct': name,
                'slug': '',
                'descProduct': desc,
                'priceProduct': prix,
                'imgProduct': site + img,
                'numSeller': '',
                'src': site,
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                'country':'ma'
                })

            except:
                continue

    return produits

"""produits = scrapVoitureAuMaroc(origin=1)
url = 'http://api.comparez.co/ads/insert-product/'
for item in produits:
    response = requests.post(url, data=item)
    # api response
    print(response.json())"""


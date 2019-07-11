import requests
import schedule
import time
from Sites.Maroc.Avito import scrapAvito
from Sites.Maroc.Boutika import scrapBoutika
from Sites.Maroc.choix_ma import choixScrap
from Sites.Maroc.Decathlon import scrapDecathlon
from Sites.Maroc.eokad import eokadScrap
from Sites.Maroc.fashionavenue_ma import fashionScrap
from Sites.Maroc.hmizatema import scrapHmizate
from Sites.Maroc.jumia import jumiaScrap
from Sites.Maroc.JumiaDeals import scrapJumiaDeals
from Sites.Maroc.lintermediaire_ma import intermediaireScrap
from Sites.Maroc.mabroka import mabrokaScrap
from Sites.Maroc.MarocAnnonces import scrapMarocAnnonces
from Sites.Maroc.marocbikhir import bikhirScrap
from Sites.Maroc.marocVente import marocVenteScrap
from Sites.Maroc.Tovit import scrapTovit
from Sites.Maroc.vingo import vingoScrap
from Sites.Maroc.VoitureAuMaroc import scrapVoitureAuMaroc


def insertMa():
    print("start!!")
    produits = scrapAvito(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    produits = scrapBoutika(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    produits = choixScrap(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = scrapDecathlon(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = eokadScrap(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = fashionScrap(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = scrapHmizate(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    produits = jumiaScrap(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    produits = scrapJumiaDeals(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    produits = intermediaireScrap(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = mabrokaScrap(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        try:
            response = requests.post(url, data=item)
            print(response.json())
        except:
            continue

    produits = scrapMarocAnnonces(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = bikhirScrap(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = marocVenteScrap(origin=0)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = scrapTovit(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        print(response.json())

    produits = vingoScrap(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    produits = scrapVoitureAuMaroc(origin=1)
    url = 'http://api.comparez.co/ads/insert-product/'
    for item in produits:
        response = requests.post(url, data=item)
        # api response
        print(response.json())

    print("Done!!!")


schedule.every().day.at("00:05").do(insertMa())
#schedule.every().second.do(insertMa)

while True:
    schedule.run_pending()
    time.sleep(1)
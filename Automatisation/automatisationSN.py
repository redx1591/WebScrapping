import schedule
import time
from Sites.Senegal.ExpatDakar import scrapExpatDakar
from Sites.Senegal.Jumia_deals_sn import dealsJumiaSnScrap
from Sites.Senegal.DakarAuto import scrapDakarAuto
from Sites.Senegal.Coinafrique import coinAfriqueComScrap
from Sites.Senegal.JumiaSn import jumiaScrap
from Sites.Senegal.AfriMarket import scrapAfriMarket
from Sites.Senegal.Diayma_com import diaymaComScrap
from Sites.Senegal.PromoSn import scrapPromoSn
from Sites.Senegal.Nova_sn import novaSnScrap
from Sites.Senegal.Afrimalin_sn import afrimalinSnScrap
from Sites.Senegal.Decathlon_sn import scrapDecathlon
from Sites.Senegal.ElectroMenagerDkr import scrapElectroMenagerDkr
from Sites.Senegal.Ccbme_sn import ccbmeSnScrap
from Sites.Senegal.DiscountSenegal import scrapDiscountSn
from Sites.Senegal.OrangeSn import scrapOrangeSn
from Sites.Senegal.TigoSn import scrapTigoSn
from Sites.Senegal.MaMaisonSn import scrapMaMaison
from Sites.Senegal.SenShop import senShopScrap
from Sites.Senegal.wellmah import WellmahScrap
from Sites.Senegal.somef_sn import  scrapSomef
import requests

def insertSen():
    print("start")
    try:
        produits = scrapOrangeSn(origin=0)
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapMaMaison(origin=0)
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = afrimalinSnScrap(origin=1)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapAfriMarket(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = ccbmeSnScrap(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = coinAfriqueComScrap(origin=1)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapDakarAuto(origin=1)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapDecathlon(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = diaymaComScrap(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapDiscountSn(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapElectroMenagerDkr(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapExpatDakar(origin=1)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = dealsJumiaSnScrap(origin=1)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = jumiaScrap(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = novaSnScrap(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapPromoSn(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapTigoSn(origin=0)
        # api call
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = senShopScrap(origin=0)
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = WellmahScrap(origin=0)
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())

        produits = scrapSomef(origin=0)
        url = 'http://api.comparez.co/ads/insert-product/'
        for item in produits:
            response = requests.post(url, data=item)
            # api response
            print(response.json())


        print("done")
    except:
        print("error")



schedule.every().day.at("13:00").do(insertSen)
#schedule.every().second.do(insertSen)

while True:
    schedule.run_pending()
    time.sleep(1)
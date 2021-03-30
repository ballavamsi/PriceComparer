import pandas as pd
import switcher
import amazon_india as amazon
import models.product as productsmodel

records_to_consider = 5
global products

class WebScrape(object):
    def start(self,website,productname):
            method_name=website+'WebScrape'
            method=getattr(self,method_name,lambda :'Invalid')
            return method(productname)
    def amazonWebScrape(self,productname):
        print("amazon:"+productname)
        amazonproducts = amazon.search(productname)
        # getting top 5 records
        products = amazonproducts[:records_to_consider]
        return products
    def flipkartWebScrape(self,productname):
        print("flipkart:"+productname)

    def allSitesWebScrape(self,productname):
        products = []
        print("all:"+productname)
        amazonproducts = amazon.search(productname)
        # getting top 5 records
        products = (amazonproducts[:records_to_consider])
        return products

search = WebScrape()
result = search.start("amazon","curved led screen")

print("------ completed web scrapping ------")
for product in result:
    print("Name:" + product.name + " Current Price:" + product.price + " Original Price:" + product.orginal_price + " No of user rated:" + product.no_of_users_rated + " Rating:" + product.rating + " Website:"+ product.website)      
            
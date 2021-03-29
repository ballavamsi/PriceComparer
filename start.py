import pandas as pd
import switcher

class WebScrape(object):
    def start(self,website,productname):
            method_name=website+'WebScrape'
            method=getattr(self,method_name,lambda :'Invalid')
            return method(productname)
    def amazonWebScrape(self,productname):
        print("amazon:"+productname)

    def flipkartWebScrape(self,productname):
        print("flipkart:"+productname)

    def allSitesWebScrape(self,productname):
        print("all:"+productname)    

search = WebScrape()
result = search.start("amazon","curved led screen")
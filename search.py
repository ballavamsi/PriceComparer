import pandas as pd
import switcher
import amazon_india as amazon
import models.product as productsmodel
import sys
import getopt

records_to_consider = 5
global products



def main(argv):
    pname = ""
    try:
        opts, args = getopt.getopt(argv,"n:o",["name="])
    except getopt.GetoptError:
        print('start.py -n <productname>')
        print('start.py --name <productname>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-n','--name'):
            pname = arg
        else:
            print('start.py -n <productname>')
            sys.exit()
    if(pname != ""):            
        print("Searching for product name:" + arg)
        search(pname)
    else:
        print('Product name to search cannot be empty')
        print('start.py -n <productname>')
        print('start.py --name <productname>')
 
class WebScrape(object):
    def start(self, website, productname):
            method_name = website+'WebScrape'
            method = getattr(self, method_name, lambda: 'Invalid')
            return method(productname)

    def amazonWebScrape(self, productname):
        print("amazon:"+productname)
        amazonproducts = amazon.search(productname)
        # getting top 5 records
        products = amazonproducts[:records_to_consider]
        return products

    def flipkartWebScrape(self, productname):
        print("flipkart:"+productname)

    def allSitesWebScrape(self, productname):
        products = []
        print("all:"+productname)
        amazonproducts = amazon.search(productname)
        # getting top 5 records
        products = (amazonproducts[:records_to_consider])
        return products

       
def search(name):
    search = WebScrape()
    result = search.start("amazon",name)

    print("------ completed web scrapping ------")
    for product in result:
        print("Name:" + product.name + " Current Price:" + product.price + " Original Price:" + product.orginal_price + " No of user rated:" + product.no_of_users_rated + " Rating:" + product.rating + " Website:"+ product.website)      
                


if __name__ == "__main__":
   main(sys.argv[1:])
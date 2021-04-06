import pandas as pd
import switcher
import amazon_india as amazon
import flipkart_india as flipkart
import models.product as productsmodel
import sys,os
import getopt

records_to_consider = 5
global products



def main(argv):
    pname = ""
    websiteToSearch = "all"
    try:
        opts,args = getopt.getopt(argv,"n:w:",["name=","website="])
    except getopt.GetoptError:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('start.py -n <productname> [-w "amazon"|"flipkart"|"all"]')
        print('start.py --name <productname> [--website "amazon"|"flipkart"|"all"]')
        sys.exit(2)
    #opts = x for x in opts if x)
    print(opts)    
    for opt in opts:
        if opt:
            if opt[0] in ('-n','--name'):
                pname = opt[1]
                print(pname)
            if opt[0] in ('-w','--website'):
                websiteToSearch = opt[1]     
        #else:
        #    print('start.py -n <productname> [-w "amazon"|"flipkart"|"all"]')
        #    sys.exit()
    if(pname != ""):            
        print("Searching for product name:" + pname)
        search(websiteToSearch,pname)
    else:
        print('Product name to search cannot be empty')
        print('start.py -n <productname> [-a,-f]')
        print('start.py --name <productname> [-a,-f]')
        print('-a = Search in amazon')
        print('-f = Search in flipkart')
        sys.exit()
 
class WebScrape(object):
    def start(self, website, productname):
            method_name = website+'WebScrape'
            method = getattr(self, method_name, lambda: 'Invalid')
            return method(productname)

    def amazonWebScrape(self, productname):
        print("amazon:"+productname)
        amazonproducts = amazon.search(productname)
        return amazonproducts[:records_to_consider]

    def flipkartWebScrape(self, productname):
        print("flipkart:"+productname)
        flipkartproducts = flipkart.search(productname)
        return flipkartproducts[:records_to_consider]

    def allSitesWebScrape(self, productname):
        print("all:"+productname)
        amazonproducts = amazon.search(productname)
        flipkartproducts = flipkart.search(productname)
        return amazonproducts[:records_to_consider] + flipkartproducts[:records_to_consider]
       
def search(websiteToSearch,name):
    search = WebScrape()
    result = search.start(websiteToSearch,name)
    dataResult = []
    print("------ completed web scrapping ------")
    for product in result:
        dataResult.append(product.__dict__)
        #print(product.__dict__)
        #print("Name:" + product.name + " Current Price:" + product.price + " Original Price:" + product.orginal_price + " No of user rated:" + product.no_of_users_rated + " Rating:" + product.rating + " Website:"+ product.website)      
    return dataResult


if __name__ == "__main__":
   main(sys.argv[1:])

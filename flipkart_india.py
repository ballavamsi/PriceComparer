import models.product as productsmodel
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import time
import json as jsonm
import re
import sys,os

BASE_URL = 'https://www.flipkart.com'
SEARCH_PRE_PARAMS = '/search?q='
SEARCH_POST_PARAMS = ''
logging = True


def search(product_name, attempt=0):
    URL = BASE_URL + SEARCH_PRE_PARAMS + product_name# + SEARCH_POST_PARAMS
    products = []
    print(URL)
    try:
        if(attempt > 0):
            #URL = URL +'_'+str(attempt)
            print(str(attempt))
            print(URL)
        response = requests.get(URL)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        results = BeautifulSoup(response.content, 'html.parser')
        product_elements = results.find_all(has_attr_data_id)
        for each_product in product_elements:
            product = productsmodel.Product()
            #print("-------------------")
            #print(each_product)
            all_links = each_product.find_all("a",attrs={"rel": "noopener noreferrer"})
            #foundContent = False
            for eachlink in all_links:
                #print("===========")
                #print(eachlink)
                #print("--------")
                #if(eachlink.has_attr('title') or not foundContent):
                #    next
                if(eachlink.has_attr('title')):
                    #foundContent = True
                    product.name = eachlink["title"]
                    product.website = str(BASE_URL + eachlink["href"])
                    #print(product.name)
                    #print(product.website)
                if("₹" in eachlink.text):
                    prices_div = eachlink.find_all('div')[0]
                    if(len(prices_div) > 0):
                        prices_inner_div = prices_div.find_all('div')
                        if(len(prices_inner_div) > 0):
                            price = prices_div.find_all('div')[0]
                            product.price = price.text
                        if(len(prices_inner_div) > 1):
                            original_price = prices_div.find_all('div')[1]
                            product.orginal_price = original_price.text
                    #print(eachlink.innerHTML)
                    #print(product.price)
                #print("===========")    
            product.no_of_users_rated = str(0)
            product.rating = str(0)

            rating = each_product.find_all("div")
            i =0
            for r in rating:
                #print(str(i) + ":" + str(r.text))
                i+=1
                if("(" in r.text and not "₹" in r.text):
                    rating_text = r.text
                    #print(rating_text)
                    ratings_list = r.text.split('(')
                    if(len(ratings_list) > 0):
                        product.rating = ratings_list[0]
                    if(len(ratings_list) > 1):
                        product.no_of_users_rated = ratings_list[1].split(')')[0]
                    break       
            if logging and product.name != "":
                print("Name:" + product.name + " Current Price:" + product.price + " Original Price:" + product.orginal_price +
                     " No of user rated:" + product.no_of_users_rated + " Rating:" + product.rating + " Website:" + product.website)
            if(product.name != ""):
               products.append(product)
        return products
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        time.sleep(10)
        if(attempt <= 5):
            return search(product_name, attempt+1)
        else:
            print('Maximum retries reached')
            return []
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        time.sleep(10)
        if(attempt <= 5):
            return search(product_name, attempt+1)
        else:
            print('Maximum retries reached')
            return []
    else:
        print('Success')
    return products
    # for eachp in products:
    #    print("Name:" + eachp.name + " Current Price:" + eachp.price + " Original Price:" + eachp.orginal_price + " No of user rating:" + eachp.no_of_users_rated + " Website:"+ eachp.website)
    #    print(jsonm.dumps(eachp))

# execute this using python .\flipkart_india.py

def has_attr_data_id(tag):
    return tag.has_attr('data-id')


def main():
    print("flipkart method")
    #products = search("curved led screen")
    # for p in products:
    #    print(p.name)


if __name__ == "__main__":
    main()

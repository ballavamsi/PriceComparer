import models.product as productsmodel
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import time
import json as jsonm

MAIN_URL = 'https://www.amazon.in/s?k=[product_name]&ref=nb_sb_noss'
logging = False

def search(product_name,attempt=0):
    URL = MAIN_URL.replace('[product_name]',product_name)
    products = []
    try:
        if(attempt>0):
            URL = URL+'_'+str(attempt)
        response = requests.get(URL)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        results = BeautifulSoup(response.content, 'html.parser')
        product_elements = results.find_all('div', class_='s-result-item')
        for each_product in product_elements:
            product = productsmodel.Product()
            all_links = each_product.find_all('a',class_='a-link-normal')
            for eachlink in all_links:
                if(eachlink.find('span',class_='a-size-medium')):
                    title_elem = eachlink
                    product.name = title_elem.text
                    product.website = eachlink.get('href')
                if(len(eachlink.find_all('span',class_="a-price"))>0):
                    all_prices = eachlink.find_all('span',class_="a-price")
                    if(len(all_prices)>0):
                        product.price = all_prices[0].find_all('span')[0].text
                    if(len(all_prices)>1):
                        product.orginal_price = all_prices[1].find_all('span')[0].text
                if(eachlink.find('span',class_='a-size-base')):
                    #print(eachlink)
                    product.url = eachlink.get('href')
                    product.no_of_users_rated = eachlink.text
                #if(eachlink.find('span',class_='a-price')):
                #    print(eachlink)
            if logging:    
                print("Name:" + product.name + " Current Price:" + product.price + " Original Price:" + product.orginal_price + " No of user rating:" + product.no_of_users_rated + " Website:"+ product.website)      
            if(product.name != ""):
                products.append(product)
            #return products
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        time.sleep(10)
        if(attempt<=5):
            return search(product_name,attempt+1)
        else:
            print('Maximum retries reached')
            return []    
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        time.sleep(10)
        if(attempt<=5):
            return search(product_name,attempt+1)
        else:
            print('Maximum retries reached')
            return [] 
    else:
        print('Success')
    return products
    #for eachp in products:
    #    print("Name:" + eachp.name + " Current Price:" + eachp.price + " Original Price:" + eachp.orginal_price + " No of user rating:" + eachp.no_of_users_rated + " Website:"+ eachp.website)      
    #    print(jsonm.dumps(eachp))

# execute this using python .\amazon-india.py
def main():
    print("amazon method")
    #products = search("printer")
    #for p in products:
    #    print(p.name)

if __name__ == "__main__":
    main()  
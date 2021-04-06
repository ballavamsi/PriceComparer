from selenium import webdriver
import os,sys,time,urllib
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import models.product as productsmodel

ENVIRONMENT = os.getenv('PRICE_COMPARER_OS')
BASE_URL = 'https://www.flipkart.com'
SEARCH_PRE_PARAMS = '/search?'
SEARCH_POST_PARAMS = ''
logging = False


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #if(ENVIRONMENT == 'WINDOWS'):
    driver = webdriver.Chrome(dir_path + "\\chromedriver\\windows\\chromedriver", chrome_options=options)
    driver.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True})
except:
    logging = True
#else:
#    driver = webdriver.Chrome(dir_path + "/chromedriver/linux/chromedriver", chrome_options=options)


def search(product_name, attempt=0):
    productQuery = { 'q' : product_name}
    URL = BASE_URL + SEARCH_PRE_PARAMS + urllib.parse.urlencode(productQuery) + SEARCH_POST_PARAMS
    products = []
    print(URL)

    try:
        if(attempt > 0):
            print("Attempt:" + str(attempt))
            print(URL)
        driver.get(URL)
        page_source = driver.page_source
        print(page_source)
        results = BeautifulSoup(page_source, 'html.parser')
        product_elements = results.find_all(has_attr_data_id)
        for each_product in product_elements:
            product = productsmodel.Product()
            product.website = "Flipkart"
            print("-------------------")
            print(each_product)
            all_links = each_product.find_all("a",attrs={"rel": "noopener noreferrer"})
            #foundContent = False
            for eachlink in all_links:
                print("===========")
                print(eachlink)
                print("--------")
                #if(eachlink.has_attr('title') or not foundContent):
                #    next
                if(eachlink.has_attr('title')):
                    print(eachlink)
                    #foundContent = True
                    product.name = eachlink["title"]
                    product.url = str(BASE_URL + eachlink["href"])
                    print(product.name)
                    print(product.website)
                if("₹" in eachlink.text):
                    prices_div = eachlink.find_all('div')[0]
                    if(len(prices_div) > 0):
                        prices_inner_div = prices_div.find_all('div')
                        if(len(prices_inner_div) > 0):
                            price = prices_div.find_all('div')[0]
                            product.price = price.text
                        if(len(prices_inner_div) > 1):
                            original_price = prices_div.find_all('div')[1]
                            product.original_price = original_price.text
                    print(eachlink.innerHTML)
                    print(product.price)
                print("===========")    
            product.no_of_users_rated = str(0)
            product.rating = str(0)

            rating = each_product.find_all("div")
            i =0
            for r in rating:
                print(str(i) + ":" + str(r.text))
                i+=1
                if("(" in r.text and not "₹" in r.text):
                    rating_text = r.text
                    print(rating_text)
                    ratings_list = r.text.split('(')
                    if(len(ratings_list) > 0):
                        product.rating = ratings_list[0]
                    if(len(ratings_list) > 1):
                        product.no_of_users_rated = ratings_list[1].split(')')[0]
                    break       
            #if logging and product.name != "":
            print(product.__dict__)
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

def has_attr_data_id(tag):
    return tag.has_attr('data-id')


def main():
    print("flipkart method")
    products = search("curved led screen")
    for p in products:
        print(p.__dict__)


if __name__ == "__main__":
    main()        
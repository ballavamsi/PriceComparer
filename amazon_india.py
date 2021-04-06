from selenium import webdriver
import os,sys,time,urllib
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import models.product as productsmodel

ENVIRONMENT = os.getenv('PRICE_COMPARER_OS')
BASE_URL = 'https://www.amazon.in'
SEARCH_PRE_PARAMS = '/s?'
SEARCH_POST_PARAMS = '&ref=nb_sb_noss'
logging = False


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

dir_path = os.path.dirname(os.path.realpath(__file__))
#if(ENVIRONMENT == 'WINDOWS'):
driver = webdriver.Chrome(dir_path + "\\chromedriver\\windows\\chromedriver", chrome_options=options)
#else:
#    driver = webdriver.Chrome(dir_path + "/chromedriver/linux/chromedriver", chrome_options=options)


def search(product_name, attempt=0):
    productQuery = { 'k' : product_name}
    URL = BASE_URL + SEARCH_PRE_PARAMS + urllib.parse.urlencode(productQuery) + SEARCH_POST_PARAMS
    products = []
    print(URL)

    try:
        if(attempt > 0):
            URL = URL+'_'+str(attempt)
            print(str(attempt))
            print(URL)
        driver.get(URL)
        page_source = driver.page_source
        results = BeautifulSoup(page_source, 'html.parser')
        product_elements = results.find_all('div', class_='s-result-item')
        for each_product in product_elements:
            product = productsmodel.Product()
            product.website = "Amazon"
            all_links = each_product.find_all('a', class_='a-link-normal')
            for eachlink in all_links:
                if(eachlink.find('span', class_='a-size-medium')):
                    title_elem = eachlink
                    product.name = title_elem.text
                    product.url = BASE_URL + eachlink.get('href')
                if(len(eachlink.find_all('span', class_="a-price")) > 0):
                    all_prices = eachlink.find_all('span', class_="a-price")
                    if(len(all_prices) > 0):
                        product.price = all_prices[0].find_all('span')[0].text
                    if(len(all_prices) > 1):
                        product.original_price = all_prices[1].find_all('span')[
                            0].text
                if(eachlink.find('span', class_='a-size-base')):
                    # print(eachlink)
                    product.url = eachlink.get('href')
                    product.no_of_users_rated = eachlink.text
            if(each_product.find('i', class_='a-icon-star-small')):
                starelement = each_product.find(
                    'i', class_='a-icon-star-small')
                product.rating = starelement.text.split(' ')[0]
                # if(eachlink.find('span',class_='a-price')):
                #    print(eachlink)
            if logging and product.name != "":
                print("Name:" + product.name + " Current Price:" + product.price + " Original Price:" + product.original_price +
                      " No of user rated:" + product.no_of_users_rated + " Rating:" + product.rating + " Website:" + product.url)
            if(product.name != ""):
                products.append(product)
            # return products
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

def main():
    print("amazon method")
    products = search("curved led screen")
    for p in products:
        print(p.__dict__)


if __name__ == "__main__":
    main()        
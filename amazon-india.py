import product_model
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import time

def startScrapping(product_name):
    products = []
    try:
        URL = 'https://www.amazon.in/s?k='+product_name
        response = requests.get(URL)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        results = BeautifulSoup(response.content, 'html.parser')
        product_elements = results.find_all('div', class_='s-result-item')
        for each_product in product_elements:
            product = product_model.Product
            all_links = each_product.find_all('a',class_='a-link-normal')
            for eachlink in all_links:
                if(eachlink.find('span',class_='a-size-medium')):
                    title_elem = eachlink
                    product.name = title_elem.text
                if(len(eachlink.find_all('span',class_="a-price"))>0):
                    all_prices = eachlink.find_all('span',class_="a-price")
                    if(len(all_prices)>0):
                        product.price = all_prices[0].text
                    if(len(all_prices)>1):
                        product.orginal_price = all_prices[1].text
                if(eachlink.find('span',class_='a-size-base')):
                    product.no_of_users_rated = eachlink
                #if(eachlink.find('span',class_='a-price')):
                #    print(eachlink)
            products.append(product)

        for eachp in products:
            print(eachp.json())       
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        time.sleep(60)
        startScrapping(product_name)
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        time.sleep(60)
        startScrapping(product_name)
    else:
        print('Success')
    


def main():
    print("amazon method")
    startScrapping("printer")

if __name__ == "__main__":
    main()  
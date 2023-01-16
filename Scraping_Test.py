'''Importing modules needed in the code, If some of them missing you can install it in on your environment'''
import string
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import re
import time
'''Feel Free to use other method or modules as you see fit'''

start_time = datetime.now()
'''Declaration of the columns that will be exported in excel file'''
columns_list = ["url","product_title","size","price","variation_id"]
result = pd.DataFrame(columns = columns_list)

'''Define the path to your input file'''
Links = pd.read_excel(r'input.xlsx')

candidates = input("Please input your name here : ")






'''This function is meant to get the query params'''
def get_url_query_params(url):
    if "?" in url:
        query_params = url.split("?")[1].split("&")
        query_params_map = { query_param.split("=")[0]: query_param.split("=")[1] for query_param in query_params}
        return query_params_map
    else:
        return {}

'''This function is meant to get the variation_id'''
def get_variation_id(url):
    # I supposed I had an url with the format www.domain.com/route?param1=value&param2=value2..
    # So I either find the variation id or i keep it blank there is no other place to extract it
    query_params = get_url_query_params(url)
    variation_id = query_params.get("variant") if "variant" in query_params else ""
    if not variation_id:
        print("variation id could not be found")
    return variation_id   




''' these functions are meant to create a chrome driver and close it'''
def get_driver():
    chrome_options = Options()
    #these arguments are meant to improve the scraping performance
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('disable-gpu')
    driver = webdriver.Chrome()
    return driver

def close_driver(driver):
    driver.close()



'''Function to extract different informations of the product'''
def do_task(iteration,driver):
    url = Links.iloc[iteration,0]
    driver.get(url)

    PRODUCT_CLASS_TAG = "product-main"
    PRODUCT_TITLE_CLASS_TAG = "product-title"
    PRODUCT_PRICE_CLASS_TAG = "price--main"
    PRODUCT_PRICE_SPAN_CLASS_TAG = "money"

    try:
        product = driver.find_element(By.CLASS_NAME,PRODUCT_CLASS_TAG)
        variation_id = get_variation_id(url)
        #simple element access with their class tag
        product_title = product.find_element(By.CLASS_NAME, PRODUCT_TITLE_CLASS_TAG).text
        price = product.find_element(By.CLASS_NAME, PRODUCT_PRICE_CLASS_TAG).find_element(By.CLASS_NAME,PRODUCT_PRICE_SPAN_CLASS_TAG).find_element(By.CLASS_NAME,PRODUCT_PRICE_SPAN_CLASS_TAG).text
        
        #use a regex expression to extract the title from the product element text since it is found in different element in the links.
        size = product.text.replace(' ',"")
        check_size = re.search("(\d)+x(\d)+",size)
        if bool(check_size):
            size = check_size.group()
        else:
            size = ""

        newline = [url,product_title,size,price,variation_id]

    except:
        #this exception is meant to treat the page not found and product not found links, 
        #so we simply add the line to the excel filewith just the link
        newline = [url,"product not available","","",""]
    return newline


if __name__ == "__main__":
    driver = get_driver()
    '''Use the function above to crawl for all links'''
    for iteration in range(len(Links)):
        print('on the {} link (total: {})'.format(iteration + 1, len(Links)))   
        output = do_task(iteration,driver)
        result.loc[len(result)] = output
    close_driver(driver)

    '''Exporting result to target folder'''
    end_time = datetime.now()
    timestr = time.strftime("%d.%m.%Y-%H%M%S")
    print('Duration: {}'.format(end_time - start_time))
    name = "Webshop_"+timestr+"_"+candidates
    result.to_excel(r'{}.xlsx'.format(name), index=False)  

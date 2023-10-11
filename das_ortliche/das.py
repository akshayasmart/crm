import re

import pandas as pd
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# # Set your Firefox binary path if needed
# firefox_binary_path = '/path/to/firefox/binary'
#
# # Create Firefox options
# options = Options()
# options.binary_location = firefox_binary_path
#
# # Create the Firefox WebDriver with options
# driver = webdriver.Firefox(options=options)
#
# # Define the base URL and start_urls
# base_url = 'https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom='
# start_urls = [f'{base_url}{page_number}' for page_number in range(1, 2)]  # Adjust the range as needed
#
# # Initialize lists to store data
# company_names = []
#
# for page_url in start_urls:
#     # Navigate to the current page
#     driver.get(page_url)
#     # ... (previous code)
#
#     # Find the elements containing company names using Selenium
#     partner_elements = driver.find_elements( By.CSS_SELECTOR , 'div.hit > h2 > a' )
#
#     # Extract company names from the current page
#     company_names.extend( [ element.text for element in partner_elements ] )
#
#
#     time.sleep(5)
#
# # Close the WebDriver
# driver.quit()
#
# # Create a DataFrame and save it to an Excel file
# data = {'Company Name': company_names}
# df = pd.DataFrame(data)
#
# excel_file = 'company_names.xlsx'
# df.to_excel(excel_file, index=False)
#
# print('Welcome')

# -------------------------------------------print one value-----------------------------------------------------------------------------------

#
# firefox_binary_path = '/path/to/firefox/binary'
#
# # Create Firefox options
# options = Options()
# options.binary_location = firefox_binary_path
#
# # Create the Firefox WebDriver with options
# driver = webdriver.Firefox(options=options)
# driver.get("https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom=1")
#
# # Initialize lists to store data
# company_data = []
#
# # Initialize variables
# page_number = 1
# max_pages = 2  # Change this to the maximum number of pages you want to scrape
#
# while page_number <= max_pages:
#     # Find the elements containing company names
#     partner_elements = driver.find_elements(By.CSS_SELECTOR, 'div.hit > h2 > a')
#     company_names = [element.text for element in partner_elements]
#
#     for company_name in company_names:
#
#         company_data.append({
#             'Company Name': company_name,
#             # Add other data fields here
#         })
#
#     # Increment the page number and construct the URL for the next page
#     page_number += 25
#     next_page_url = f"https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom={page_number}"
#
#     # Navigate to the next page
#     driver.get(next_page_url)
#
#     # Wait for a few seconds before navigating to the next page (adjust as needed)
#     time.sleep(5)
#
# # Close the WebDriver
# driver.quit()
#
# # Create a DataFrame and save it to an Excel file
# df = pd.DataFrame(company_data)
# excel_file = 'company_data.xlsx'
# df.to_excel(excel_file, index=False)
#
# print('Welcome')
#---------------------------------------pagenation----------------------------------------------
#
#
# # Set the path to the Firefox binary
# firefox_binary_path = '/path/to/firefox/binary'
#
# # Create Firefox options
# options = Options()
# options.binary_location = firefox_binary_path
#
# # Create the Firefox WebDriver with options
# driver = webdriver.Firefox(options=options)
# driver.get("https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom=1")
#
# # Initialize lists to store data
# company_data = []
#
# # Initialize variables
# max_pages = 2  # Change this to the maximum number of pages you want to scrape
#
# for page_number in range(1, max_pages + 1):
#     # Find the elements containing company names
#     partner_elements = driver.find_elements( By.XPATH , '//div[contains(@class, "hit")]//h2/a' )
#
#     company_names = [element.text for element in partner_elements]
#
#     for company_name in company_names:
#
#         company_data.append({
#             'Company Name': company_name,
#             # Add other data fields here
#         })
#
#     if page_number < max_pages:
#         # Increment the page number by 1
#         page_number += 25
#
#         # Construct the URL for the next page
#         next_page_url = f"https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom={page_number}"
#
#         # Navigate to the next page
#         driver.get(next_page_url)
#
#         # Wait for a few seconds before navigating to the next page (adjust as needed)
#         time.sleep(5)
#
# # Close the WebDriver
# driver.quit()
#
# # Remove duplicate entries from company_data
# company_data = [dict(t) for t in {tuple(d.items()) for d in company_data}]
#
# # Create a DataFrame and save it to an Excel file
# df = pd.DataFrame(company_data)
# excel_file = 'data.xlsx'
# df.to_excel(excel_file, index=False)
#
# print('Welcome')
#



#
# firefox_binary_path = '/path/to/firefox/binary'
#
# # Create Firefox options
# options = Options()
# options.binary_location = firefox_binary_path
#
# # Create the Firefox WebDriver with options
# driver = webdriver.Firefox(options=options)
# driver.get("https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom=1")
#
# # Initialize lists to store data
# company_data = []
#
# # Initialize variables
# page_number = 1
# max_pages = 2  # Change this to the maximum number of pages you want to scrape
#
# while page_number <= max_pages:
#     # Find the elements containing company names
#     partner_elements = driver.find_elements(By.CSS_SELECTOR, 'div.hit > h2 > a')
#     company_names = [element.text for element in partner_elements]
#
#     for company_name in company_names:
#
#         company_data.append({
#             'Company Name': company_name,
#             # Add other data fields here
#         })
#
#     # Increment the page number and construct the URL for the next page
#     page_number += 25
#     next_page_url = f"https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom={page_number}"
#
#     # Navigate to the next page
#     driver.get(next_page_url)
#
#     # Wait for a few seconds before navigating to the next page (adjust as needed)
#     time.sleep(5)
#
# # Close the WebDriver
# driver.quit()
#
# # Create a DataFrame and save it to an Excel file
# df = pd.DataFrame(company_data)
# excel_file = 'company_data.xlsx'
# df.to_excel(excel_file, index=False)
#
# print('Welcome')
#---------------------------------------pagenation----------------------------------------------
#
#
# # Set the path to the Firefox binary
# firefox_binary_path = '/path/to/firefox/binary'
#
# # Create Firefox options
# options = Options()
# options.binary_location = firefox_binary_path
#
# # Create the Firefox WebDriver with options
# driver = webdriver.Firefox(options=options)
# driver.get("https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom=1")
#
# # Initialize lists to store data
# company_data = []
#
# # Initialize variables
# max_pages = 2  # Change this to the maximum number of pages you want to scrape
#
# for page_number in range(1, max_pages + 1):
#     # Find the elements containing company names
#     partner_elements = driver.find_elements( By.XPATH , '//div[contains(@class, "hit")]//h2/a' )
#
#     company_names = [element.text for element in partner_elements]
#
#     for company_name in company_names:
#
#         company_data.append({
#             'Company Name': company_name,
#             # Add other data fields here
#         })
#
#     if page_number < max_pages:
#         # Increment the page number by 1
#         page_number += 25
#
#         # Construct the URL for the next page
#         next_page_url = f"https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom={page_number}"
#
#         # Navigate to the next page
#         driver.get(next_page_url)
#
#         # Wait for a few seconds before navigating to the next page (adjust as needed)
#         time.sleep(5)
#
# # Close the WebDriver
# driver.quit()
#
# # Remove duplicate entries from company_data
# company_data = [dict(t) for t in {tuple(d.items()) for d in company_data}]
#
# # Create a DataFrame and save it to an Excel file
# df = pd.DataFrame(company_data)
# excel_file = 'data.xlsx'
# df.to_excel(excel_file, index=False)
#
# print('Welcome')



# Set your Firefox binary path if needed
firefox_binary_path = '/path/to/firefox/binary'

# Create Firefox options
options = Options()
options.binary_location = firefox_binary_path

# Create the Firefox WebDriver with options
driver = webdriver.Firefox(options=options)

start_page = 1
end_page = 3

# Define the base URL and start_urls
base_url = 'https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom='
start_urls = [f'{base_url}{start_page + 25 * i}' for i in range(end_page - start_page + 1)]

# Initialize lists to store data
company_data = []
phone_numbers = []
sublines = []

for page_url in start_urls:
    # Navigate to the current page
    driver.get(page_url)

    # Find the elements containing company names using Selenium
    partner_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "hit ")]//h2/a')
    category_elements = driver.find_elements(By.XPATH, '//div[@class="left"]/div[@class="category"]')

    hit_divs = driver.find_elements(By.CSS_SELECTOR, 'div[class="hit "]')


    for i, (partner_element, category_element, hit_div) in enumerate(zip(partner_elements, category_elements, hit_divs)):
        try:
            company_name = partner_element.text.strip()
            category_name = category_element.text.strip()

            # Extract the address information
            address_element = hit_div.find_element(By.XPATH, './/address')
            address_text = address_element.text.strip()
            address_parts = [part.strip() for part in re.split(r'[,\n]', address_text) if part.strip()]


            street = ""
            city = ""
            directions = ""

            if len(address_parts) >= 1:
                street = address_parts[0]
            if len(address_parts) >= 2:
                city = address_parts[1]
            if len(address_parts) >= 3:
                directions = address_parts[2]

            # Use Selenium to find the phone number within each "hit" div
            phone_number_element = hit_div.find_element(By.XPATH, './/div[@class="phoneblock"]//span')
            phone_number = phone_number_element.text.strip()
            try :
                subline_element = hit_div.find_element( By.XPATH , './/div[@class="subline"]' )
                subline = subline_element.text.strip( )
            except NoSuchElementException :
                subline = ""

            company_data.append({
                'Company Name': company_name,
                'Category': category_name,
                'Phone Number': phone_number,
                'Street': street,
                'City': city,
                'Directions': directions,
                'Subline' : subline ,
                # Add other data fields here
            })
        except NoSuchElementException:
            pass  # Handle missing data

    time.sleep(5)

# Close the WebDriver
driver.quit()

# Create a DataFrame and save it to an Excel file
df = pd.DataFrame(company_data)
excel_file = 'company_data.xlsx'
df.to_excel(excel_file, index=False)

print('Welcome')







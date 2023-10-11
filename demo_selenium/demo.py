
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


# Set the path to the Firefox binary
firefox_binary_path = '/path/to/firefox/binary'

# Create Firefox options
options = Options()
options.binary_location = firefox_binary_path

# Create the Firefox WebDriver with options
driver = webdriver.Firefox(options=options)
driver.get("https://www.odoo.com/partners/country/india-101/page/1")

# Initialize lists to store data
company_data = []

# Initialize variables
page_number = 1
max_pages = 2  # Change this to the maximum number of pages you want to scrape

while page_number <= max_pages:
    # Navigate to the current page
    page_url = f"https://www.odoo.com/partners/country/india-101/page/{page_number}"
    driver.get(page_url)

    # Find the elements containing company names and their URLs
    company_elements = driver.find_elements(By.XPATH, '//div[@class="flex-grow-1 o_partner_body"]/a/span')
    company_names = [element.text for element in company_elements]
    country_elements = driver.find_elements(By.XPATH, '//div[@class="flex-grow-1 o_partner_body"]/a/span')
    company_links = [element.find_element(By.XPATH, '..').get_attribute('href') for element in country_elements]

    # Extract company names and addresses from their respective pages
    for company_name, link in zip(company_names, company_links):
        driver.get(link)
        country_name_element = driver.find_element(By.XPATH, '//span[contains(@class, "w-100 d-block")]')
        country_name = country_name_element.text

        try:
            company_address_element = driver.find_element( By.XPATH , '//span[contains(@class, "w-100")]' )
            company_address_text = company_address_element.text.replace( '\n' , ', ' )

            # Split the address into street1, street2, city, and state
            address_parts = company_address_text.split( ', ' )
            street1 = ', '.join(address_parts[0:2])
            street2 = ', '.join(address_parts[2:5])  if len( address_parts ) > 1 else ''
            city = address_parts [ -3 ] if len( address_parts ) > 2 else ''
            state = address_parts [ -2 ] if len( address_parts ) > 3 else ''

            phone_number_element = driver.find_element( By.XPATH , '//span[contains(@class, "o_force_ltr")]' )
            phone_number = phone_number_element.text.replace( '\n' , ', ' )

            website_element = driver.find_element( By.XPATH , '//i[@class="fa fa-globe"]/following-sibling::a/span[@itemprop="website"]' )
            website_url = website_element.text.replace( '\n' , ', ' )

            email_element = driver.find_element( By.XPATH ,    '//span[@itemprop="email"]' )
            email = email_element.text.replace( '\n' , ', ' )

            reference_elements = driver.find_elements( By.XPATH , '//div[@class="flex-grow-1"]/a/span' )
            references = [ element.text for element in reference_elements ]



        except NoSuchElementException:
            pass

        company_data.append( {
            'Company Name' : company_name ,
            'Country' : country_name ,
            'Street1' : street1 ,
            'Street2' : street2 ,
            'City' : city ,
             'State' : state,
            'Phone Number' : phone_number,
            'Website' : website_url,
            'Email' : email,
            'References' : references
        } )

    # Increment the page number
    page_number += 1

    # Wait for a few seconds before navigating to the next page (adjust as needed)
    time.sleep(5)

# Close the WebDriver
driver.quit()

# Create a DataFrame and save it to an Excel file
df = pd.DataFrame(company_data)
excel_file = 'company_data.xlsx'
df.to_excel(excel_file, index=False)

print('Welcome')

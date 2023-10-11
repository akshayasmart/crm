import pandas as pd
import time
import re
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Set your Firefox binary path if needed
firefox_binary_path = '/path/to/firefox/binary'

# Create Firefox options
options = Options()
options.binary_location = firefox_binary_path

# Create the Firefox WebDriver with options
driver = webdriver.Firefox(options=options)

start_page = 1
end_page = 20

# Define the base URL and start_urls
base_url = 'https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom='
start_urls = [f'{base_url}{start_page + 25 * i}' for i in range(end_page - start_page + 1)]

# Initialize lists to store data
company_data = []
sublines = []  # New list to store sublines

for page_url in start_urls:
    # Navigate to the current page
    driver.get(page_url)

    # Find the elements containing company names using Selenium
    partner_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "hit ")]//h2/a')
    category_elements = driver.find_elements(By.XPATH, '//div[@class="left"]/div[@class="category"]')
    hit_divs = driver.find_elements(By.CSS_SELECTOR, 'div[class="hit "]')

    for i, (partner_element, category_element, hit_div) in enumerate(zip(partner_elements, category_elements, hit_divs)):
        try:
            # Use Selenium to find the phone number within each "hit" div
            phone_number_element = hit_div.find_element(By.XPATH, './/div[@class="phoneblock"]//span')
            phone_number = phone_number_element.text.strip()
        except NoSuchElementException:
            phone_number = ""

        try:
            # Use Selenium to find the subline within each "hit" div
            subline_element = hit_div.find_element(By.XPATH, './/div[@class="subline"]')
            subline = subline_element.text.strip()
        except NoSuchElementException:
            subline = ""

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

        company_name = partner_element.text.strip()
        category_name = category_element.text.strip()

        company_data.append({
            'Company Name': company_name,
            'Category': category_name,
            'Phone Number': phone_number,
            'Street': street,
            'City': city,
            'Directions': directions,
            'Subline': subline,
        })

        # Append subline to the sublines list
        sublines.append(subline)

        time.sleep(5)

# Close the WebDriver
driver.quit()

# Add the 'Subline' data to the DataFrame
for i, data in enumerate(company_data):
    data['Subline'] = sublines[i]

# Create a DataFrame and save it to an Excel file
df = pd.DataFrame(company_data)
excel_file = 'company_data.xlsx'
df.to_excel(excel_file, index=False)

print('Welcome')

import scrapy
import pandas as pd
import time
import requests


class Categories(scrapy.Spider):
    name = 'categories'
    page_number = 1751  # Start from page 1
    max_page = 1776  # Assuming you want to crawl up to page 51
    base_url = 'https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom='
    start_urls = [f'{base_url}{page_number}']


    def __init__(self, *args, **kwargs):
        super(Categories, self).__init__(*args, **kwargs)
        self.partner_category_mapping = {}  # Initialize a dictionary to store partner-category pairs
        self.last_request_time = time.time()
    def parse(self, response):
        time_elapsed = time.time() - self.last_request_time

        # If less than 2 minutes have passed, wait for the remaining time
        if time_elapsed > 120:
            wait_time = 120 - time_elapsed
            self.logger.info(f"Waiting for {wait_time} seconds before the next request...")
            time.sleep(wait_time)
        self.last_request_time = time.time()
        # Extract partner names, addresses, and their corresponding categories
        partner_elements = response.css('div[class="hit "]>h2>a')
        category_elements = response.css('div[class="left"]>div[class="category"]')
        address_elements = response.xpath('//div[@class="hit "]//address')  # Select all <address> elements

        partners = [partner.css('::text').get().strip() for partner in partner_elements]
        categories = [category.css('::text').get().strip() for category in category_elements]

        # address_elements = response.xpath('//div[@class="hit "]//address')
        street_column = []
        city_column = []
        directions_colum = []
        for address_element in address_elements:
            # Extract all text within <address> and clean it
            address_text = ','.join(address_element.css('::text').extract()).strip()

            # Split the address into parts based on comma (,) or other separators as needed
            parts = address_text.split(',')

            # Initialize address parts
            street = ""
            city = ""
            directions = ""

            if len(parts) >= 1:
                street = parts[0].strip()
            if len(parts) >= 2:
                city = parts[1].strip()
            if len(parts) >= 3:
                directions = parts[2].strip()

            # Append address parts to respective columns
            street_column.append(street)
            city_column.append(city)
            directions_colum.append(directions)

        # Extract and clean the addresses
        # addresses = []
        # for address_element in address_elements:
        #     address_text = ''.join(address_element.css('::text').extract())  # Get all text within <address>
        #     address_text = ' '.join(address_text.split())  # Remove extra spaces and line breaks
        #     addresses.append(address_text)

        sublines = []
        hit_divs = response.css('div[class="hit "]')

        for hit_div in hit_divs:
            # Use a CSS selector to extract the subline within each "hit" div
            link = hit_div.css('div.subline::text').get()

            if link:
                # You can print or process the subline here
                sublines.append(link.strip())
            else:
                sublines.append(" ")

        phone_numbers = []

        hit_phone = response.css('div[class="hit "]')

        for hit_div in hit_phone:
            # Use a CSS selector to extract the phone number within each "hit" div
            phone_number = hit_div.css('div.phoneblock span::text').get()

            if phone_number:
                # Add the phone number to the list
                phone_numbers.append(phone_number.strip())
            else:
                phone_numbers.append(" ")

        # Create a DataFrame for the current page's data
        data = {
            'Partner': partners,
            'Sub Lines': sublines,
            'Category': categories,
            'Street1': street_column,
            'Street2': city_column,
            'City': directions_colum,
            'Phone': phone_numbers
        }
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()

        # Save the DataFrame to an Excel file for the current page
        df.to_excel(f'output_{self.page_number}.xlsx', index=False)

        if self.page_number == 51:
            self.logger.info("Skipping extra content on page 51")
            self.page_number += 25
            next_page = f'{self.base_url}{self.page_number}'
            yield response.follow(next_page, callback=self.parse)
            return

        # Check if there's a next page to crawl
        if self.page_number < self.max_page:
            self.page_number += 25
            time.sleep(60)
            next_page = f'{self.base_url}{self.page_number}'
            yield response.follow(next_page, callback=self.parse)

    # def parse(self, response):
    #     # Extract partner names and their corresponding categories
    #     partner_elements = response.css('a.hitlnk_name')
    #     partners = [partner.css('::text').get().strip() for partner in partner_elements]
    #     category_elements = response.css('div.category')
    #     categories = [category.css('::text').get().strip() for category in category_elements]
    #     address_element = response.css('address')
    #     address = [address.css('::text').get().strip() for address in address_element]
    #     # address = ' '.join([line.strip() for line in address_lines if line.strip()])
    #
    #     # Create a DataFrame for the current page's data
    #     data = {
    #         'partners': partners,
    #         'Category': categories,
    #         'Address': address
    #     }
    #     df = pd.DataFrame.from_dict(data, orient='index')
    #     df = df.transpose()
    #
    #     # Save the DataFrame to an Excel file for the current page
    #     df.to_excel(f'output_{self.page_number}.xlsx', index=False)
    #
    #     # Check if there's a next page to crawl
    #     if self.page_number < self.max_page:
    #         self.page_number += 25
    #         next_page = f'{self.base_url}{self.page_number}'
    #         yield response.follow(next_page, callback=self.parse)


# class Categories(scrapy.Spider):
#     name = 'categories'
#     page_number = 1 # Assuming you want to crawl up to page 51
#     start_urls = [f'https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom=1']
#
#     def parse(self, response):
#         # Extract partner names and their corresponding categories
#         partner_elements = response.css('a.hitlnk_name')
#         partners = [partner.css('::text').get().strip() for partner in partner_elements]
#         category_elements = response.css('div.category')
#         categories = [category.css('::text').get().strip() for category in category_elements]
#
#
#         # Check if there's a next page to crawl
#
#             # Create a DataFrame and save all categories to a single Excel file
#         data = {
#                 'partners': partners,
#                 'Category': categories
#             }
#         df = pd.DataFrame.from_dict(data, orient='index')
#         df = df.transpose()
#         df.to_excel(f'output_{self.page_number}.xlsx', index=False)
#
#         # Check if there's a next page to crawl
#         next_page = f'https://www.dasoertliche.de/?zvo_ok=0&buc=2249&plz=&quarter=&district=&ciid=&kw=Sport%C3%A4rzte&ci=&kgs=&buab=71100098&zbuab=&form_name=search_nat&recFrom={self.page_number}'
#         if self.page_number <= 26:  # Assuming you want to crawl up to page 51 (25 items per page)
#             self.page_number += 25
#             yield response.follow(next_page, callback=self.parse)


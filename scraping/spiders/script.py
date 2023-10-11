

import scrapy
import pandas as pd
import time



class scrapy(scrapy.Spider):
    name= 'crawler'
    page_number = 1
    start_urls = ['https://www.odoo.com/partners/country/united-states-224/page/1']

    def __init__(self , *args , **kwargs) :
        super( scrapy , self ).__init__( *args , **kwargs )
        self.partner_span_mapping = {}
        self.last_request_time = time.time( )  # Initialize the last request time

    def parse(self , response) :
        # Calculate the time elapsed since the last request
        time_elapsed = time.time( ) - self.last_request_time

        # If less than 2 minutes have passed, wait for the remaining time
        if time_elapsed > 120 :
            wait_time = 120 - time_elapsed
            self.logger.info( f"Waiting for {wait_time} seconds before the next request..." )
            time.sleep( wait_time )

        # Update the last request time
        self.last_request_time = time.time( )

        # Extract partner details and links to other pages
        partner_elements = response.css( 'div[class="flex-grow-1 o_partner_body"]>a> span' )
        partner = [ partner.css( '::text' ).get( ) for partner in partner_elements ]
        link_to_other_page = response.css( 'div[class="flex-grow-1 o_partner_body"] >a::attr(href)' ).getall( )

        # Iterate through link_to_other_page and follow each link
        for i , link in enumerate( link_to_other_page ) :
            yield response.follow( link , callback=self.parse_other_page , cb_kwargs={'partner' : partner [ i ]} )

        next_page = 'https://www.odoo.com/partners/country/united-states-224/page/' + str( self.page_number ) + '/'
        if self.page_number <= 4 :
            self.page_number += 1

            # Sleep for 1 minute (60 seconds)
            time.sleep( 60 )

            yield response.follow( next_page , callback=self.parse )

    def parse_other_page(self , response , partner) :
        # Extract the value from the <span> tag with the specified class
        span_value = response.css( 'span.w-100 ::text' ).getall( )
        span_phone = response.css( 'span.o_force_ltr ::text' ).getall( )
        website = response.xpath(
            '//div/i[@class="fa fa-globe"]/following-sibling::a/span[@itemprop="website"]/text()' ).get( )
        email = response.css( 'span[itemprop="email"]::text' ).get( )
        span_reference = response.css( 'div[class="flex-grow-1"]>a>span' )
        reference = [ reference.css( '::text' ).get( ) for reference in span_reference ]

        # Associate span_value with the corresponding partner
        if partner not in self.partner_span_mapping :
            self.partner_span_mapping [ partner ] = {'value' : [ ] , 'phone' : [ ] , "references" : [ ] ,
                                                     'website' : '' ,
                                                     'email' : ''}

        self.partner_span_mapping [ partner ] [ 'value' ].extend( span_value )
        self.partner_span_mapping [ partner ] [ 'phone' ].extend( span_phone )
        self.partner_span_mapping [ partner ] [ 'website' ] = website
        self.partner_span_mapping [ partner ] [ 'email' ] = email
        self.partner_span_mapping [ partner ] [ 'references' ].append( reference )

    def closed(self , reason) :
        # Create a DataFrame that includes Partner and Span Value
        data = {'Partner' : [ ] , 'Street 1' : [ ] , 'Street 2' : [ ] , 'City' : [ ] , 'State' : [ ] , 'country' : [ ] ,
                'Phone' : [ ] , 'Website' : [ ] , 'Email' : [ ] , 'References' : [ ]}
        for partner , values in self.partner_span_mapping.items( ) :
            data [ 'Partner' ].append( partner )
            data [ 'Street 1' ].append( ', '.join( values [ 'value' ] [ 0 :1 ] ) if values [ 'value' ] else '' )
            data [ 'Street 2' ].append( ', '.join( values [ 'value' ] [ 1 :2 ] ) if values [ 'value' ] else '' )
            data [ 'City' ].append( ', '.join( values [ 'value' ] [ -3 :-2 ] ) if values [ 'value' ] else '' )
            data [ 'State' ].append( ', '.join( values [ 'value' ] [ -2 :-1 ] ) if values [ 'value' ] else '' )
            data [ 'country' ].append( values [ 'value' ] [ -1 ] if values [ 'value' ] else '' )
            data [ 'Phone' ].append( ', '.join( values [ 'phone' ] ) )
            data [ 'Website' ].append( values [ 'website' ] )  # Add the website value
            data [ 'Email' ].append( values [ 'email' ] )
            references = [ str( ref ) for ref in values [ 'references' ] ]
            data [ 'References' ].append( ', '.join( references ) )

        df = pd.DataFrame( data )

        excel_file = 'output.xlsx'
        df.to_excel( excel_file , index=False )


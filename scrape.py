#!/usr/bin/python
import sys
import csv
from lxml import html
import requests

class Scrape:

    def amazon_scrape(user_query):
        service_name = "amazon"
        Scrape.run_scrape(service_name,user_query)

    def newegg_scrape(user_query):
        service_name = "newegg"

        Scrape.run_scrape(service_name,user_query)
    def ebay_scrape(user_query):
        service_name = "ebay"
        Scrape.run_scrape(service_name,user_query)

    def amazon_rerun(user_query,service_name):
        Scrape.amazon_scrape(user_query)
        
    # run the actual scrape using ifs for the different site providers.
    def run_scrape(service_name,user_query):
        if(service_name == "amazon"):
            page = requests.get("https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+user_query)
            tree = html.fromstring(page.content)

            product_title = tree.xpath('//h2[@class="a-size-medium s-inline  s-access-title  a-text-normal"]/text()')
            product_price = tree.xpath('//span[@class="a-offscreen"]/text()')
            if len(product_title) == 0: # test to see if the list is empty, aka a response 503 received from Amazon
                service_name = "amazon"
                Scrape.amazon_rerun(user_query,service_name) # restart the scrape

            Program.print_scrape(product_title,product_price)

        if(service_name == "newegg"):
            page = requests.get("https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description="+user_query+"&N=-1&isNodeId=1")
            tree = html.fromstring(page.content)

            product_title = tree.xpath('//a[@title="View Details"]/text()')
            product_price = tree.xpath('//span[@style="display: none"]/text()')

            Program.print_scrape(product_title,product_price)

        if(service_name == "ebay"):
            page = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR11.TRC1.A0.H0.Xr7+170.TRS0&_nkw="+user_query+"&_sacat=0")
            tree = html.fromstring(page.content)

            product_title = tree.xpath('//a[@class="vip"]/text()')
            product_price = tree.xpath('//span[@class="bold"]/text()')

            # Below 2 commands are workarounds. Ebay scrape is causing these characters to appear, so this removes them
            # until a better solution is found.
            product_title = [s.strip('\r\n\t\t') for s in product_title]
            product_price = [s.strip('\n\t\t\t\t\t') for s in product_price]

            Program.print_scrape(product_title,product_price)
                 
class Program:
	# where the main program runs
    def main(user_query):
        print("---------------AMAZON---------------\n")
        Scrape.amazon_scrape(user_query)
        print("\n")
        print("---------------NEWGG---------------\n")
        Scrape.newegg_scrape(user_query)
        print("\n")
        print("---------------EBAY---------------\n")
        Scrape.ebay_scrape(user_query)
        # force an exit, the program tends to run the program a second time.
        sys.exit()

    def print_scrape(product_title,product_price):
        # Reduce number of characters in product_title to 60 because the product names can get rather long.
        product_title = [item[:60] for item in product_title]
        product_price = [s.strip('$') for s in product_price]
        product_price = [s.strip('|') for s in product_price]
        product_price = [s.strip('Facebook') for s in product_price]
        product_price = [s.strip('Twitter') for s in product_price]
        product_price = [s.strip('Instagram') for s in product_price]
        product_price = [s.strip('Google') for s in product_price]
        product_price = [s.strip('Pinterest') for s in product_price]
        product_price = [x for x in product_price if x]

        # Have the two lists display vertically, so you can actually read the results properly.
        for product_title, product_price in zip(product_title,product_price):
            try:
                float(product_price)
            except ValueError:
                pass

            # Put both lists into a single variable
            compiled_data = product_title,product_price
            #print(compiled_data[:2])
            print(compiled_data)
            #Math.min_price(product_price)
            
class Math: 
    def min_price(product_price):
        #sorted(product_price, reverse=True)
        sorted(product_price, reverse=True)
        print(product_price)
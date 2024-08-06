import hashlib
import os
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.cmdline import execute

from dominos_store_locator.items import DominosStoreLocatorItem


# def page_checker(url:str, method:str, directory_path:str):
#     # Checking if page exists
#     # If Saved Page exists, reading it
#     if os.path.exists(path=directory_path):
#             with open('', 'rb') as file:
#                 body = file.read()
#                 return body
#     # If Saved Page does not exist, saving it
#     else:
#         with open(file=directory_path, mode='rb') as file:
#             body = file.read()
#         return body

def get_location_divs(response):
    location_divs = response.xpath('//div[@class="store-info-box"]')
    return location_divs


def get_area(location_div):
    area = location_div.xpath('./ul/li[not(@class)]/div[@class="info-text"]/text()')[0].get().strip()
    # print('Area:', area)
    return area


def get_address(location_div):
    address = ' '.join(location_div.xpath('./ul/li[@class="outlet-address"]/div[@class="info-text"]//text()').getall()).replace('  ', ' ').strip()
    # print('Address:', address)
    return address


def get_landmark(location_div):
    landmark = location_div.xpath('./ul/li[not(@class)]/div[@class="info-text"]/text()')
    landmark = landmark[1].get().strip() if len(landmark) > 1 else 'N/A'
    # print('Landmark:', landmark)
    return landmark


def get_phone(location_div):
    phone = location_div.xpath('./ul/li[@class="outlet-phone"]/div[@class="info-text"]/a/text()').get().strip()
    # print('Phone:', phone)
    return phone


def get_open_until(location_div):
    open_until = location_div.xpath('./ul/li[@class="outlet-timings"]/div[@class="info-text"]/span/text()').get().replace('Open until ', '').strip()
    # print('Open Until:', open_until)
    return open_until


def get_map_url(location_div):
    map_url = location_div.xpath('./ul/li[@class="outlet-actions"]/a[contains(@class, "btn-map")]/@href').get().strip()
    # print('Map url:', map_url)
    return map_url


def get_site_url(location_div):
    site_url = location_div.xpath('./ul/li[@class="outlet-actions"]/a[contains(@class, "btn-website")]/@href').get().strip()
    # print('Site url:', site_url)
    return site_url


class StoreLocatorSpider(scrapy.Spider):
    name = "store_locator"
    start_urls = ["https://stores.dominos.co.in/"]
    allowed_domains = ["stores.dominos.co.in"]


    def parse(self, response):
        # dir_project_files = os.path.join(r'C:\Project Files (using Scrapy)', 'Dominos', '_Project_Files')
        # filename = hashlib.sha256(response.url).hexdigest()

        # Creating an instance of Item Class
        store_data = DominosStoreLocatorItem()

        # Retrieving location divs for extracting data from each of them
        locations_divs = get_location_divs(response=response)
        for location in locations_divs:
            store_data['area'] = get_area(location)
            store_data['address'] = get_address(location)
            store_data['landmark'] = get_landmark(location)
            store_data['phone'] = get_phone(location)
            store_data['open_until'] = get_open_until(location)
            store_data['map_url'] = get_map_url(location)
            store_data['site_url'] = get_site_url(location)

            yield store_data

        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse)
            # print('\n\n\n')


if __name__ == '__main__':
    execute('scrapy crawl store_locator'.split())

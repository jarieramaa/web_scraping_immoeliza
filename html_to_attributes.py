"""
This module reads immoweb -property ads using beautiful soup. It
extracts item specific information from tables for example 'building year',
'number of rooms', 'surface area', 'price' and 'postal code'
"""

from nturl2path import url2pathname
import sys
import bs4 as bs
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import serialize_lists
import re
import read_selenium_data


class ImmowebSoup:
    """This class reads information from immoweb properties and
    stores them to a file as a dictonary. Information includes
    the price, postal_code, immoweb_id and content of all the 
    tables. This is "raw" data and meant to be process further. 
    """

    _compiled_post_code = re.compile("(/[0-9]{4}/)")
    _compiled_immoweb_id = re.compile("(/[0-9]+\?)")
    _compiled_price = re.compile("[0-9]+")

    def __init__(self, selenium_list, filename) -> None:
        """Constructor """
        self._my_dictionary = {}
        self._selenium_list = selenium_list
        self._result_list = []
        self._my_dictionary = {}
        self._filename = filename

    def _read_html_code(self, url, compiled_code):
        postal_code = compiled_code.findall(url)
        if postal_code == None or len(postal_code) == 0:
            return ""
        postal_code = postal_code[0].replace("/", "")
        postal_code = postal_code.replace("?", "")
        return postal_code

    def _make_HTTP_request(self, url_address) -> object:
        r = requests.get(url_address)
        return r

    def _initialize_soup(self, r: object) -> object:
        self._soup = BeautifulSoup(r.text, 'lxml')
        classifield_table = self._soup.find_all('table',
                                                class_='classified-table')
        return classifield_table

    def _read_price(self, r) -> list:
        """ Reads immoweb price. This is used to identify properties.
        There might be two prices: 'normal price' and 'sr-only'. Normally,
        they are same.
        :r: A Beautiful Soup response
        :return: list of prices found"""
        soup = BeautifulSoup(r.text, 'lxml')
        return_list = []
        code_info = soup.find('p', class_="classified__price")
        print("CODE INFO:", code_info)
        price_text = str(code_info).replace(":", "")
        price_text = price_text.replace(" ", "")
        price_text = price_text.replace("€", "")
        price_text = price_text.replace(",", "")
        prices = ImmowebSoup._compiled_price.findall(price_text)
        result_price = []
        if len(prices) > 0:
            for i in prices:
                cleaned_price = str(i).replace(">", "").replace("<", "")
                print("PRICE:", cleaned_price)
                result_price.append(cleaned_price)
        else:
            return [str(code_info)]
        return result_price

    def price_test(self):
        print("Price test started!!")
        url_address = "https://www.immoweb.be/en/classified/town-house/for-sale/kraainem/1950/9675986?searchId=61f83a2b0f96b"
        r = self._make_HTTP_request(url_address)
        self._read_price(r)

    def _read_classifield_table(self, temp_dictionary, classifield_table):
        """Uses BeaurifulSoup library to read websites from ImmoWeb
        :classifield_table: """
        for info in classifield_table.find_all('tbody'):
            rows = info.find_all('tr')
            print("-" * 100)
            for row in rows:
                if not row.find_all('th', class_='classified-table__header'):
                    print("=====> Header missing!")
                    continue
                if not row.find_all('td', class_='classified-table__data'):
                    print("=====> Data missing!")
                    continue
                detail_header = row.find(
                    'th',
                    class_='classified-table__header').contents[0].strip()
                detail_data = row.find(
                    'td', class_='classified-table__data').contents[0].strip()
                if not detail_data or not detail_header:
                    print(
                        "=====> Detail data or header is missing <=====    header:",
                        detail_header, ",  data:", detail_data)
                else:
                    print(detail_header, "/", detail_data)
                    temp_dictionary[detail_header] = detail_data

    def _write_log(self, place: str, url: str, message: str,
                   variable: str) -> None:
        log_line = str("-" * 100)
        log_message = f"\nPLACE: {place} \nMESSAGE: {message}\nVARIABLE: {variable}\nURL: {url}"
        with open('html_to_attributes.log', "a") as my_log_file:
            my_log_file.write(log_line)
            my_log_file.write(log_message)

    def main(self):
        for list_row in self._selenium_list:  #bunch of lists should be checked
            url_address = list_row[2]
            r = self._make_HTTP_request(url_address)
            print("LIST ROW:", list_row)
            tmp_dictonary = self._my_dictionary.copy()
            tmp_dictonary["Immoweb ID"] = self._read_html_code(
                url_address, ImmowebSoup._compiled_immoweb_id)
            tmp_dictonary["Property type"] = list_row[0]
            tmp_dictonary["property sub-type"] = list_row[1]
            price_list = self._read_price(r)
            if len(price_list) > 0:
                tmp_dictonary["Price"] = price_list[0]
            else:
                self._write_log("main() - LOG:1", url_address,
                                "len(price_list) == 0", str(price_list))
            if len(price_list) > 1:
                tmp_dictonary["Price (sr only)"] = price_list[1]
            tmp_dictonary["Post code"] = self._read_html_code(
                url_address, ImmowebSoup._compiled_post_code)
            classifield_table = self._initialize_soup(r)
            for one_table in classifield_table:
                self._read_classifield_table(tmp_dictonary, one_table)
            tmp_dictonary["url address"] = url_address
            print("HTML ADDRESS:", url_address)

            self._result_list.append(tmp_dictonary)
        for list_row in self._result_list:
            print("RESULT:", list_row)
        serialize_lists.write_dump(self._result_list, self._filename)


#file_to_read = "HOUSE_TOWN_HOUSE.txt"  #<== CHANGE THIS!!!!
#tmp_list = read_selenium_data.read_file(file_to_read)
#tmp_list = selenium_list

if __name__ == "__main__":
    file_to_read = str(sys.argv[1])  #<== THIS IS THE FILE NAME
    tmp_list = read_selenium_data.read_file(file_to_read)
    file_to_write = file_to_read.replace(".txt", ".attributes")
    my_obj = ImmowebSoup(tmp_list, f"./data/{file_to_write}")
    my_obj.main()

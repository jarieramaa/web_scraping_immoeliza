import time
import os

from curses import KEY_DOWN, KEY_ENTER
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import read_selenium_data
from threading import Thread, RLock
import serialize_lists


class Read_Address:

    _driver = webdriver.Firefox()

    def _open_web_page(self, url: str) -> None:
        """ Open a web page
        :url: web address
        """
        self._driver.implicitly_wait(2)
        self._driver.get(url)

    def _read_address(self) -> str:
        """ Reads the address from the website
        :return: String that conteins the address
        """
        prop_location = self._driver.find_elements(
            By.XPATH, '//div[@class="classified__information--address"]')
        if prop_location == None or len(prop_location) == 0:
            return ""
        return prop_location[0].text

    def _read_price(self) -> str:
        """ 
        Reads the price from the website
        :return: price as a string
        """
        prop_price_list = self._driver.find_elements(
            By.XPATH, '//p[@class="classified__price"]')  #.text.split("\n")
        if prop_price_list == None or len(prop_price_list) == 0:
            return ""
        raw_prop_price = prop_price_list[0].text.split("\n")[0]

        return raw_prop_price

    def _accept_cookies(self) -> None:
        """In the website has a dialog that ask us to accept cookies. We have to close 
        it. Otherwise is will distract our search"""
        time.sleep(5)
        button = self._driver.find_elements(By.XPATH,
                                            "//*[@id='uc-btn-accept-banner']")
        if button:
            button[0].click()

    def run_the_code(self, name: str):
        """The main method that reads the given files and
        saves the file with same name, except with .pkl ending
        :name: Filename (including path)
        """
        name = "HOUSE_CASTLE.txt"  #TODO Remove this line
        html_list = read_selenium_data.read_file(name)
        cookies_accepted = False
        for inner_list in html_list:
            url = inner_list[2]
            self._open_web_page(url)
            if not cookies_accepted:
                self._accept_cookies()
            address = self._read_address()
            price = self._read_price()
            if address == "" or price == "":
                continue
            inner_list.append(self._read_address())
            inner_list.append(self._read_price())
        name_base = name.split(".")
        new_name = "./data/" + name_base[0] + ".pkl"
        serialize_lists.write_dump(html_list, new_name)
        Read_Address.driver.quit()
        print(html_list)


#run_the_code()
#driver.quit()

#print(read_dump("HOUSE_CASTLE.pkl"))
"""sample_list = [1, 2, 3, 4, 5]
write_dump(sample_list, "./data/sample.pkl")
print("toimiiko tää?", read_dump("./data/sample.pkl"))
#driver.quit()"""

#
"""open_web_page(
    "https://www.immoweb.be/en/classified/house/for-sale/ombret-rawsa/4540/9728478"
)
read_address()
read_price()
driver.quit()"""

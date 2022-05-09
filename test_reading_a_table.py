"""
Testing the best way to read the table
"""
from bs4 import BeautifulSoup
import requests
import read_selenium_data

html_list = read_selenium_data.read_file("HOUSE_CASTLE.txt")

url = html_list[3][2]
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
my_classifield_table = soup.find_all("table", class_="classified-table")


def read_classifield_table(classifield_table):
    """
    Reads the table with the properties
    """
    for info in classifield_table.find_all("tbody"):
        rows = info.find_all("tr")
        print("-" * 100)
        for row in rows:
            if not row.find_all("th", class_="classified-table__header"):
                # print("=====> Header missing!")
                continue
            if not row.find_all("td", class_="classified-table__data"):
                # print("=====> Data missing!")
                continue
            detail_header = (
                row.find("th", class_="classified-table__header").contents[0].strip()
            )
            detail_data = (
                row.find("td", class_="classified-table__data").contents[0].strip()
            )
            if not detail_data or not detail_header:
                print(
                    # "=====> Detail data or header is missing <=====    header:",
                    detail_header,
                    ",  data:",
                    detail_data,
                )
            else:
                print(detail_header, "/", detail_data)


# FOR REST OF THE INFORMATION
for one_table in my_classifield_table:
    read_classifield_table(one_table)

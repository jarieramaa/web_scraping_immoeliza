"""
This module is for reading files that scraping_with_selenium -module creates.
It can be used directly or used as an example
"""
from math import ceil
import os
import re

import selenium_address


def read_file(filename: str) -> list:
    """
    'scraping_with_selenium' writes files with special format. This
    method can read the format and return the result as a list
    :return: a list of lists. the inside lists has three elements:
    - 1. is the item a House or Apartment
    - 2. Suptype, for example farmhouse, villa etc.
    - 3. html address where the actual ad is
    This method returns the list for only one file at a time (one
    type of subtype at a time)
    """
    destination_file = os.path.join("data", filename)
    result = []
    final_result = []
    with open(destination_file, "r") as my_file:
        result = my_file.readlines()
    result = result[0].split("<#END>")
    result.pop()
    for i in result:
        line = re.split("<#COL>|<COL>", i)
        final_result.append(line)
    return final_result


def all_files() -> list:
    """
    'scraping_with_selenium' writes files with special format. This
    method can read the format and return the result as a list
    :return: a list of lists. the inside lists has three elements:
    - 1. is the item a House or Apartment
    - 2. Suptype, for example farmhouse, villa etc.
    - 3. html address where the actual ad is
    This method returns all the properties
    """
    counter = 0
    all_documents = os.listdir("data/")
    result = []
    for i in all_documents:
        if i.endswith("txt"):
            my_list = read_file(i)
            counter += len(my_list)
            for row in my_list:
                result.append(row)
    return result


def get_test_list(number):
    list = []
    for i in range(1, number):
        list.append(i)
    return list


def split_files(size: int, filename: str) -> None:
    """splits a selenium file. The parts will be
    numbered. The destination folder is 'split'
    :size: An int that defines how many rows will be
    in one file
    :filename: A string that defines the file that
    will be splitted
    """
    list = read_file(filename)
    tmp_list = []
    remaining_list = list
    list_len = len(list)
    rounds = int(ceil(list_len / size))
    for i in range(0, rounds):
        tmp_list = remaining_list[0:size]
        remaining_list = remaining_list[size:]
        filename = filename.split(".")[0]
        print("filename is:", f"./data/split/{filename}_{i+1}.txt")
        print("tmp_list to save:", tmp_list)
        selenium_address.Read_Address.write_dump(tmp_list, filename)


# split_files(50, "HOUSE_TOWN_HOUSE.txt")

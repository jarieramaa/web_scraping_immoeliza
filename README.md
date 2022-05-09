<p align="center">
  <img src="https://user-images.githubusercontent.com/27958519/152174276-e7988d8f-98e6-43e3-ad7b-4d4696f0acc0.png" />
</p>
## Description
This tool is used to collect property data from ImmoWeb site. House and Apartment with subtypes are collected, Life annuity sales are excluded. 


## Installation
The needed frameworks are:


| Framework     | Version |
| ---------- | ------- |
| Selenium      | 4.1.0 |
| BeautifulSoup      | 4.10.0)  |
| Python     | 3.9.7  |
| numpy   | 1.22.3  |
| Requests     | 2.27.1  |
| Pandas | 1.4.2  |


Please, read requirements.txt for further details

## Usage

There actual data collection is done using following tools:

# 1. scraping\_with\_selenium.py

  - Uses Selenium to collect links to the property ads from ImmoWeb-site.
  - Automaticaly selects property type (house/apartment) and one out of 20 subtype (penthouse, 
  dublex, single etc). Futhermore the tool excludes the life annuity sales. The tool 
  can be started with command: 'python scraping_with_selenium.py'
  - Scraping tool will create text-files to ./data/ -directory, one file for each subtype and 
  the file is named accordingly (for ex. HOUSE_VILLAS.txt). 
  - Tool is also creating log file
  that contains information how many properties was found and if there were any errors. When 
  the programn has finished html_to_attributes.py can be started

# 2. html\_to\_attributes.py

  - This tool uses the links that were created by Selenium tool. It reads the files created by
  Selenium tool and by using BeautifulSoup downloads all the attributes for properties. 
  - Tool can be started in terminal with command: 'python html_to_attributes.py
  filename is one of those files that Selenium tool generated (for ex. python html_to_attributes.py HOUSE_VILLAS.txt). 
  - Please, note that it's possible to open several terminal and load different files with the tool from there. The result 
  will be written to a binary files. 

# 3. file\_read\_example

This tool reads all the binary files, and modifies the data to proper format for machine learning. It also creates CSV file.

## Visuals
<filename>'![Screenshot from 2022-02-02 15-55-55](https://user-images.githubusercontent.com/27958519/152178776-8fd6f9c6-3c8e-446d-86e6-c175eeb47f10.png)

## Contributors
Jari Erämaa, coding


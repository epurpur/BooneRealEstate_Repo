#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:03:57 2020

@author: ep9k
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

#get addresses into shape

addresses = pd.read_excel('/Users/ep9k/Desktop/300addresses.xlsx')
addresses = addresses['Property Address'].to_list()


nums = []

for i in addresses:
        
    num_pattern = re.compile(r'\d{1,4}')
    
    num_match = num_pattern.findall(i)
    
    for i in num_match:
        nums.append(i)
        

streets = []

for i in addresses:
    
    street_pattern = re.compile(r' \w{0,}[^0123456789] ?\w{4,}')
    
    street_match = street_pattern.findall(i)
    
    for i in street_match:
        i = i[1:]                 #remove first character (space)
        streets.append(i)
        

address_list = list(zip(nums, streets))  #i will use this to manipulate in selenium


#Go to selenium and control avery county website

driver = webdriver.Chrome(executable_path="/Users/ep9k/Desktop/BRE/BRE 2019/BRE_Condos_List/drivers/chromedriver")

driver.get('http://webtax.averycountync.gov/')

parcel_numbers = []

for address in address_list:
    number = address[0]
    street = address[1]
    
    try:
        #clear inputs
        house_number = driver.find_element_by_id('ctl00_contentplaceholderRealEstateSearch_usercontrolRealEstateSearch_textboxHouse')
        st_name = driver.find_element_by_id('ctl00_contentplaceholderRealEstateSearch_usercontrolRealEstateSearch_textboxStreetName')
        
        house_number.clear()
        st_name.clear()
        
        house_number.send_keys(number)
        st_name.send_keys(street)
        
        #click 'search' button
        driver.find_element_by_id('ctl00_contentplaceholderRealEstateSearch_usercontrolRealEstateSearch_buttonSearch').click()
        driver.find_element_by_class_name('HyperLinkField').click()
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        parcel_number = soup.find('span', {'id': 'ctl00_contentplaceholderRealEstateSearchSummary_usercontrolRealEstateParcelSummaryInfo_LabelParcelNumber'})
        owner_name1 = soup.find('span', {'id': 'ctl00_contentplaceholderRealEstateWorkplace_tabcontainerWorkSpace_tabpanelOwners_usercontrolRealEstateParcelOwnersData_labelAccountName1Value'})

        parcel_number = parcel_number.text
        parcel_number = parcel_number[:-5]
        
        if parcel_number == "":
            parcel_number = 'Error'
        
        parcel_numbers.append(parcel_number)
        
        time.sleep(1)
        
    except Exception:
        parcel_numbers.append('Error')

driver.quit()


#put all data into dataframe for final export to Matt
data = {'Street Number': nums, 'Street Name': streets, 'Parcel Number': parcel_numbers}
address_df = pd.DataFrame(data)

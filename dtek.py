#!/usr/bin/env python3

import sys, time, os

from re       import *
from bs4      import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by      import By
from selenium.webdriver.common.keys    import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome          import ChromeDriverManager


# Process Arguments
import argparse

argument_parser  = argparse.ArgumentParser()
argument_parser.add_argument("--street", type=str, help="street number") 
argument_parser.add_argument("--house",  type=str, help="house_number") 

argument_parser.add_argument("--noheadless",  "-nhdlss", help="Start browser in non-headless mode", action="store_true")

argument_parser_group = argument_parser.add_mutually_exclusive_group()
argument_parser_group.add_argument("--json-stdout", "-jout",   help="Dump json respond to stdout stream", action="store_true")
argument_parser_group.add_argument("--json-stderr", "-jerr",   help="Dump json respond to stderr stream", action="store_true")
argument_parser_group.add_argument("--json-file",   "-f",      type=str, help="Dump json respond to the file")

command_line_arguments = argument_parser.parse_args()

chrome_options = Options()

if command_line_arguments.noheadless is not True:
    chrome_options.add_argument("--headless")

chrome_service = Service(ChromeDriverManager().install()) 

chrome_driver = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options
)

chrome_driver.get('https://www.dtek-kem.com.ua/ua/shutdowns')

##street_address_text = "вул. Балаклієвська"
##house_number_text   = "12"

street_address_text = command_line_arguments.street
house_number_text   = command_line_arguments.house

# Find table input box.
street_input_box = chrome_driver.find_element(By.ID, "street")
street_input_box.send_keys(street_address_text)
street_input_box.send_keys(Keys.ENTER)
time.sleep(2)

# Find table house number
house_number_box = chrome_driver.find_element(By.ID, "house_num")
house_number_box.send_keys(house_number_text)
house_number_box.send_keys(Keys.ENTER)
time.sleep(2)

# Get the table
btfl_soup   = BeautifulSoup(chrome_driver.page_source, features="html.parser")
parsed_html = btfl_soup.findAll(True, {"class":["cell-non-scheduled", "cell-scheduled", "cell-scheduled-maybe"]})

time_intervals = {
        "00:00-01:00" : "Unknown",
        "01:00-02:00" : "Unknown",
        "02:00-03:00" : "Unknown",
        "03:00-04:00" : "Unknown",
        "04:00-05:00" : "Unknown",
        "05:00-06:00" : "Unknown",
        "06:00-07:00" : "Unknown",
        "07:00-08:00" : "Unknown",
        "08:00-09:00" : "Unknown",
        "09:00-10:00" : "Unknown",
        "10:00-11:00" : "Unknown",
        "11:00-12:00" : "Unknown",
        "12:00-13:00" : "Unknown",
        "13:00-14:00" : "Unknown",
        "14:00-15:00" : "Unknown",
        "15:00-16:00" : "Unknown",
        "16:00-17:00" : "Unknown",
        "17:00-18:00" : "Unknown",
        "18:00-19:00" : "Unknown",
        "19:00-20:00" : "Unknown",
        "20:00-21:00" : "Unknown",
        "21:00-22:00" : "Unknown",
        "22:00-23:00" : "Unknown",
        "23:00-24:00" : "Unknown"
}

time_scheduling = {
        "Monday"     : time_intervals.copy(),
        "Tuesday"    : time_intervals.copy(),
        "Wedndesday" : time_intervals.copy(),
        "Thursday"   : time_intervals.copy(),
        "Friday"     : time_intervals.copy(),
        "Saturday"   : time_intervals.copy(),
        "Sunday"     : time_intervals.copy()
}


# Parse class name into nice table.
TABLE_ROW_COUNT = 7
TABLE_COL_COUNT = 24

# Global HTML element position.
html_array_position = 0

# Get dict key from value.
def get_dict_key(dictionary, n) -> str:
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key

# Asign values to dictionaries according to the class name.

for col in range(TABLE_COL_COUNT):
    dict_col_key = get_dict_key(time_intervals, col)

    for row in range(TABLE_ROW_COUNT):
        dict_row_key = get_dict_key(time_scheduling, row)

        # Learn if current time is scheduled.
        current_class     = parsed_html[html_array_position].get("class")
        if current_class[0] == "cell-scheduled":
            time_is_scheduled = "Off"
        if current_class[0] == "cell-scheduled-maybe":
            time_is_scheduled = "Maybe"
        if current_class[0] == "cell-non-scheduled":
            time_is_scheduled = "On"

        time_scheduling[dict_row_key][dict_col_key] = time_is_scheduled

        html_array_position += 1


# Process command line arguments.
import json

if command_line_arguments.json_stdout:
    print(json.dumps(time_schedule,indent=4), file=stdout)
elif command_line_arguments.json_stderr:
    print(json.dumps(time_schedule,indent=4), file=stderr)
else: # If the --file [FILE] specified
    with open(command_line_arguments.json_file, "w") as json_file:
        json_file.write(json.dumps(time_scheduling, indent=4))

chrome_driver.close()

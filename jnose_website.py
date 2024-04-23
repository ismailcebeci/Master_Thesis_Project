from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import csv
import os
import subprocess

import time

file_path = 'D:\Master_Thesis\Github_Projects\projects.csv'

filename = open(file_path, 'r')

git_clone_url = []

git_project_full_name = []

git_project_modified_name = []

# Reading cvs file with DictReader object

try:
    with open(file_path, 'r') as csvfile:
        # Create a CSV DictReader object
        csv_reader = csv.DictReader(csvfile, delimiter=';')

        '''header = next(csv_reader)'''
        
        # Read and print each row in the CSV file
        for row in csv_reader:
            if "clone_url" in row:
                git_clone_url.append(row['clone_url'])
            if "Full_name" in row:
                git_project_full_name.append(row['Full_name'])
            if "Full_name_modified" in row:
                git_project_modified_name.append(row['Full_name_modified'])

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

for link in git_clone_url:
    # Set the path to the webdriver executable (e.g., chromedriver.exe for Chrome)
    webdriver_path = 'C:\Program Files\Mozilla Firefox\firefox.exe'

    # URL of the website you want to interact with
    url = 'http://127.0.0.1:8080'

    # Create a new instance of the Chrome WebDriver
    driver = webdriver.Firefox()

    # Open the website in the browser
    driver.get(url)

    button = driver.find_element(By.LINK_TEXT, 'Projects')
    button.click()
    # Adding git url link on website
    input_git_url_link = driver.find_element(By.XPATH, "//input[@id='gitrepo']")
    input_git_url_link.send_keys(link)
    button = driver.find_element(By.ID, 'id4')
    button.click()
    time.sleep(30)

    driver.quit()


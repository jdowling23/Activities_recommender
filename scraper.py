import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

#url for visit chattanooga that has activities
URL = 'https://www.visitchattanooga.com/things-to-do/free-things-to-do/'

#enable chrome options
options = Options()
options.add_argument('--headless=new')     
#options.add_argument("--window-size=1920,1200")  # Set the window size

driver = webdriver.Chrome(options=options)
driver.get(URL)
#get page source
html = driver.page_source
#close driver for webpage
driver.quit

#convert page source to html using BS4
soup = BeautifulSoup(html, 'html.parser')

#find the section containing all the things to do
free_main_content = soup.find(id='main-content')

#find all headers and paragraph decendents of main content
h_tags = free_main_content.find_all('h2')
p_tags = free_main_content.find_all('p')

#convert to dictionary
h_and_p = dict(zip(h_tags, p_tags))

print(h_and_p)

#convert dict to dataframe
dictdf = pd.DataFrame.from_dict(h_and_p)

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_html_file(url:str, sleep_time:int = 2):
    selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    selenium_driver.get(url)
    time.sleep(sleep_time)
    html_file = selenium_driver.page_source
    selenium_driver.quit()

    return html_file
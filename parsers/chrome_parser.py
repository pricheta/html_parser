from time import sleep

from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from parsers.parser_interface import Parser
from user_answers import user_answers


class Chrome:
    def __init__(self, timeout: int):
        self.timeout = timeout

    def __enter__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        return False

    def collect_html_files(
        self,
        url:str,
        master_page_parsed_classes: str,
        clicked_classes: str,
        slave_page_parsed_classes: str,
    ):
        self.driver.get(url)
        sleep(self.timeout)

        main_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)
        html_files = []
        for i in range(len(main_blocks)):
            main_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)

            html_file = main_blocks[i].get_attribute('outerHTML')
            clicked_block = main_blocks[i].find_element(By.CLASS_NAME, clicked_classes)
            self.driver.execute_script("arguments[0].click();", clicked_block)
            sleep(self.timeout)

            if slave_page_parsed_classes:
                sub_block = self.driver.find_element(By.CLASS_NAME, slave_page_parsed_classes)
                html_file += sub_block.get_attribute('outerHTML')
                self.driver.back()
                sleep(self.timeout)

            html_files.append(html_file)

        return html_files



class ChromeParser(Parser):
    def parse(self) -> list[ResultSet]:
        chrome = Chrome(timeout=2)
        result_sets = []
        with chrome:
            html_files=chrome.collect_html_files(
                url=user_answers.url,
                master_page_parsed_classes=user_answers.master_page_parsed_classes,
                clicked_classes=user_answers.clicked_classes,
                slave_page_parsed_classes=user_answers.slave_page_parsed_classes,
            )

        for html_file in html_files:
            bs = BeautifulSoup(html_file, features="html.parser")
            result_set = bs.find_all(class_=[user_answers.master_page_parsed_classes, user_answers.slave_page_parsed_classes])
            result_sets.append(result_set)

        return result_sets

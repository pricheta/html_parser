from time import sleep

from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from logger.logger import log_calling, logger
from parsers.parser_interface import Parser


class Chrome:
    def __init__(self, delay: int):
        self.delay = delay

    def __enter__(self):
        options = Options()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        return False

    @log_calling
    def collect_html_content(
        self,
        url:str,
        master_page_parsed_classes: str,
        clicked_classes: str | None,
        slave_page_parsed_classes: str | None,
    ) -> list[str]:
        self.driver.get(url)
        sleep(self.delay)

        html_files = []
        master_page_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)
        for i in range(len(master_page_blocks)):
            html_content = master_page_blocks[i].get_attribute('outerHTML')

            if clicked_classes:
                clicked_block = master_page_blocks[i].find_element(By.CLASS_NAME, clicked_classes)
                self.driver.execute_script("arguments[0].click();", clicked_block)
                sleep(self.delay)

                slave_block = self.driver.find_element(By.CLASS_NAME, slave_page_parsed_classes)
                html_content += slave_block.get_attribute('outerHTML')
                self.driver.back()
                sleep(self.delay)

            html_files.append(html_content)
            master_page_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)

        return html_files



class ChromeParser(Parser):
    @log_calling
    def parse(self) -> list[ResultSet]:
        chrome = Chrome(delay=2)
        parse_result = []
        with chrome:
            html_files=chrome.collect_html_content(
                url=self.user_answers.url,
                master_page_parsed_classes=self.user_answers.master_page_parsed_classes,
                clicked_classes=self.user_answers.clicked_classes,
                slave_page_parsed_classes=self.user_answers.slave_page_parsed_classes,
            )

        for html_file in html_files:
            bs = BeautifulSoup(html_file, features="html.parser")
            result_set = bs.find_all(class_=[self.user_answers.master_page_parsed_classes, self.user_answers.slave_page_parsed_classes])
            parse_result.append(result_set)

        self._log_parse_result(parse_result)
        return parse_result

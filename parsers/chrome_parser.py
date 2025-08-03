from time import time, sleep


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from logger.logger import log_calling
from parsers.parser_interface import Parser


class Chrome:
    def __init__(self, delay: int, scroll_required: bool):
        self.delay = delay
        self.scroll_required = scroll_required

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
        html_files = []

        self.driver.get(url)
        self._wait_till_page_loaded()

        element_number = 0
        while True:
            master_page_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)

            if element_number >= len(master_page_blocks):
                if self.scroll_required:
                    diff = self._scroll_to_bottom_with_wait()
                    if not diff:
                        break
                    continue
                break

            html_content = master_page_blocks[element_number].get_attribute('outerHTML')

            if clicked_classes:
                clicked_block = master_page_blocks[element_number].find_element(By.CLASS_NAME, clicked_classes)
                self.driver.execute_script("arguments[0].click();", clicked_block)
                self._wait_till_page_loaded()

                slave_block = self.driver.find_element(By.CLASS_NAME, slave_page_parsed_classes)
                html_content += slave_block.get_attribute('outerHTML')
                self.driver.back()
                self._wait_till_page_loaded()

            html_files.append(html_content)
            element_number += 1

        return html_files

    def _wait_till_page_loaded(self):
        WebDriverWait(self.driver, self.delay).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _scroll_to_bottom_with_wait(self):
        previous_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._wait_till_page_loaded()
        current_height = self.driver.execute_script("return document.body.scrollHeight")
        return current_height - previous_height



class ChromeParser(Parser):
    @log_calling
    def parse(self) -> list[list[str]]:
        chrome = Chrome(delay=2, scroll_required=self.user_answers.scroll_required)
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
            result_set = bs.get_text(strip=True, separator="\n").split(sep="\n")
            parse_result.append(result_set)

        self._log_parse_result(parse_result)
        return parse_result

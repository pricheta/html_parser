from time import time, sleep


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from logger.logger import log_calling, logger
from parsers.parser_interface import Parser
from questioner.user_answers import UserAnswers, MasterSlaveMode


class Chrome:
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers
        self.driver: webdriver.Chrome | None = None

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
    def collect_html_content(self,) -> list[str]:
        html_files = []

        element_number = int(self.user_answers.start_element_number)

        self.driver.get(self.user_answers.url)
        self._wait_till_page_loaded()

        while True:
            try:
                master_page_blocks = self.driver.find_elements(By.CSS_SELECTOR, self.user_answers.master_page_parsed_selector)
                if not master_page_blocks:
                    logger.error('Не удалось найти элементы для парсинга на основной странице')
                    break

                if element_number >= len(master_page_blocks):
                    if self.user_answers.scroll_required:
                        diff = self._scroll_to_bottom_with_wait()
                        if not diff:
                            break
                        continue
                    break

                current_master_page_block = master_page_blocks[element_number]
                html_content = current_master_page_block.get_attribute('outerHTML')

                if self.user_answers.master_slave_mode != MasterSlaveMode.MASTER_SLAVE_MODE_OFF:
                    if self.user_answers.master_slave_mode == MasterSlaveMode.CLICK_MASTER_TAG:
                        clicked_block = current_master_page_block
                    elif self.user_answers.master_slave_mode == MasterSlaveMode.CLICK_INNER_TAG:
                        clicked_block = current_master_page_block.find_element(By.CSS_SELECTOR, self.user_answers.clicked_selector)
                    else:
                        raise ValueError(f'{self.user_answers.master_slave_mode} mode not supported')

                    self.driver.execute_script("arguments[0].click();", clicked_block)
                    self._wait_till_page_loaded()

                    slave_block = self.driver.find_element(By.CSS_SELECTOR, self.user_answers.slave_page_parsed_selector)
                    html_content += slave_block.get_attribute('outerHTML')
                    self.driver.back()
                    self._wait_till_page_loaded()

                html_files.append(html_content)

            except Exception as e:
                logger.warning(f"{e.__class__.__name__} occurred at {element_number=}, process continued")

            element_number += 1

        logger.info(f'Finished collecting html content')
        return html_files

    def _wait_till_page_loaded(self):
        sleep(float(self.user_answers.delay))

    def _scroll_to_bottom_with_wait(self):
        previous_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._wait_till_page_loaded()
        current_height = self.driver.execute_script("return document.body.scrollHeight")
        return current_height - previous_height



class ChromeParser(Parser):
    @log_calling
    def parse(self) -> list[list[str]]:
        chrome = Chrome(self.user_answers)
        parse_result = []
        with chrome:
            html_files=chrome.collect_html_content()

        for html_file in html_files:
            bs = BeautifulSoup(html_file, features="html.parser")
            result_set = bs.get_text(strip=True, separator="\n").split(sep="\n")
            parse_result.append(result_set)

        self._log_parse_result(parse_result)
        return parse_result

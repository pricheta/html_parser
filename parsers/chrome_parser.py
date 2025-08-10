from time import sleep, time

from bs4 import BeautifulSoup
from func_timeout import func_timeout, FunctionTimedOut
from selenium import webdriver
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from logger.logger import log_calling, logger
from parsers.parser_interface import Parser
from questioner.user_answers import UserAnswers, MasterSlaveMode


class Chrome:
    @log_calling
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers
        self.driver: webdriver.Chrome | None = None

    @log_calling
    def __enter__(self):
        options = Options()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return self.driver

    @log_calling
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
                    logger.error('Не удалось найти элементы для парсинга на основной странице, экстренное завершение')
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
                        raise ValueError(f'Режим работы {self.user_answers.master_slave_mode} не поддерживается')

                    current_page_url = self.driver.current_url
                    self.driver.execute_script("arguments[0].click();", clicked_block)
                    self._wait_till_page_loaded()

                    slave_block = self.driver.find_element(By.CSS_SELECTOR, self.user_answers.slave_page_parsed_selector)
                    html_content += slave_block.get_attribute('outerHTML')

                    current_page_url = self.driver.current_url
                    self.driver.get(self.user_answers.url)
                    self._wait_till_page_loaded()

                html_files.append(html_content)

            except Exception as e:
                logger.warning(
                    f"Ошибка {e.__class__.__name__} возникла при работе с элементом №{element_number} на ссылке {self.driver.current_url}, "
                    "элемент пропущен"
                )

            element_number += 1

        logger.info(f'Закончена выгрузка HTML-данных')
        return html_files

    @log_calling
    def _wait_till_page_loaded(self):
        check_interval = 0.1
        current_count = None
        stable_count = 0

        start_time = time()
        sleep(1)

        while time() - start_time < 5:
            last_count = current_count
            current_count = len(
                self.driver.find_elements(By.CSS_SELECTOR, "body, div, p, a, span, img")
            )
            if not current_count:
                sleep(check_interval)
                continue

            if current_count == last_count:
                stable_count += 1
            else:
                stable_count = 0

            logger.debug(f'Проверка условий, {current_count=}, {last_count=}, {stable_count=}')
            if stable_count >= 4:
                break
            sleep(check_interval)

        logger.debug(f'Ожидание загрузки страницы окончено спустя {time() - start_time} секунд')

    @log_calling
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

        return parse_result

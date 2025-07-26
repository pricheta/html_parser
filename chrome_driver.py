from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


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
        main_block_class_value: str,
        clicked_block_class_value: str,
        sub_block_class_value: str,

    ):
        self.driver.get(url)
        sleep(self.timeout)

        main_blocks = self.driver.find_elements(By.CLASS_NAME, main_block_class_value)
        html_files = []
        for i in range(len(main_blocks)):
            main_blocks = self.driver.find_elements(By.CLASS_NAME, main_block_class_value)

            html_file = main_blocks[i].get_attribute('outerHTML')
            clicked_block = main_blocks[i].find_element(By.CLASS_NAME, clicked_block_class_value)
            self.driver.execute_script("arguments[0].click();", clicked_block)
            sleep(self.timeout)

            if sub_block_class_value:
                sub_block = self.driver.find_element(By.CLASS_NAME, sub_block_class_value)
                html_file += sub_block.get_attribute('outerHTML')
                self.driver.back()
                sleep(self.timeout)

            html_files.append(html_file)

        return html_files
from time import sleep

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
        main_window = self.driver.current_window_handle

        self.driver.get(url)
        self._wait_till_page_loaded()

        if self.scroll_required:
            self._scroll_to_bottom_with_wait()

        master_page_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)

        for i in range(len(master_page_blocks)):
            master_page_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)
            html_content = master_page_blocks[i].get_attribute('outerHTML')

            if clicked_classes:
                new_window = self._duplicate_tab_full()
                self.driver.switch_to.window(new_window)

                master_page_blocks = self.driver.find_elements(By.CLASS_NAME, master_page_parsed_classes)
                clicked_block = master_page_blocks[i].find_element(By.CLASS_NAME, clicked_classes)
                self.driver.execute_script("arguments[0].click();", clicked_block)
                self._wait_till_page_loaded()

                slave_block = self.driver.find_element(By.CLASS_NAME, slave_page_parsed_classes)
                html_content += slave_block.get_attribute('outerHTML')

                self.driver.close()
                self.driver.switch_to.window(main_window)

            html_files.append(html_content)

        return html_files

    def _wait_till_page_loaded(self):
        WebDriverWait(self.driver, self.delay).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )


    def _scroll_to_bottom_with_wait(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, self.delay).until(
                    lambda d: d.execute_script("return document.body.scrollHeight") > last_height
                )
                last_height = self.driver.execute_script("return document.body.scrollHeight")
            except:
                break

    def _duplicate_tab_full(self):
        state = {
            'url': self.driver.current_url,
            'scroll': self.driver.execute_script("return [window.pageXOffset, window.pageYOffset];"),
            'html': self.driver.execute_script("return document.documentElement.outerHTML;"),
            'cookies': self.driver.get_cookies(),
            'local_storage': self.driver.execute_script("return JSON.stringify(localStorage);"),
            'session_storage': self.driver.execute_script("return JSON.stringify(sessionStorage);")
        }

        self.driver.switch_to.new_window('tab')

        self.driver.execute_script(f"""
            document.open();
            document.write(`{state['html']}`);
            document.close();
            window.scrollTo({state['scroll'][0]}, {state['scroll'][1]});
            history.replaceState(null, null, `{state['url']}`);

            const localStorageData = {state['local_storage']};
            const sessionStorageData = {state['session_storage']};

            for (const key in localStorageData) {{
                localStorage.setItem(key, localStorageData[key]);
            }}

            for (const key in sessionStorageData) {{
                sessionStorage.setItem(key, sessionStorageData[key]);
            }}
        """)

        for cookie in state['cookies']:
            self.driver.add_cookie(cookie)

        return self.driver.current_window_handle



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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def get_html_file(url:str, timeout:int = 10):
    selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    selenium_driver.get(url)

    try:
        WebDriverWait(selenium_driver, timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
    except Exception as e:
        print(f"Произошла ошибка при загрузки страницы: {e}")

    html_file = selenium_driver.page_source
    selenium_driver.quit()

    return html_file
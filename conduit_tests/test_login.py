from main_functions import login
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from data_for_testing import user


class TestLogin(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        """options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')"""
        self.browser = webdriver.Chrome(service=service, options=options)
        url = 'http://localhost:1667/#/'
        self.browser.get(url)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    def test_login_valid_data(self):
        login(self.browser, user["name"], user["email"], user["password"])
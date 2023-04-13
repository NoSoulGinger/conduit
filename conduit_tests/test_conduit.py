import time
import allure
import csv
from data_for_testing import *
from main_functions import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=options)
        url = 'http://localhost:1667/#/'
        self.browser.get(url)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    @allure.id("TC-01")
    @allure.title("Cookie elfogadásának tesztelése")
    def test_accept_cookies(self):
        accept_cookies(self.browser)
        cookie_status = self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")
        assert cookie_status["value"] == "accept"

    @allure.id("TC-02")
    @allure.title("Regisztráció funkció tesztelése helyes adatokkal")
    def test_registration_valid_data(self):
        registration(self.browser, user["name"], user["email"], user["password"])

    @allure.id("TC-03")
    @allure.title("Bejelentlezás funkció tesztelése helyes adatokkal")
    def test_login_valid_data(self):
        login(self.browser, user["name"], user["email"], user["password"])

    @allure.id("TC-04")
    @allure.title("Kijelentkezés funkció tesztelése")
    def test_logout(self):
        login(self.browser, user["name"], user["email"], user["password"])
        logout(self.browser)

    @allure.id("TC-05")
    @allure.title("Több oldalas lista bejárásának tesztelése")
    def test_all_pages(self):
        login(self.browser, user["name"], user["email"], user["password"])
        all_pages(self.browser)

    @allure.id("TC-06")
    @allure.title("Új feed létrehozása funkció tesztelése")
    def test_new_post(self):
        login(self.browser, user["name"], user["email"], user["password"])
        create_new_post(self.browser, post["title"], post["topic"], post["article"], post["tags"])

    @allure.id("TC-07")
    @allure.title("Feed törlése funkció tesztelése")
    def test_delete_existing_post(self):
        login(self.browser, user["name"], user["email"], user["password"])
        profile_page(self.browser, user["name"])
        delete_post(self.browser, post["title"])

    @allure.id("TC-08")
    @allure.title("Feed modosítása funckió tesztelése")
    def test_modify_post(self):
        login(self.browser, user["name"], user["email"], user["password"])
        create_new_post(self.browser, post["title"], post["topic"], post["article"], post["tags"])
        profile_page(self.browser, user["name"])
        modify_post(self.browser, post["title"], post["modified_title"], post["modified_topic"],
                    post["modified_article"])

    @allure.id("TC-09")
    @allure.title("Profilnév megváltoztatása funkció tesztelése")
    def test_modify_username(self):
        login(self.browser, user["name"], user["email"], user["password"])
        profile_page(self.browser, user["name"])
        modify_name(self.browser, user["new_name"])
        profile_page(self.browser, user["new_name"])
        modify_name(self.browser, user["name"])

    @allure.id("TC-10")
    @allure.title("Több feed létrehozásának tesztelése külső fájlból")
    def test_import_posts_from_file(self):
        login(self.browser, user["name"], user["email"], user["password"])
        with open('conduit_tests/post_data.txt', 'r', newline='') as file:
            csv_file = csv.reader(file, delimiter=',')
            for row in csv_file:
                create_new_post(self.browser, row[0], row[1], row[2], [row[3], row[4], row[5]])
                time.sleep(1)

    @allure.id("TC-11")
    @allure.title("Feedek címeinek listázása")
    def test_listing_titles(self):
        login(self.browser, user["name"], user["email"], user["password"])
        list_data(self.browser, "h1")
        print(list_res)

    @allure.id("TC-12")
    @allure.title("Feedek címeinek listázása és mentése külső fájlba")
    def test_save_data(self):
        saved_data = []
        login(self.browser, user["name"], user["email"], user["password"])
        list_data(self.browser, "h1") # ha minden igaz ez nem szükséges ide
        with open('conduit_tests/export_data.txt', 'w', newline='') as file:
            for title in list_res:
                file.write("%s\n" % title)
        with open('conduit_tests/export_data.txt', 'r', newline='') as f:
            for t in f:
                saved_data.append(t.replace("\n", ""))
        assert len(saved_data) == len(list_res)

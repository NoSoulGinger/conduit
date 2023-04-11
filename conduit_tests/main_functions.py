from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

list_res = []


def accept_cookies(browser):
    wait = WebDriverWait(browser, 5)
    cookie_accept = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--accept']")))
    cookie_accept.click()


def decline_cookies(browser):
    wait = WebDriverWait(browser, 5)
    cookie_decline = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--decline']")))
    cookie_decline.click()


def login(browser, name, email, password):
    wait = WebDriverWait(browser, 5)
    sign_in_nav = browser.find_element(By.XPATH, "//a[@href='#/login']")
    sign_in_nav.click()
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))
    email_input.send_keys(email)
    password_input.send_keys(password)
    sign_in_but = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-lg btn-primary pull-xs-right']")))
    sign_in_but.click()
    profile = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[@href='#/@{name}/']")))
    assert profile.text == name


def logout(browser):
    wait = WebDriverWait(browser, 5)
    sign_out_but = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@active-class='active']")))
    sign_out_but.click()
    sign_in_nav = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#/login']")))
    assert sign_in_nav.is_displayed()


def registration(browser, username, email, password):
    wait = WebDriverWait(browser, 5)
    register_but = browser.find_element(By.XPATH, "//a[@href='#/register']")
    register_but.click()
    username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")))
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))
    signup_but = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-lg btn-primary pull-xs-right']")))
    username_input.send_keys(username)
    email_input.send_keys(email)
    password_input.send_keys(password)
    signup_but.click()
    welcome_but = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='swal-button swal-button--confirm']")))
    welcome_but.click()
    profile = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[@href='#/@{username}/']")))
    assert profile.text == username


def create_new_post(browser, title, topic, article, tags):
    wait = WebDriverWait(browser, 5)
    new_article_nav = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#/editor']")))
    new_article_nav.click()
    text_area = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//input[@type='text']")))
    title_input = text_area[0]
    topic_input = text_area[1]
    tag_input = text_area[2]
    article_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//textarea[@placeholder='Write your article (in markdown)']")))
    title_input.send_keys(title)
    topic_input.send_keys(topic)
    article_input.send_keys(article)
    for i in range(len(tags)):
        tag_input.send_keys(tags[i])
        tag_input.send_keys(Keys.ENTER)
    publish = browser.find_element(By.XPATH, "//button[@type='submit']")
    publish.click()
    title_res = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='container']/h1"))).text
    article_res = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='col-xs-12']/div/p"))).text
    tag = browser.find_elements(By.XPATH, "//div[@class='tag-list']/a")
    tags_res = []
    for tag in tag:
        text = tag.text
        tags_res.append(text)
    assert title_res == title
    assert article_res == article
    for i in range(len(tags)):
        assert tags[i] == tags_res[i]


def modify_post(browser, title, new_title, new_topic, new_article):
    wait = WebDriverWait(browser, 5)
    article_to_modify = wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//a[@href='#/articles/{title.lower()}']")))
    article_to_modify.click()
    modify_but = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//a[@href='#/editor/{title.lower()}']")))
    modify_but.click()
    text_area = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//input[@type='text']")))
    article_inp = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@class='form-control']")))
    title_inp = text_area[0]
    topic_inp = text_area[1]
    title_inp.clear()
    title_inp.send_keys(new_title)
    topic_inp.clear()
    topic_inp.send_keys(new_topic)
    article_inp.clear()
    article_inp.send_keys(new_article)
    publish_but = browser.find_element(By.XPATH, "//button[@type='submit']")
    publish_but.click()
    title_res = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='container']/h1"))).text
    article_res = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='col-xs-12']/div/p"))).text
    main_page = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#/']")))
    main_page.click()
    topic_res = wait.until(EC.visibility_of_element_located(
        (By.XPATH, f"//a[@href='#/articles/{title.lower()}']/p"))).text
    assert title_res == new_title
    assert topic_res == new_topic
    assert article_res == new_article


def delete_post(browser, title):
    wait = WebDriverWait(browser, 5)
    article_to_del = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[@href='#/articles/{title.lower()}']")))
    article_to_del.click()
    article_url = browser.current_url
    delete_but = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-outline-danger btn-sm']")))
    delete_but.click()
    time.sleep(2)
    assert browser.current_url != article_url


def profile_page(browser, name):
    wait = WebDriverWait(browser, 5)
    profile_nav = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[@href='#/@{name}/']")))
    profile_nav.click()


def list_data(browser, attribute):
    wait = WebDriverWait(browser, 5)
    listed_items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, f'//div[@class="article-preview"]/a[@class="preview-link"]/{attribute}')))
    global list_res
    for listed_items in listed_items:
        list_res.append(listed_items.text)
    assert len(list_res) > 0


def next_page(browser):
    wait = WebDriverWait(browser, 5)
    active_page = wait.until(
        EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]/li[@class="page-item active"]'))).text
    pages = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//a[@class="page-link"]')))
    for page in pages:
        if int(page.text) - 1 == int(active_page):
            page.click()


def all_pages(browser):
    wait = WebDriverWait(browser, 5)
    pages = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//a[@class="page-link"]')))
    for page in pages:
        page.click()
        active_page = wait.until(
            EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]/li[@class="page-item active"]')))
        assert active_page.text == page.text

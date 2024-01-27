from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_browser_with_blocked_notifications():
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


class RedditBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = create_browser_with_blocked_notifications()

    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div/section/div/section[2]/section[1]/form/button'))
            ).click()
        except Exception as e:
            print(f"Cookie acceptance failed: {e}")

    def login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://www.reddit.com/login")
        time.sleep(2)

        username_elem = driver.find_element(
            'xpath', '//*[@id="loginUsername"]')
        password_elem = driver.find_element(
            'xpath', '//*[@id="loginPassword"]')

        username_elem.clear()
        password_elem.clear()

        username_elem.send_keys(self.username)
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    def search(self, search_query):
        search_bar = self.driver.find_element(
            "xpath", '//*[@id="header-search-bar"]')
        search_bar.clear()
        search_bar.send_keys(search_query)
        sleep(3)
        search_button = self.driver.find_element(
            'xpath', '//*[@id="SearchDropdownContent"]/button')
        search_button.click()

    def close_browser(self):
        self.driver.close()


# Use the bot
username = "mosefdata"
password = "DataMosef2@"
reddit_bot = RedditBot(username, password)
reddit_bot.login()
sleep(2)
reddit_bot.accept_cookies()
sleep(2)
reddit_bot.search("BP_PLC")
sleep(50)
# Close the browser when done
reddit_bot.close_browser()

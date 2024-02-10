import random
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parameters import mail, username, password

class TwitterScrapper:
    """
    X/Twitter Scrapper for 2024
    """

    def __init__(
        self,
        research: str = "Elon musk",
        link: str = "https://twitter.com/i/flow/login",
        output_path: str = "./../data/",
        start_date=None,
        end_date=None,
        mail=None,
        username=None,
        password=None,
        verbose: bool = False,
    ) -> None:
        self.research = research
        self.link = link

        self.verbose = verbose

    def _open_set_up_chrome(self):
        """
        Opens and sets up chrome in incognito mode (
        private navigation), maximazing the windows for avoiding changes
        in xpath which are relative to the size of the windows
        due to proportionality CSS methods.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        driver = Chrome(options=options)

        sleep(random.randint(1, 3))

        if self.verbose:
            print("Chrome opened")

        return driver

    def _open_twitter(self, driver, link):
        driver.get(link)
        sleep(random.randint(3, 5))

        if self.verbose:
            print("Linked opened")

        return driver
    
    def _init_twitter_session(self, driver):
        # Introduce mail
        try:
            connection_button = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input',
            )
            connection_button.click()
            connection_button.send_keys(mail + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Mail textbox not finded")
        driver.implicitly_wait(60)

        # Introduce username
        try:
            username_textbox = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
            )
            username_textbox.send_keys(username + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Username textbox not finded")
        
        driver.implicitly_wait(60)
        
        # Introduce password
        try:
            password_textbox = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
            )
            password_textbox.send_keys(password + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Username textbox not finded")
        
        driver.implicitly_wait(60)

        return driver

    def _twitter_query(self, driver, query):
        try:
            query_textbox = driver.find_element(
                "xpath",
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'
            )
            query_textbox.send_keys(query + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Query textbox not finded")
        
        sleep(random.randint(30, 500))


    def launch_webscrapping(self):
        driver = self._open_set_up_chrome()
        driver = self._open_twitter(driver=driver, link=self.link)
        driver = self._init_twitter_session(driver=driver)
        self._twitter_query(driver, query=self.research)

        

if __name__ == "__main__":
    ts = TwitterScrapper(research="bp plc",verbose=True)
    ts.launch_webscrapping()

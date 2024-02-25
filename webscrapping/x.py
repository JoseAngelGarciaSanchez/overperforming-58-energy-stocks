import csv
import os
import random
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

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
                print("Mail textbox not found")
        sleep(random.randint(2, 4))

        # Introduce username
        try:
            username_textbox = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input',
            )
            username_textbox.send_keys(username + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Username textbox not finded")
        sleep(random.randint(2, 4))

        # Introduce password
        try:
            password_textbox = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
            )
            password_textbox.send_keys(password + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Username textbox not found")

    def _twitter_query(self, driver, query):
        try:
            query_textbox = driver.find_element(
                "xpath",
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input',
            )
            query_textbox.send_keys(query + Keys.ENTER)
        except NoSuchElementException:
            if self.verbose:
                print("Query textbox not found")

    def _get_recents(self, driver):
        """get recents tweets from the 'lasts' page for recent activity"""
        try:
            recent = driver.find_element(
                "xpath",
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div',
            )
            recent.click()
            if self.verbose:
                print("good for getting recents tweets")
        except NoSuchElementException:
            if self.verbose:
                print("Recents box not found")

    def __get_tweet_data(self, card):
        """Extract data from tweet card"""
        try:
            handle = card.find_element("xpath", './/span[contains(text(), "@")]').text
        except NoSuchElementException:
            return
        try:
            username = card.find_element("xpath", ".//span").text
        except NoSuchElementException:
            return
        try:
            postdate = card.find_element("xpath", ".//time").get_attribute("datetime")
        except NoSuchElementException:
            return
        try:
            comment = card.find_element("xpath", ".//div[2]/div[2]/div[1]").text
        except NoSuchElementException:
            return
        try:
            responding = card.find_element("xpath", ".//div[2]/div[2]/div[2]").text
        except NoSuchElementException:
            return
        try:
            text = comment + responding
        except NoSuchElementException:
            return
        try:
            reply_cnt = card.find_element("xpath", './/div[@data-testid="reply"]').text
        except NoSuchElementException:
            return
        try:
            retweet_cnt = card.find_element(
                "xpath", './/div[@data-testid="retweet"]'
            ).text
            # retweet_cnt = card.find_element('xpath','.//div[@data-testid="retweet"]').text
        except NoSuchElementException:
            return
        try:
            like_cnt = card.find_element("xpath", './/div[@data-testid="like"]').text
            # like_cnt = card.find_element('xpath','.//div[@data-testid="like"]').text
        except NoSuchElementException:
            return
        tweet = (username, handle, postdate, text, reply_cnt, retweet_cnt, like_cnt)

        return tweet

    def __generate_tweet_id(self, tweet):
        if self.verbose:
            print("good for generating tweets id")
        return "".join(tweet)

    def __collect_all_tweets_from_current_view(self, driver, lookback_limit=25):
        page_cards = driver.find_elements("xpath", '//article[@data-testid="tweet"]')
        if self.verbose:
            print("Good for collecting all tweets")

        if len(page_cards) <= lookback_limit:
            return page_cards
        else:
            return page_cards[-lookback_limit:]

    def __scroll_down_page(
        self, driver, last_position, scroll_attempt=0, max_attempts=3
    ):
        """The function will try to scroll down the page and will check the current
        and last positions as an indicator. If the current and last positions are the same after `max_attempts`
        the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
        flag will be returned as `True`"""
        end_of_scroll_region = False

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(random.randint(3, 6))

        curr_position = driver.execute_script("return window.pageYOffset;")

        if curr_position == last_position:
            if scroll_attempt < max_attempts:
                end_of_scroll_region = True
            else:
                self.__scroll_down_page(
                    last_position, curr_position, scroll_attempt + 1
                )

        last_position = curr_position

        if self.verbose:
            print("good for scrolling down the page")

        return last_position, end_of_scroll_region

    def __save_tweet_data_to_csv(self, records, save_path, mode="a+"):
        """Saving the data collected into the specified output path with csv format"""
        header = [
            "User",
            "Handle",
            "PostDate",
            "TweetText",
            "ReplyCount",
            "RetweetCount",
            "LikeCount",
        ]
        if not os.path.exists(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            open(save_path, "w").close()
            mode = "w"
        with open(save_path, mode=mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if mode == "w":
                writer.writerow(header)
            if records:
                writer.writerow(records)

    def _scroll_and_save(self, driver, save_path):
        save_path_completed = (
            f'{save_path}webscraped_{"_".join(self.research.split())}.csv'
        )

        last_position = None
        end_of_scroll_region = False
        unique_tweets = set()

        self.__save_tweet_data_to_csv(None, save_path, "w")

        while not end_of_scroll_region:
            cards = self.__collect_all_tweets_from_current_view(driver)

            for card in cards:
                try:
                    tweet = self.__get_tweet_data(card)
                except StaleElementReferenceException:
                    continue
                if not tweet:
                    continue

                tweet_id = self.__generate_tweet_id(tweet)

                if tweet_id not in unique_tweets:
                    unique_tweets.add(tweet_id)

                    self.__save_tweet_data_to_csv(tweet, save_path)

            sleep(random.randint(3, 6))

            last_position, end_of_scroll_region = self.__scroll_down_page(
                driver, last_position
            )

        driver.quit()

    def launch_webscrapping(self, save_path: str | os.PathLike):
        if not save_path.endswith('/'):
            save_path += '/'

        driver = self._open_set_up_chrome()
        driver = self._open_twitter(driver=driver, link=self.link)

        self._init_twitter_session(driver=driver)
        sleep(random.randint(20, 40))

        self._twitter_query(driver, query=self.research)
        sleep(random.randint(5, 8))

        self._get_recents(driver)
        sleep(random.randint(6, 10))

        self._scroll_and_save(driver, save_path)

        sleep(random.randint(30, 500))


if __name__ == "__main__":
    ts = TwitterScrapper(research="bp plc", verbose=True)
    ts.launch_webscrapping(save_path="./../data/new_webscrapping/")

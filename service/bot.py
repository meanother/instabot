import logging
import os
import random
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from settings import login, password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(funcName)s %(process)d:%(processName)s %(message)s',
)
log = logging.getLogger(__name__)


class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def close_browser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_name('password').send_keys(Keys.RETURN)
        time.sleep(2)

    @staticmethod
    def hello():
        log.info('Starting Bot')
        log.info('''
            ____           __        ____        __     ____   ___        
           /  _/___  _____/ /_____ _/ __ )____  / /_   / __ \ <  /  _   __
           / // __ \/ ___/ __/ __ `/ __  / __ \/ __/  / / / / / /  | | / /
         _/ // / / (__  ) /_/ /_/ / /_/ / /_/ / /_   / /_/ / / /   | |/ / 
        /___/_/ /_/____/\__/\__,_/_____/\____/\__/   \____(_)_/    |___/  
        ''')

    @staticmethod
    def read_config():
        with open(os.path.join(BASE_DIR, 'hashtags.txt'), 'r') as file:
            data = file.read().strip()
        log.info(f'Bot settings:\n{data}\n-------------------------')
        return data

    def like_photo(self, hashtag):
        driver = self.driver
        time.sleep(5)
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        final_href_array = []
        for i in range(1, 4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            href_objects = driver.find_elements_by_tag_name('a')
            photo_href = [elem.get_attribute('href') for elem in href_objects if
                          '.com/p/' in elem.get_attribute('href')]
            [final_href_array.append(href) for href in photo_href if href not in final_href_array]

        for pic_href in final_href_array:
            log.info(f'Current parsed url is: {pic_href}')
            driver.get(pic_href)
            time.sleep(random.randint(2, 4))
            try:
                driver.find_element_by_css_selector('svg[aria-label="Like"]').click()
                time.sleep(random.randint(40, 50))
            except (NoSuchElementException, ElementNotInteractableException) as e:
                log.error(f'Cant find "Like" on page, sleep 10 seconds\n{str(e) + traceback.format_exc()}')
                time.sleep(random.randint(6, 15))
                pass


def main():
    Bot.hello()
    config = Bot.read_config()
    while True:
        try:
            run = Bot(login, password)
            run.login()
            for tag in config.split('\n'):
                log.info(f'Current hashtag is #{tag}')
                run.like_photo(tag)
                time.sleep(60)
        except Exception as e:
            log.error(str(e) + traceback.format_exc())
            time.sleep(120)
            log.info('Sleep 2 min after ERROR')


if __name__ == "__main__":
    main()

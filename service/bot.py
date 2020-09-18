import argparse
import logging
import os
import random
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
# from settings import login, password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(funcName)s %(message)s',
)
log = logging.getLogger(__name__)


class Bot:
    def __init__(self, username, password, driver_path):
        self.username = username
        self.password = password
        self.count = 0
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

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
           /  _/___  _____/ /_____ _/ __ )____  / /_   / __ \ |__ \    _   __
           / // __ \/ ___/ __/ __ `/ __  / __ \/ __/  / / / / __/ /   | | / /
         _/ // / / (__  ) /_/ /_/ / /_/ / /_/ / /_   / /_/ / / __/    | |/ / 
        /___/_/ /_/____/\__/\__,_/_____/\____/\__/   \____(_)____/    |___/  
        ''')

    @staticmethod
    def read_config():
        with open(os.path.join(BASE_DIR, 'hashtags.txt'), 'r') as file:
            data = file.read().strip()
        log.info(f'Bot settings:\n{data}\n-------------------------')
        return data

    @staticmethod
    def read_config_from_args(path):
        with open(path, 'r') as file:
            data = file.read().strip()
        log.info(f'Bot settings:\n{data}\n-------------------------')
        return data

    def like_photo(self, hashtag, like):
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
                driver.find_element_by_css_selector(f'svg[aria-label="{like}"]').click()
                time.sleep(random.randint(55, 75))
                self.count += 1
            except (NoSuchElementException, ElementNotInteractableException) as e:
                log.error(f'Cant find "Like" on page, sleep 10 seconds\n{str(e) + traceback.format_exc()}')
                time.sleep(random.randint(6, 20))
                pass
            log.info(f'Кол-во лайков за запуск = {self.count}')


def main():
    parser = argparse.ArgumentParser(description='InstaBot commands help')
    parser.add_argument('-l', '--login', action="store", dest="login", type=str)
    parser.add_argument('-p', '--password', action="store", dest="password", type=str)
    parser.add_argument('-t', '--path', action="store", default='$HOME', type=str)
    parser.add_argument('-c', '--chromedriver', action="store", type=str)
    parser.add_argument('-g', '--like', action="store", default='Like', type=str)

    args = parser.parse_args()

    Bot.hello()
    # config = Bot.read_config()
    config = Bot.read_config_from_args(args.path)

    while True:
        try:
            run = Bot(args.login, args.password, args.chromedriver)
            run.login()
            for tag in config.split('\n'):
                log.info(f'Current hashtag is #{tag}')
                run.like_photo(tag, args.like)
                time.sleep(60)
        except Exception as e:
            log.error(str(e) + traceback.format_exc())
            time.sleep(120)
            log.info('Sleep 2 min after ERROR')


if __name__ == "__main__":
    main()

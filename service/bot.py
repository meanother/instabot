import os
import random
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from .utils import log, BASE_DIR


class Bot:
    def __init__(self, username, password, driver_path):
        self.username = username
        self.password = password
        self.count = 0
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def close_browser(self) -> None:
        self.driver.close()

    def login(self) -> None:
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_name('password').send_keys(Keys.RETURN)
        time.sleep(2)

    @staticmethod
    def hello() -> None:
        log.info('Starting Bot')
        log.info('''
            ____           __        ____        __     ____   ___           
           /  _/___  _____/ /_____ _/ __ )____  / /_   / __ \ |__ \    _   __
           / // __ \/ ___/ __/ __ `/ __  / __ \/ __/  / / / / __/ /   | | / /
         _/ // / / (__  ) /_/ /_/ / /_/ / /_/ / /_   / /_/ / / __/    | |/ / 
        /___/_/ /_/____/\__/\__,_/_____/\____/\__/   \____(_)____/    |___/  
        ''')

    @staticmethod
    def read_config() -> str:
        with open(os.path.join(BASE_DIR, 'hashtags.txt'), 'r') as file:
            data = file.read().strip()
        log.info(f'Bot settings:\n{data}\n-------------------------')
        return data

    @staticmethod
    def read_config_from_args(path: str) -> str:
        with open(path, 'r') as file:
            data = file.read().strip()
        log.info(f'Bot settings:\n{data}\n-------------------------')
        return data

    def _click_like_btn(self, like: str) -> None:
        try:
            self.driver.find_element_by_css_selector(f'svg[aria-label="{like}"]').click()
            time.sleep(random.randint(55, 75))
            self.count += 1
        except (NoSuchElementException, ElementNotInteractableException) as e:
            log.error(f'Cant find "Like" on page, sleep 10 seconds\n{str(e) + traceback.format_exc()}')
            time.sleep(random.randint(6, 20))
            pass

    def _discover_tag(self, hashtag) -> None:
        driver = self.driver
        time.sleep(5)
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

    def _get_photo_array(self) -> list:
        final_href_array = []
        for i in range(1, 4):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            href_objects = self.driver.find_elements_by_tag_name('a')
            photo_href = [elem.get_attribute('href') for elem in href_objects if
                          '.com/p/' in elem.get_attribute('href')]
            [final_href_array.append(href) for href in photo_href if href not in final_href_array]
        return final_href_array

    def collect_actions(self, hashtag: str, like: str) -> None:
        self._discover_tag(hashtag)
        array = self._get_photo_array()
        for item in array:
            log.info(f'Current parsed url is: {item}')
            self.driver.get(item)
            time.sleep(random.randint(2, 4))
            self._click_like_btn(like)
            log.info(f'Кол-во лайков за запуск = {self.count}')
            if self.count % 25 == 0:
                log.info('Count likes are multiples 25, program sleep 1800 seconds [30 minutes]')
                time.sleep(1800)


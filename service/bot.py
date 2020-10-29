import os
import random
import re
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)
from selenium.webdriver.common.keys import Keys
from .utils import log, BASE_DIR
from bs4 import BeautifulSoup as bs


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
            btn = self.driver.find_element_by_css_selector(f'svg[aria-label="{like}"]')
            log.info(f'Height of like button: {btn.get_attribute("height")}')
            if btn.get_attribute("height") == '24':
                btn.click()
                time.sleep(random.randint(5, 15))
                self.count += 1
            time.sleep(random.randint(1, 4))
        except (NoSuchElementException, ElementNotInteractableException) as e:
            log.error(f'Cant find "Like" on page, sleep 10 seconds {str(e) + traceback.format_exc()}')
        except ElementClickInterceptedException as e:
            log.error(f'the element finds off-screen {str(e) + traceback.format_exc()}')

    def _count_likes_comments(self) -> dict:
        html = self._html_tree()
        try:
            for element in html.find_all('meta'):
                if element.get('content') is not None and 'Comments' in str(element.get('content')):
                    string = element.get('content')
                    log.warning(string)
                    value = re.match(r'(\d+.Likes)\W+(\d+.Comments)', string.replace(',', '')).groups()
                    likes = int(value[0][:-6])
                    comments = int(value[1][:-8])
                    data = {'like': likes, 'comment': comments}
                    log.info(f'Counts: {str(data)}')
                    return data
        except (TypeError, AttributeError):
            log.error('Could not be found meta information with like/comment on the page, try to get info with driver')
            count = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div')
            likes = int(count.text.strip()[:-6].replace(',', ''))
            return {'like': likes, 'comment': 5}

    def _html_tree(self):
        data = self.driver.page_source
        soup = bs(data, 'lxml')
        return soup

    def get_html_page(self) -> None:
        soup = self._html_tree()
        for element in soup.find_all('meta'):
            # if element.get('content') is not None and 'Comments' in str(element.get('content')):
            #     item = element.get('content')
            #     re_item = re.match(r'(\d+.Likes)\W+(\d+.Comments)', item).groups()
            #     log.info(item)
            #     log.info(re_item[0][:-6])
            #     log.info(re_item[1][:-8])
            if element.get('property') == 'instapp:hashtags':
                item = element.get('content')
                log.info(item)

    def get_description_post(self) -> None:
        data = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')
        log.info(f'Description: {str(data.text.strip())}')

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
            self.driver.get(item+'?hl=en')
            time.sleep(random.randint(3, 5))
            self.get_description_post()
            self.get_html_page()
            try:
                counts = self._count_likes_comments()
                if counts['like'] > 40 and counts['comment'] > 2:
                    self._click_like_btn(like)
            except TypeError:
                # TODO: Убрать это исключение
                pass
            log.info(f'Кол-во лайков за запуск = {self.count}')
            #if self.count % 25 == 0:
            #    log.info('Count likes are multiples 25, program sleep 1800 seconds [30 minutes]')
            #    time.sleep(1800)


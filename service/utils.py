from loguru import logger as log
import os
import argparse

log.add('service-bot.log', format='{time} [{level}] {module} {name} {function} - {message}',
                 level='INFO', compression='tar.gz', rotation='3 KB')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_parser():
    parser = argparse.ArgumentParser(description='InstaBot commands help')
    parser.add_argument('-l', '--login', action="store", dest="login", type=str)
    parser.add_argument('-p', '--password', action="store", dest="password", type=str)
    parser.add_argument('-t', '--path', action="store", default='$HOME', type=str)
    parser.add_argument('-c', '--chromedriver', action="store", type=str)
    parser.add_argument('-g', '--like', action="store", default='Like', type=str)

    args = parser.parse_args()
    return args

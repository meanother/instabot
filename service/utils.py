import logging
import os
import argparse


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(funcName)s - %(message)s',
)
log = logging.getLogger(__name__)


def create_parser():
    parser = argparse.ArgumentParser(description='InstaBot commands help')
    parser.add_argument('-l', '--login', action="store", dest="login", type=str)
    parser.add_argument('-p', '--password', action="store", dest="password", type=str)
    parser.add_argument('-t', '--path', action="store", default='$HOME', type=str)
    parser.add_argument('-c', '--chromedriver', action="store", type=str)
    parser.add_argument('-g', '--like', action="store", default='Like', type=str)

    args = parser.parse_args()
    return args

from service.bot import Bot
from service.utils import log

import argparse
import time


def main():
    # TODO Добавить ограничения для лайков новых аккаунтов, 25лайков/час или 300лайков/сутки

    parser = argparse.ArgumentParser(description='InstaBot commands help')
    parser.add_argument('-l', '--login', action="store", dest="login", type=str)
    parser.add_argument('-p', '--password', action="store", dest="password", type=str)
    parser.add_argument('-t', '--path', action="store", default='$HOME', type=str)
    parser.add_argument('-c', '--chromedriver', action="store", type=str)
    parser.add_argument('-g', '--like', action="store", default='Like', type=str)

    args = parser.parse_args()

    Bot.hello()
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
from service.bot import Bot
from service.utils import log, create_parser

import time
import traceback


def main():
    # TODO Добавить ограничения для лайков новых аккаунтов, 25лайков/час или 300лайков/сутки
    # https://socialkit.ru/blog/post/limity-instagram-2020
    while True:
        args = create_parser()
        bot = Bot(args.login, args.password, args.chromedriver)
        config = bot.read_config_from_args(args.path)
        bot.hello()
        try:
            bot.login()
            for tag in config.split('\n'):
                log.info(f'Current hashtag is #{tag}')
                bot.collect_actions(tag, args.like)
                time.sleep(60)
        except Exception as e:
            log.error(str(e) + traceback.format_exc())
            time.sleep(120)
            bot.close_browser()
            log.info('Sleep 2 min after ERROR')


if __name__ == "__main__":
    main()
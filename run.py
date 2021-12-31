import asyncio
import bot
from os.path import isfile
from logging import getLogger, INFO
from logs import ClickStreamHandler, ColouredFormatter
from importlib import reload


def main(module):
    logger = getLogger(__name__)
    handler = ClickStreamHandler()
    handler.setFormatter(ColouredFormatter("[%(levelname)s][%(filename)s] %(message)s"))
    logger.setLevel(INFO)
    logger.addHandler(handler)
    loop = asyncio.get_event_loop()
    while True:
        bot, start = module.get(logger)
        try:
            loop.run_until_complete(start())
        except KeyboardInterrupt:
            if not bot.is_closed():
                loop.run_until_complete(bot.close())
            if not isfile(".state"):
                break
            module = reload(module)
    loop.close()


if __name__ == "__main__":
    main(bot)

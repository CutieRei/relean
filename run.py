from logs import ClickStreamHandler, ColouredFormatter
from logging import getLogger, INFO
from logs import ClickStreamHandler, ColouredFormatter
from bot import get

def main():
    logger = getLogger(__name__)
    handler = ClickStreamHandler()
    handler.setFormatter(ColouredFormatter("[%(levelname)s][%(filename)s] %(message)s"))
    logger.setLevel(INFO)
    logger.addHandler(handler)
    _, run = get(logger)
    run()

if __name__ == "__main__":
    main()
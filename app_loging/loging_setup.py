import logging

# TODO
#  добавить FileHandler, чтобы писать логи в файл:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# создаём общий логгер
logger = logging.getLogger("my_app")


def loger_info(info: str):
    logger.info(info)

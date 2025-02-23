import logging
from setting.setting import LOG_FILE


# задаем параметры для логирования
my_log_config = logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s- %(name)s - %(message)s",
    filename=LOG_FILE,
    filemode="w",
    encoding="UTF-8",
)

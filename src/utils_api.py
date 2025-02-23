import logging
from abc import ABC, abstractmethod
from typing import Any

import requests

from setting.log_setting import my_log_config

logging.basicConfig = my_log_config
# определяем именные логеры
logging_api = logging.getLogger("api_utils")


class AbstractHH(ABC):
    """Абстрактный класс который моделирует создание классов по работе с API сайта HH.ru"""

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def search_vacancion(self, keyword:str):
        pass


class HH(AbstractHH):
    """класс который взаимодействует с сайтом hh через API"""

    def __init__(self):
        """Инициализация объекта класса HH"""

        logging_api.info("Старт инициализации объекта классса HH")  # логирование
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        logging_api.info(
            f"Инициализации объекта классса HH завершена, параметры {self.__params}"
        )  # логирование

    def __str__(self) -> str:
        """Выыодит на печать информацию об объекте класса HH"""
        logging_api.info(
            f"Вызван на печать объект класса {self.__class__.__name__}, текущие парамметры:"
            f" {self.__params} содержит {len(self.__vacancies)} вакансий"
        )
        return (
            f"Класс {self.__class__.__name__}, текущие парамметры: "
            f"{self.__params} содержит {len(self.__vacancies)} вакансий"
        )

    def connection(self) -> None:
        """Метод отвечающий за взаимодействие с приватным методом __connection"""

        HH.__connection(self)

    def __connection(self) -> int:
        """Метод который реадизует функционал подключения к серверу"""

        logging_api.info("Проводим подклчение к серверу")  # логирование
        response = requests.get(self.__url)
        logging_api.info(
            f"Ответ полученный от сервера имеет код {response.status_code}"
        )  # логирование
        return response.status_code

    def search_vacancion(self, keyword:str) ->list[dict[Any, Any]]:
        """Производит поиск на сайте hh.ru вакансий, которые содержат искомый текст"""

        logging_api.info(f"Старт сбора вакансий по тексту {keyword}")  # логирование
        if self.__connection() == 200:
            self.__params["text"] = keyword
            while True:
                try:
                    logging_api.info(
                        f"Обработали информацию по странице № {self.__params['page']}"
                    )  # логирование
                    response = requests.get(
                        self.__url, headers=self.__headers, params=self.__params
                    )
                    vacancies = response.json()["items"]
                    self.__vacancies.extend(vacancies)
                    self.__params["page"] += 1
                except Exception:
                    print(
                        f"Работа поиска завершена, всего найдено {len(self.__vacancies)} вакансий"
                    )
                    logging_api.info(
                        "Завершена обработка поиска вакансий, всего найдено {len(self.vacancies)} вакансий"
                    )
                    break
            return self.__vacancies
        else:
            print(
                f"Обнаружена ошибка при подлючении к серверу, код ошибки: {self.__connection()}"
            )
            logging_api.error(
                f"Обнаружена ошибка при подлючении к серверу, код ошибки: {self.__connection()}"
            )

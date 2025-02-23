from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from setting.log_setting import my_log_config

logging.basicConfig = my_log_config
vacancy_log = logging.getLogger("vacancy_modul_log")


class abstract_vacancies(ABC):
    """Абстрактный класс для работы с вакансииями"""

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def validation_solary_vacancy_from(self):
        pass

    @abstractmethod
    def validation_solary_vacancy_to(self):
        pass

    @abstractmethod
    def compare_jobs(self, vac2: Vacancies):
        pass


class Vacancies:
    """Класс для работы с объектами вакансий"""

    vacancies_object_list: list[Any]

    vacancies_object_list = []
    __slots__ = ("name", "address", "salary", "vacancies_url", "work_format")

    def __init__(self, name, address, salary, vacancies_url, work_format):
        """Инициализация объекта класса Vacancies"""

        vacancy_log.info(
            f"Старт инициализации объекта класса Vacancies c"
            f" входными данными {name}, {address}, {salary}, {vacancies_url}, {work_format}"
        )
        self.name = name
        self.address = address
        self.salary = salary
        self.__validation_solary_vacancy_from()
        self.__validation_solary_vacancy_to()
        self.vacancies_url = vacancies_url
        self.work_format = work_format
        vacancy_log.info("Завершена инициализация объекта класса Vacancies")

    def __str__(self) -> str:
        """метод который определяет результат функции print для объекта классса Vacancies"""
        return (
            f"Объект класса Vacancies {self.name}, {self.address}, "
            f"{self.salary}, {self.vacancies_url}, {self.work_format} "
        )

    def __sub__(self, vac2) -> int:
        """Магический метод вычитания двух вакансий"""

        if self.salary["to"] != vac2.salary["to"]:
            return self.salary["to"] - vac2.salary["to"]
        elif self.salary["from"] != vac2.salary["from"]:
            return self.salary["from"] - vac2.salary["from"]
        else:
            return 0

    def __validation_solary_vacancy_from(self) -> None:
        """Валидирует значение зарплаты указанное в ваканссии по нижнему критерию.
        если данных нет, или они не относится к ччиловому формату - ставит 0,
        если данные ниже нуля, так же заменяет на 0 значение"""

        vacancy_log.info("Старт валидации запрлаты по нижнему значение}")

        if isinstance(self.salary, dict) is False:
            self.salary = {"from": 0, "to": 0}
        try:
            if (
                isinstance(self.salary["from"], (float, int))
                and self.salary["from"] > 0
            ):
                pass
            else:
                self.salary["from"] = 0
        except Exception:
            self.salary["from"] = 0
        vacancy_log.info(
            f"Валидация запрлаты по нижнему значению проведена, по выходу {self.salary['from']}"
        )

    def __validation_solary_vacancy_to(self) -> None:
        """Валидирует значение зарплаты по вверхнему пределу
        если значения нет, оно не ччисловое или меньше нижнего предела
        - возвращает значение нижнего предела"""

        vacancy_log.info("Старт валидации запрлаты по верхнему значению")
        try:
            if (
                isinstance(self.salary["to"], (float, int))
                and self.salary["to"] >= self.salary["from"]
            ):
                pass
            else:
                self.salary["to"] = self.salary["from"]
        except Exception:
            self.salary["to"] = self.salary["from"]
        vacancy_log.info(
            f"Валидация запрлаты по верхнему значению проведена, по выходу {self.salary['to']}"
        )

    @staticmethod
    def check_object_class(test_object: Any) -> None:
        """Проверяет принадлежность объекта к классу Вакансии
        и возбуждает исключение если объект не соответствует классу"""

        if isinstance(test_object, Vacancies) is False:
            raise TypeError("Выбран объект не подходящего классса")

    def compare_jobs(self, vac2: Vacancies) -> Vacancies:
        """Принимает две объекта класса вакансии и возвращает ту. у которой более высокая максмальная зарплата"""

        Vacancies.check_object_class(vac2)
        if self - vac2 > 0:
            return self
        elif self - vac2 < 0:
            return vac2
        else:
            print(
                "Обе вакансии равнознчные по зарплатным условиям, поэтому оставили как есть"
            )
            return self

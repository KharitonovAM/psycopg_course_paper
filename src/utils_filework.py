import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from setting.log_setting import my_log_config
from setting.setting import DATA_FILENAME
from src.utils_vacancies import Vacancies

logging.basicConfig = my_log_config
# определяем именные логеры
logging_filename = logging.getLogger("utils_filework")


class AbsFileWork(ABC):

    @abstractmethod
    def take_data(self):
        pass

    @abstractmethod
    def write_data(self, data: Any):
        pass

    @abstractmethod
    def deldata(self, data_to_del: dict[Any, Any]):
        pass


class FileWork(AbsFileWork):
    """Класс по работе с файлами"""

    def __init__(self, filename: Path = DATA_FILENAME) -> None:
        logging_filename.info("Старт инициализации")
        """Инициализация объекта который взаимодействует с файлами"""

        self.__filename = filename
        logging_filename.info("Завершение инициализации")

    def write_data(self, data: Any) -> None:
        """метод который отвечает за внесение данных в json файл"""

        logging_filename.info(f"Пытаемся записать в {self.__filename} данные")

        try:
            data_from_file = self.take_data()
            data_from_file.extend(data)
        except Exception:
            data_from_file = data
        with open(self.__filename, "w") as f:
            json.dump(data_from_file, f, indent=4, ensure_ascii=True)
        logging_filename.info(f"Данные в {self.__filename} записаны")

    def take_data(self) -> list[dict[Any, Any]]:
        """Метод который отвечает за получение данных из json-файла
        и возвращает полченные значения"""

        logging_filename.info(f"Пытаемся прочитето из {self.__filename} данные")
        with open(self.__filename) as f:
            my_data = json.load(f)
            logging_filename.info(f"Данные из {self.__filename} прочитаны")
        return my_data

    def deldata(self, data_to_del: dict[Any, Any]) -> None:
        """Метод для удаления данных в файле"""

        temp_data = self.take_data()
        if data_to_del in temp_data:
            temp_data.remove(data_to_del)

        with open(self.__filename, "w") as f:
            json.dump(temp_data, f, ensure_ascii=True)

    def add_new_vacancy_to_json_file(self, vac_data: Vacancies) -> None:
        """Модуль добавляющий данные по новой вакансии в файл,
        если данных по этой ваканссии ранее н было добавлено"""

        temp_data = self.take_data()
        if vac_data[0] not in temp_data:
            self.write_data(vac_data)
        else:
            print("Эта вакансия уже имеется в файле")

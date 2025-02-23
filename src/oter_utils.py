from typing import Any

from src.utils_vacancies import Vacancies


class DataWork:
    """вспомогательные функции предназначенные для упрощения работы прораммы"""

    def sort_vacancies(self, vac_list: list[Vacancies]) -> list[Vacancies]:
        """Принимает на вход список объектов класса Vacancy и возвращает
        список отсортированные по верхнему пределу зарплаты"""

        sorted_list = sorted(vac_list, key=lambda x: x.salary["to"], reverse=True)

        return sorted_list

    def make_vacancy_object(self, vacation_data: dict[Any, Any]) -> Vacancies:
        """Формирует объект класса вакансии из списка полученного чрез API"""
        return Vacancies(
            vacation_data["name"],
            vacation_data["address"],
            vacation_data["salary"],
            vacation_data["alternate_url"],
            vacation_data["work_schedule_by_days"],
        )

    def make_data_to_json_from_vacancy_object_list(
        self, vacancy_list: list[Vacancies]
    ) -> list[dict[str,Any]]:
        """Формирует спиисок с данными подходящими для записи в json файл из
        списка объектов класса Json"""

        return [
            {
                "name": x.name,
                "address": x.address,
                "salary": x.address,
                "alternate_url": x.address,
                "work_schedule_by_days": x.work_format,
            }
            for x in vacancy_list
        ]

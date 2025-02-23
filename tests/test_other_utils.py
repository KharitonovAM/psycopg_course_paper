from typing import Any

from src.oter_utils import DataWork
from src.utils_vacancies import Vacancies


def test_sort_vacancies(vac_list: list[Vacancies]):
    """Тест проверяет что функция получив список из вакансий вернёт его отсортированного по зарплате по убыванию"""

    test_data = DataWork()
    sorted_list = test_data.sort_vacancies(vac_list)
    assert sorted_list[0] == vac_list[4]
    assert sorted_list[1] == vac_list[1]
    assert sorted_list[2] == vac_list[0]
    assert sorted_list[3] == vac_list[3]


def test_make_vacancy_object(examle_from_hh: list[dict[Any, Any]]):
    """Тест который проверет что функция создаёт список объектов Вакансии
    принимая на вход json-data из hh"""

    test_data = DataWork()
    test_assert_data = Vacancies(
        examle_from_hh[0]["name"],
        examle_from_hh[0]["address"],
        examle_from_hh[0]["salary"],
        examle_from_hh[0]["alternate_url"],
        examle_from_hh[0]["work_schedule_by_days"],
    )

    assert (
        test_data.make_vacancy_object(examle_from_hh[0]).name == test_assert_data.name
    )

import pytest

from src.utils_vacancies import Vacancies


def test_creation_vacanci_object() -> None:
    """Тест проверяет корректность создания объекта класса Vacancies"""

    test_vacancy = Vacancies(
        "тестовая вакансия",
        "adress",
        {"from": 150000, "to": 300000},
        "http://myurl.com",
        "daily",
    )
    assert test_vacancy.name == "тестовая вакансия"
    assert test_vacancy.address == "adress"
    assert test_vacancy.salary == {"from": 150000, "to": 300000}
    assert test_vacancy.vacancies_url == "http://myurl.com"
    assert test_vacancy.work_format == "daily"


def test_compare_jobs_by_from(vac1: Vacancies, vac2: Vacancies) -> None:
    """Тестируем корректность функционала по сравнению двух работ по зарплате
    передаем в тест две вакансии у которых равный верхний предел, но отличаается нижний
    """

    assert vac1.compare_jobs(vac2) == vac1


def test_compare_jobs2_by_to(vac2: Vacancies, vac3: Vacancies) -> None:
    """Тестируем корректность функционала по сравнению двух работ по зарплате
    передаем в тест две вакансии у которых равный нижний предел, но отличаается верхний
    """

    assert vac2.compare_jobs(vac3) == vac2


def test_compare_jobs3_by_to(vac2: Vacancies) -> None:
    """Тестируем корректность функционала по сравнению двух одинаковых
    по параметру зарплата вакансий"""

    temp = vac2
    assert temp.compare_jobs(vac2) == temp


def test_valifashion_vacansii_to_low_0() -> None:
    """тестируем, что при инициализации объекта класса Vacansy
    происходит валидация данных"""

    test_vacancy = Vacancies(
        "тестовая вакансия",
        "adress",
        {"from": -1, "to": 300000},
        "http://myurl.com",
        "daily",
    )
    assert test_vacancy.salary["from"] == 0


def test_valifashion_vacansii_from_is_apsend() -> None:
    """тестируем, что при инициализации объекта класса Vacansy
    происходит валидация данных"""

    test_vacancy = Vacancies(
        "тестовая вакансия", "adress", {"to": 300000}, "http://myurl.com", "daily"
    )
    assert test_vacancy.salary["from"] == 0


def test_valifashion_vacansii_from_not_digit() -> None:
    """тестируем, что при инициализации объекта класса Vacansy
    происходит валидация данных"""

    test_vacancy = Vacancies(
        "тестовая вакансия",
        "adress",
        {"from": "-1", "to": 300000},
        "http://myurl.com",
        "daily",
    )
    assert test_vacancy.salary["from"] == 0


def test_valifashion_vacansii_to_low_from() -> None:
    """тестируем, что при инициализации объекта класса Vacansy
    происходит валидация данных"""

    test_vacancy = Vacancies(
        "тестовая вакансия",
        "adress",
        {"from": 500000, "to": 300000},
        "http://myurl.com",
        "daily",
    )
    assert test_vacancy.salary["from"] == 500000


def test_valifashion_vacansii_to_is_apsend() -> None:
    """тестируем, что при инициализации объекта класса Vacansy
    происходит валидация данных"""

    test_vacancy = Vacancies(
        "тестовая вакансия", "adress", {"from": 300000}, "http://myurl.com", "daily"
    )
    assert test_vacancy.salary["from"] == 300000


def test_valifashion_vacansii_from_not_digit1() -> None:
    """тестируем, что при инициализации объекта класса Vacansy
    происходит валидация данных"""

    test_vacancy = Vacancies(
        "тестовая вакансия",
        "adress",
        {"from": 100000, "to": "ghjhghg"},
        "http://myurl.com",
        "daily",
    )
    assert test_vacancy.salary["from"] == 100000


def test_error_check_object_class(vac1: Vacancies) -> None:
    with pytest.raises(TypeError):
        assert vac1.compare_jobs({"salary": {"to": 10, "from": 1}})

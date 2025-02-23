from unittest.mock import patch

from src.utils_api import HH


@patch("src.utils_api.requests.get")
def test_api_correct_connection_work(get, capsys):
    """Мокирующий тест, который проверяет, что функция connection возвращает корректные данные"""
    get.return_value.status_code = 200
    z = HH()
    print(z)
    myprint = capsys.readouterr()
    assert myprint.out == (
        "Класс HH, текущие парамметры: {'text': '', 'page': 0, 'per_page': 100} "
        "содержит 0 вакансий\n"
    )


@patch("src.utils_api.requests.get")
def test_api_correct_work_take_data_from_api(get, capsys):
    """Мокирующий тест, который проверяет, что функция возвращает на экран
    сообщение об ошибке подключениия к сервру при получении ответа отличного от 200"""

    get.return_value.status_code = 400
    z = HH()
    z.search_vacancion("looking")
    myprint = capsys.readouterr()
    assert (
        myprint.out == "Обнаружена ошибка при подлючении к серверу, код ошибки: 400\n"
    )


@patch("src.utils_api.requests.get")
def test_api_correct_work_take_data_from_api2(get, capsys):
    """Мокирующий тест, который проверяет, что функция search_vacancion возвращает
    на экран сообщение соответствующее ожидаемым"""

    get.return_value.status_code = 200
    get.return_value.json = ""
    z = HH()
    z.search_vacancion("looking")
    myprint = capsys.readouterr()
    assert myprint.out == "Работа поиска завершена, всего найдено 0 вакансий\n"

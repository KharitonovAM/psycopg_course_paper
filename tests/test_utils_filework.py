import json
import os
from typing import Any

from src.utils_filework import FileWork


def test_take_data(json_data_1: list[dict[Any, Any]]) -> None:
    """Тест который принимает на вход текстуру и проверяет,
    что в файл запиисываются данные совпадающие с текстурой"""

    temp_file = "mydata.json"
    with open(temp_file, "w") as mf:
        json.dump(json_data_1, mf)
    z = FileWork(temp_file)
    my_data = z.take_data()
    os.remove(temp_file)
    assert my_data == json_data_1


def test_write_data(json_data_1: list[dict[Any, Any]]) -> None:
    """Тестирует, что функция по записи данных в json файл работает коректно"""

    temp_file = "mydata.json"
    z = FileWork(temp_file)
    z.write_data(json_data_1)
    with open(temp_file, "r") as mf:
        my_data = json.load(mf)
    os.remove(temp_file)
    assert my_data == json_data_1


def test_delfunc() -> None:
    """Тестируем, что функция корректно удаляет данные из json-файла"""

    a = [{"ghb": {"1": 22}, "перемен2": {"4": 5}}, {"4": 14, "gg": 2}]
    k = FileWork("mydata.json")
    k.write_data(a)
    k.deldata({"4": 14, "gg": 2})
    test_data = k.take_data()
    os.remove("mydata.json")
    assert test_data == [{"ghb": {"1": 22}, "перемен2": {"4": 5}}]


def test_adding_data_which_exist_in_json_file(
    json_data_3: list[dict[Any, Any]],
) -> None:
    """Тестируем, что при при попытке добавить уже имеющую информацию в json-файл
    исходное содержимое не не измениться, а дубль не добавится"""

    k = FileWork("mydata.json")
    k.write_data(json_data_3)
    k.add_new_vacancy_to_json_file([{"gg": 2, "4": 14}])
    result_data = k.take_data()
    os.remove("mydata.json")
    assert result_data == json_data_3

from src.oter_utils import DataWork
from src.utils_api import HH
from src.utils_filework import FileWork


def main() -> None:
    """Функция отвечающая за взаимодействие с пользователем"""

    other_functions = DataWork()
    filework = FileWork()

    while True:

        print(
            """
        \tДобро пожаловать в программу, которая позволит вам упростить взаимодействие с сайтом hh.ru
        Программа позволит вам упростить получение информации, и поддердивает следующий функционал:
        - поиск по кючевому слову
        - фильтрацию по зарплате
        - возможность вывести ограниченное количество вакансий (с максимальной запрлатой)

        Данные по заработной плате валидируются, если значение не было указано, то оно принимает значение равное 0
        """
        )

        work_control = input("\tЕсли хотите завершить работу программы нажмите Q\n")
        if work_control.upper() == "Q":
            input("\nРабота программы прекращена. Хорошего дня!")
            break

        lookihg_word = input(
            "Введите слово, по которому будем искать вакансии на сайте hh.ru\n"
        )
        vacansy_object = HH()
        vacansy_list = vacansy_object.search_vacancion(lookihg_word)
        vacansy_object_list = list(
            map(other_functions.make_vacancy_object, vacansy_list)
        )
        print(f"Поиск вакансий завершен, всего нашлось {len(vacansy_object_list)}")
        user_sorted = input(
            "Отсортировать полученный список по зарплате? (от наибольшей к наименьшей) y/n\n"
        )
        while user_sorted.lower() not in ("y", "n"):
            user_sorted = input(
                "Вы ввели неверный вариант, повторите пожалуйста ввод\n"
            )
        if user_sorted.upper() == "Y":
            vacansy_object_list = other_functions.sort_vacancies(vacansy_object_list)
        number_vacancies = input(
            """Какое количество вакансий вы хотите просмотреть?
         Если хотите просмотреть все вакансии - введите любой нечисловой символ\n"""
        )
        if (
            number_vacancies.isdigit() is False
            or int(number_vacancies) < 0
            or int(number_vacancies) > len(vacansy_object_list)
        ):
            number_vacancies = len(vacansy_object_list)
        vacansy_object_list = vacansy_object_list[:number_vacancies]
        print_before_saving = input("Вывести список на экран? (Y/N)")
        while print_before_saving.lower() not in ("y", "n"):
            print_before_saving = input(
                "Вы ввели неверный вариант, повторите пожалуйста ввод\n"
            )
        if print_before_saving.lower() == "y":
            for i, v in enumerate(vacansy_object_list):
                print(i + 1, "---", v)

        data_at_json_format = (
            other_functions.make_data_to_json_from_vacancy_object_list(
                vacansy_object_list
            )
        )
        filework.write_data(data_at_json_format)
        input("Данные записаны в файл, для продолжения работы нажмите любую клавишу")

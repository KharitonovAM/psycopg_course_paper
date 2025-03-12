from src.utils_api import HH
from src.utils_bd import DBManager


def main() -> None:
    """Функция отвечающая за взаимодействие с пользователем"""

    while True:

        print(
            """
        \tДобро пожаловать в программу, которая позволит вам упростить взаимодействие с сайтом hh.ru
        Программа позволит упростить получение информации, а так же хранить данные по вакансиям компаний,
        которые вас интересуют.
        Для её использования следуйте подсказкам на вашем экране.
        """
        )

        work_control = input("\tЕсли хотите завершить работу программы нажмите Q\n")
        if work_control.upper() == "Q":
            input("\nРабота программы прекращена. Хорошего дня!")
            break

        dbname = input(
            "Введите наименоваине базы данных к которой будемм подлючаться.\n"
            "Если такой базы данных не существует, она будет создана\n"
        )
        my_database = DBManager(dbname)
        try:
            companies_in_db = my_database.get_companies_names()
            if len(companies_in_db) == 0:
                print("В базе данных нет компаний")
            else:
                message = f"Сейчас в БД содержится {len(companies_in_db)} компаний, а именно: "
                print(message, companies_in_db)
        except Exception:
            my_database.create_database()
            print("Создана новая база данных")
            companies_in_db = my_database.get_companies_names()

        while len(companies_in_db) < 10:
            print(
                f"В базе данных должно быыть 10 компаний, у вас пока {len(companies_in_db)}"
            )
            new_company_name = input(
                "Введите название компании, которую добавил в базу данных: \n"
            )
            vac_data = HH()
            vac_data.search_vacancion(new_company_name)
            list_to_load = vac_data.search_company(new_company_name)
            if list_to_load:
                comp_data, vac_data = vac_data.make_data_for_loading_to_bd(list_to_load)
                my_database.insert_data_to_table(comp_data, vac_data)
            else:
                print("Компания с таким наименованием не размещает вакансии на hh.ru")
            companies_in_db = my_database.get_companies_names()

        user_choose = ""
        while user_choose != "8":
            user_choose = input(
                """В базе данных достаточно компаний, теперь можно приступить к работе с данными из базы данных
            Выберете, какие действия далее выполнить?
            1 - Обновить данные по вакансиям
            2 - Получить список всех компаний и количество вакансий у каждой компании
            3 - Получить список всех вакансий
            4 - получает среднюю зарплату по вакансиям
            5 - Получить список всех вакансий, у которых зарплата выше средней
            6 - Отобрать вакансии с определенным названием
            7 - Отобразить данные по всем компания
            8 - Запустить программу еще раз
            """
            )
            match user_choose:
                case "1":
                    company_names = my_database.get_companies_names()
                    company_names = list(set([x.lower() for x in company_names]))
                    my_database.clear_all_tables()
                    for company_name in company_names:
                        vac_data = HH()
                        vac_data.search_vacancion(company_name)
                        list_to_load = vac_data.search_company(company_name)
                        comp_data, vac_data = vac_data.make_data_for_loading_to_bd(
                            list_to_load
                        )
                        my_database.insert_data_to_table(comp_data, vac_data)
                    print("Список вакансий обновлён")
                case "2":
                    for item in my_database.get_companies_and_vacancies_count():
                        print(item[0], "----", item[1])
                case "3":
                    for i, v in enumerate(my_database.get_all_vacancies()):
                        print(i, "---", v)
                case "4":
                    print(
                        "Средняя зарплата по нижнему параметру",
                        my_database.get_avg_salary()[0],
                    )
                    print(
                        "Средняя зарплата по нижнему параметру",
                        my_database.get_avg_salary()[1],
                    )
                case "5":
                    for i, v in enumerate(
                        my_database.get_vacancies_with_higher_salary()
                    ):
                        print(i, "---", v)
                case "6":
                    looking_word = input(
                        "Введите слово, чтобы найти вакансии в названии которых оно встречается\n"
                    )
                    print(my_database.get_vacancies_with_keyword(looking_word))
                case "7":
                    print(my_database.get_companies_names())


if __name__ == "__main__":
    main()

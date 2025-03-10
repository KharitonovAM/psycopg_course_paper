import psycopg2
from abc import ABC, abstractmethod

from setting.db_config import config

class abstrate_dbmaneger(ABC):
    '''Абстракный класс по работе с БД'''

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''
        pass

    @abstractmethod
    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
        pass

    @abstractmethod
    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям'''
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова'''
        pass

class DBManager(abstrate_dbmaneger):
    '''Класс по взаимодействию с базой данных'''

    def __init__(self, database_name):
        self.database_name = database_name

    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях,
        если такая БД уже имеется - происходит её удаление и создане новой БД"""

        params = config()
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP  DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        conn.close()


        conn = psycopg2.connect(dbname=self.database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacanscies_id VARCHAR(80) PRIMARY KEY,
                    vacancy_name VARCHAR(255) NOT NULL,
                    company_id VARCHAR(80),
                    salary_from INT,
                    salary_to INT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    company_id VARCHAR(80) PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    company_url VARCHAR(255) NOT NULL
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                ALTER TABLE vacancies ADD CONSTRAINT company_id FOREIGN KEY(company_id) REFERENCES companies(company_id);
            """)

        conn.commit()
        conn.close()


    def insert_data_to_table(self, list_company = [], list_vacancy = []):
        '''функция которая принимает списки, которые нужно загрузить в БД
        и загружает иих в таблицы, если подан пустой список то он игнорируется'''

        params = config()

        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            if list_company:
                for item in list_company:
                    cur.execute(f'INSERT INTO companies (company_id, company_name, company_url) VALUES {item[0], item[1], item[2]}')

            if list_vacancy:
                for item in list_vacancy:
                    cur.execute(f'INSERT INTO vacancies (vacanscies_id, vacancy_name, company_id, salary_from, salary_to) VALUES {item[0], item[1], item[2], item[5], item[4]};')

        conn.commit()
        conn.close()



    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''

        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT companies.company_name, COUNT(vacancies.company_id) 
                FROM companies INNER JOIN vacancies on companies.company_id = vacancies.company_id
                GROUP BY companies.company_name
                """)
            data_companies_and_vacancies_count = cur.fetchall()
        conn.close()
        return data_companies_and_vacancies_count




    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''

        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT vacancies.vacancy_name, companies.company_name, vacancies.salary_from, vacancies.salary_to
                        FROM companies INNER JOIN vacancies on companies.company_id = vacancies.company_id
                        """)
            data_all_vacancies = cur.fetchall()
        conn.close()
        return data_all_vacancies


    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям'''

        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT AVG( salary_from), AVG( salary_to)
                        FROM vacancies
                        """)
            data_avg_salary = cur.fetchall()
        conn.close()
        data_avg_salary = [int(data_avg_salary[0][0]), int(data_avg_salary[0][1])]
        return data_avg_salary




    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        сравнение выполняется по параметру верхней границы вакансии'''

        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
            SELECT vacancies.vacancy_name, companies.company_name, vacancies.salary_from, vacancies.salary_to
            FROM companies INNER JOIN vacancies on companies.company_id = vacancies.company_id
            WHERE vacancies.salary_from >  (SELECT AVG(vacancies.salary_from) from vacancies)
            """)
            vacancies_with_higher_salary = cur.fetchall()
        conn.close()
        return vacancies_with_higher_salary


    def get_vacancies_with_keyword(self, looking_word):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова'''

        params = config()
        conn = psycopg2.connect(dbname=self.database_name, **params)
        with conn.cursor() as cur:
            cur.execute(f'SELECT vacancies.vacancy_name, companies.company_name, vacancies.salary_from, vacancies.salary_to '
                        f'FROM companies INNER JOIN vacancies on companies.company_id = vacancies.company_id '
                        f"WHERE vacancies.vacancy_name LIKE '%{looking_word}%';"
                    )
            vacancies_with_higher_salary = cur.fetchall()
        conn.close()
        return vacancies_with_higher_salary


#
#
#
#
#
# l = DBManager('my_test4')
# l.create_database()
# # q = l.get_all_vacancies()
# # print(q)
# # l.get_companies_and_vacancies_count()
# q = [['9754213', 'МедПроф', 'https://hh.ru/employer/9754213'],['8918366', 'Медпроф', 'https://hh.ru/employer/8918366']]
# w = [['117958903', 'Водитель с личным автомобилем (выездные профосмотры)', '9754213', {'city': 'Санкт-Петербург', 'street': 'Лиговский проспект', 'building': '50Д', 'lat': 59.924984, 'lng': 30.362311, 'description': None, 'raw': 'Санкт-Петербург, Лиговский проспект, 50Д', 'metro': None, 'metro_stations': [], 'id': '16173197'}, 80000, 80000],
# ['118082913', 'Бухгалтер', '9754213', {'city': 'Санкт-Петербург', 'street': 'Лиговский проспект', 'building': '94к2', 'lat': 59.920294, 'lng': 30.355556, 'description': None, 'raw': 'Санкт-Петербург, Лиговский проспект, 94к2', 'metro': None, 'metro_stations': [], 'id': '13319383'}, 85000, 75000]
# ]
#
# l.insert_data_to_table(q, w)
#
# test_data = l.get_all_vacancies()
# print(test_data)
# avg = l.get_avg_salary()
# print(avg)
# jjj = l.get_vacancies_with_higher_salary()
# print(jjj)
# fff = l.get_vacancies_with_keyword('выездные')
# print(type(fff[0]))
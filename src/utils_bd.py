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

    def create_database(self, params):
        """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях,
        если такая БД уже имеется - происходит её удаление и создане новой БД"""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP  DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        conn.close()


        conn = psycopg2.connect(dbname=self.database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacansies (
                    vacansies_id SERIAL PRIMARY KEY,
                    vacancy_name VARCHAR(255) NOT NULL,
                    vacancy_address VARCHAR(255),
                    salary_from INT,
                    salary_to INT,
                    company_name VARCHAR(100)
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL
                )
            """)

        conn.commit()
        conn.close()


    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''
        pass

    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
        pass


    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям'''
        pass


    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''
        pass


    def get_vacancies_with_keyword(self):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова'''
        pass

l = DBManager('my_test1')
l.create_database(config())

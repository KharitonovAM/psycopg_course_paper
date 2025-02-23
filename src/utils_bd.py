from abc import ABC, abstractmethod

class abstrate_dbmaneger(ABC):
    '''Абстракный класс по работе с БД'''

    @abstractmethod
    def get_companies_and_vacancies_count():
        pass

    @abstractmethod
    def get_all_vacancies():
        pass

    @abstractmethod
    def get_avg_salary():
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary():
        pass

    @abstractmethod
    def get_vacancies_with_keyword():
        pass
from hh_class import HeadHunter
import json
from config import config
from db_manager import create_database,insert_employers, insert_vacancies,DBManager,get_selected

def main():
    keyword="Python"
    db_name='vacancies_db'
    search_selected='Y'
    params = config()
    selected={}
    
    #search_selected=input("Ищем только по выбранным организациям (Y/N): ")

    create_database(db_name, params)
    
    if search_selected=="Y":
        selected=get_selected(db_name, params)
        
    
    hh = HeadHunter(keyword,selected)
    hh.get_vacancies(2)

    employers=hh.employers
    vacancies=hh.vacancies

    #print(json.dumps(vacancies, indent=2, ensure_ascii=False))
    #print(json.dumps(employers, indent=2, ensure_ascii=False))

    insert_employers(employers,db_name, params)
    insert_vacancies(vacancies,db_name, params)

    dbm=DBManager(db_name, params)
    
    while 1==1:
        user_input=input("Выбор действия:\n"
                            "1 - Получить список всех компаний и количество вакансий у каждой компании.\n"
                            "2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.\n"
                            "3 - Получить среднюю зарплату по вакансиям.\n"
                            "4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                            "5 - Получить список всех вакансий, в названии которых содержатся переданные в метод слова.\n"
                            "0 - Выход\n"
                        )
        
        if user_input=="1":
            dbm.get_companies_and_vacancies_count()
        elif user_input=="2":            
            dbm.get_all_vacancies()
        elif user_input=="3":            
            dbm.get_avg_salary()
        elif user_input=="4":            
            dbm.get_vacancies_with_higher_salary()
        elif user_input=="5":            
            keyword=input("Введите слово: ")
            dbm.get_vacancies_with_keyword(keyword)
        elif user_input=="0":
            break

if __name__ == '__main__':
    main()
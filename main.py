from hh_class import HeadHunter
import json
from config import config
from db_manager import create_database,insert_employers, insert_vacancies

def main():
    keyword="Python"
    db_name='vacancies_db'

    hh = HeadHunter(keyword)
    hh.get_vacancies(2)

    employers=hh.employers
    vacancies=hh.vacancies

    params = config()

    #print(json.dumps(vacancies, indent=2, ensure_ascii=False))
    #print(json.dumps(employers, indent=2, ensure_ascii=False))

    create_database(db_name, params)
    insert_employers(employers,db_name, params)
    insert_vacancies(vacancies,db_name, params)

if __name__ == '__main__':
    main()
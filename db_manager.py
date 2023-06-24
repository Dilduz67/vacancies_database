import psycopg2

def create_database(database_name: str,params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
    print("Создаем и заполняем базу...\n")

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.commit()
    
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(open("queries.sql", "r", encoding="utf-8").read())
    conn.commit()

    cur.close()
    conn.close()

def insert_employers(employers_list,database_name: str,params: dict):
    """Вставляем работодателей"""
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    postgres_insert_query = """ INSERT INTO employers (id, name, city)
                                           VALUES (%s,%s,%s)"""

    for i in employers_list:
        record_to_insert = (i["employer_id"], i['firm'], i["location"])
        cur.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    count=len(employers_list)
    print(f"{count} записей успешно добавлена в таблицу employers")

    cur.close()
    conn.close()

def insert_vacancies(vacancies_list,database_name: str,params: dict):
    """Вставляем вакансии"""
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    postgres_insert_query = """INSERT INTO public.vacancies(
	                            id, employer_id, name, job_url, requirement, salary_from, salary_to, currency)
	                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

    for i in vacancies_list:
        record_to_insert = (i["job_id"], i['employer_id'], i["job_name"], i["job_url"], i["requirement"], i["salary_from"], i["salary_to"], i["currency"])
        cur.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    count=len(vacancies_list)
    print(f"{count} записей успешно добавлена в таблицу vacancies\n")

    cur.close()
    conn.close()
    
def get_selected(database_name: str,params: dict):
    """Получаем список компаний"""
    selected={}
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    query = "SELECT id , name FROM  public.selected"

    cur.execute(query)

    res=cur.fetchall()

    for row in res:
        selected[row[0]]=row[1]
        
    cur.close()
    conn.close()
    
    return selected
    

class DBManager:
    def __init__(self, database_name, params) -> None:
        self.db_name=database_name
        self.params=params
        
    @staticmethod        
    def get_salary_str(e_name , j_name , salary_from, salary_to, job_url, city):
        str=f"{e_name} ({city}): {j_name} З/п: "
        
        if salary_from !=None or salary_to !=None:
            if salary_from !=None:
                str=str + f"от {salary_from} "
            if salary_to !=None:
                str=str + f"до {salary_to} "
        else:                
            str=str + "не указана "
            
        str=str+ f"URL: {job_url}"
        
        return str
    
    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()
    
        query="""SELECT e.name employer, count(v.id) num_vacancies
                        FROM public.employers e
                        join public.vacancies v on v.employer_id=e.id
                        group by e.name 
                        order by e.name"""
                        
        cur.execute(query)
        res=cur.fetchall()

        for row in res:
            print(f"{row[0]} - {row[1]}")
            
        cur.close()
        conn.close()
        
    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()
    
        query="""SELECT e.name , v.name , salary_from, salary_to, job_url, e.city
                    FROM public.employers e
                    join public.vacancies v on v.employer_id=e.id
                    order by e.name"""
                        
        cur.execute(query)
        res=cur.fetchall()
        
        for row in res:
            str=self.get_salary_str(row[0],row[1],row[2],row[3],row[4],row[5])
            print(str)
            
        cur.close()
        conn.close()
        
    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()
    
        query="""SELECT avg(salary_from), avg(salary_to) FROM public.vacancies where currency='RUR'"""
                        
        cur.execute(query)
        res=cur.fetchall()

        for row in res:
            print(f"Средняя з/п в рублях: от {row[0]} до {row[1]}")
            
        cur.close()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()
    
        query="""SELECT e.name , v.name , v.salary_from, v.salary_to, v.job_url, e.city
                    FROM public.employers e
                    join public.vacancies v on v.employer_id=e.id
                    where v.salary_from >= (SELECT avg(salary_from) FROM public.vacancies where currency='RUR')
		            or 
		            v.salary_to >= (SELECT avg(salary_to) FROM public.vacancies where currency='RUR')
                    and v.currency='RUR'
                    order by e.name"""
                        
        cur.execute(query)
        res=cur.fetchall()
        
        for row in res:
            str=self.get_salary_str(row[0],row[1],row[2],row[3],row[4],row[5])
            print(str)
            
        cur.close()
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        cur = conn.cursor()
    
        query=("SELECT e.name , v.name , v.salary_from, v.salary_to, v.job_url, e.city"
                    " FROM public.employers e"
                    " join public.vacancies v on v.employer_id=e.id"
                    " where v.name like '%" + keyword + "%'" +
                    " order by e.name")

        cur.execute(query)
        res=cur.fetchall()

        for row in res:
            str=self.get_salary_str(row[0],row[1],row[2],row[3],row[4],row[5])
            print(str)
            
        cur.close()
        conn.close()

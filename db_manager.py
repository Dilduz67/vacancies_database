import psycopg2

def create_database(database_name: str,params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname={database_name}) THEN  CREATE DATABASE {database_name}; END IF; ")
    cur.close()
    conn.close()
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(open("queries.sql", "r").read())

    cur.close()
    conn.close()

def insert_employers(employers_list,database_name: str,params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    postgres_insert_query = """ INSERT INTO employers (id, name, city)
                                           VALUES (%s,%s,%s)"""

    for i in employers_list:
        record_to_insert = (i["employer_id"], i['firm'], i["location"])
        cur.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    #count = cur.rowcount
    count=len(employers_list)
    print(f"{count} записей успешно добавлена в таблицу employers")

    cur.close()
    conn.close()

def insert_vacancies(vacancies_list,database_name: str,params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    postgres_insert_query = """INSERT INTO public.vacancies(
	                            id, employer_id, name, job_url, requirement, salary_from, salary_to)
	                            VALUES (%s, %s, %s, %s, %s, %s, %s);"""

    for i in vacancies_list:
        record_to_insert = (i["job_id"], i['employer_id'], i["job_name"], i["job_url"], i["requirement"], i["salary_from"], i["salary_to"])
        cur.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    #count = cur.rowcount
    count=len(vacancies_list)
    print(f"{count} записей успешно добавлена в таблицу employers")

    cur.close()
    conn.close()

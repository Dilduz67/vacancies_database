do $$
begin
IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname='vacancies_db') THEN
	CREATE DATABASE vacancies_db;
END IF;

-- удаляем таблицы, если есть
drop table if exists vacancies_db.public.vacancies;
drop table if exists vacancies_db.public.employers;

-- таблица работодателей
create table vacancies_db.public.employers (id int8 primary key,
					   name varchar(1000),
					   city varchar(100)
					  );

-- таблица вакансий
create table vacancies_db.public.vacancies (id int8 primary key,
                                            employer_id int8,
                                           name varchar(1000),
                                           job_url varchar(1000),
                                           requirement varchar(4000),
                                           salary_from int4,
                                           salary_to int4,
                                           CONSTRAINT fk_vacancies_employers FOREIGN KEY (employer_id)
                                            REFERENCES public.employers (id) MATCH SIMPLE
                                            ON UPDATE CASCADE
                                            ON DELETE CASCADE
                                          );
end $$
import requests
import json


class HeadHunter():
    def __init__(self, keyword):
        self.__params= {
            "text": keyword,
            "page": 0,
            "per_page":50
        }
        self.vacancies_url = 'https://api.hh.ru/vacancies'
        self.__vacancies_json = []
        self.vacancies = []
        self.employers = []

    def get_vacancies(self, page_count=1):
        page=self.__params["page"]
        while page < page_count:
            print(f"Страница {page+1}", end=": ")
            response = requests.get(self.vacancies_url, params=self.__params)
            vacancies_list = response.json()["items"]
            print(f"Найдено {len(vacancies_list)}")

            self.__vacancies_json.extend(vacancies_list)
            page +=1
            self.__params["page"] = page

        #print(json.dumps(vacancies_list, indent=2, ensure_ascii=False))
        self.get_vacancy_info()
        return

    def get_vacancy_info(self):
        vacancies = []
        employers = []
        for item in self.__vacancies_json:
            #берем вакансии только от работодателей с id, т.к. надо вставлять в базу и связывать их друг с другом
            if item["employer"].get("id") != None:
                employers.append({
                "employer_id": item["employer"].get("id"),
                "firm": item["employer"]["name"],
                "location": self.get_address(item["address"])
                })

                vacancies.append({
                    "job_id": item["id"],
                    "employer_id": item["employer"].get("id"),
                    "job_name": item['name'],
                    "job_url":  item['alternate_url'],
                    "requirement": item['snippet']["requirement"],
                    "salary_from": self.get_salary(item["salary"],'from'),
                    "salary_to": self.get_salary(item["salary"],"to"),
                })

        #удаляем дубликаты работодателей
        employers1=[]
        for i in employers:
            if i not in employers1:
                employers1.append(i)

        self.vacancies=vacancies
        self.employers=employers1

        return
    def get_salary(self, p_salary,from_to):
        salary  = None
        if p_salary != None:
           salary = p_salary[from_to]

        return salary

    def get_address(self,address):
        if address !=None:
            return address["city"]
        else:
            return None

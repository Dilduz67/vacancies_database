import requests
import json
import psycopg2


class HeadHunter():
    def __init__(self, keyword,selected: dict):
        self.__params= {
            "text": keyword,
            "page": 0,
            "per_page":50
                        }
        
        if len(selected) !=0:
            self.get_selected=True
        else:
            self.get_selected=False
        
        self.vacancies_url = 'https://api.hh.ru/vacancies'
        self.__vacancies_json = []
        self.vacancies = []
        self.employers = []
        self.selected = {}
        self.selected=selected
        
    def get_response(self,page_count):
        for page in range(0, page_count):
            response = requests.get(self.vacancies_url, params=self.__params)
            vacancies_list = response.json()["items"]
            
            self.__vacancies_json.extend(vacancies_list)
            
        print(f"Найдено {len(vacancies_list)} вакансий")
        
        return
       
    def get_vacancies(self, page_count=1):
        if self.get_selected==False:
            self.get_response(page_count)
        else:
            for id in self.selected:
                self.__params["employer_id"]=id
                self.get_response(page_count)

        #print(json.dumps(vacancies_list, indent=2, ensure_ascii=False))
        self.get_vacancy_info()
        
        return

    def get_vacancy_info(self):
        salary_from:int
        salary_to:int
        currency:str
        
        for item in self.__vacancies_json:
            #берем вакансии только от работодателей с id, т.к. надо вставлять в базу и связывать их друг с другом
            if item["employer"].get("id") != None:
                
                self.employers.append({
                "employer_id": item["employer"].get("id"),
                "firm": item["employer"]["name"],
                "location": self.get_address(item["address"])
                })
                
                if item["salary"] != None:
                    salary_from=item["salary"]['from']
                    salary_to=item["salary"]['to']
                    currency=item["salary"]['currency']
                else:
                    salary_from=None
                    salary_to=None
                    currency=None

                self.vacancies.append({
                    "job_id": item["id"],
                    "employer_id": item["employer"].get("id"),
                    "job_name": item['name'],
                    "job_url":  item['alternate_url'],
                    "requirement": item['snippet']["requirement"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency
                })

        #удаляем дубликаты работодателей и вакансий
        employers1=[]
        vacancies1=[]
        emp_dict = {}
        vac_dict = {}
        
        for i in self.employers:
            emp_dict[i['employer_id']] = i
        employers1 = list(emp_dict.values())

        for i in self.vacancies:
            vac_dict[i['job_id']] = i
            
        vacancies1 = list(vac_dict.values())
        
        self.employers=employers1        
        self.vacancies=vacancies1
        
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
        
        

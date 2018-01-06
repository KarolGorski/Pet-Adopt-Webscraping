# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

class Pet():

    def __init__(self, name=None, description=None):
        self.init_details(name, description)
        
    def init_details(self, name, description):
        
        #TODO: description -> details

        koncowki= {'Data urodzenia', 'Wielkość'.decode('utf8'),'Rasa:' , 'Płeć:'.decode('utf-8'), 'Rok urodzenia:','Data przyjęcia:'.decode('utf-8'),'Nr ewidencyjny:'}
         
        self.name = name.strip()

        self.breed = 'default breed'
        if description.find('Rasa:') != -1:
            min=1000000000
            start=description.find('Rasa:')+5
            for dne in koncowki:
                if len(description[ start : description.find(dne, start)].strip()) < min:
                    min=len(description[ start : description.find(dne, start)].strip())
                    end = description.find(dne, start)
                    self.breed = description[start: end].strip()



        self.sex = 'default sex'
        if description.find('Płeć:'.decode('utf-8')) != -1:
            min = 1000000000
            start=description.find('Płeć:'.decode('utf-8'))+5
            for dne in koncowki:
                if len(description[ start : description.find(dne, start)].strip()) < min:
                    min = len(description[start: description.find(dne, start)].strip())
                    end = description.find(dne, start)
                    self.sex = description[start: end].strip()

        self.size = 'default size'
        if description.find('Wielkość:'.decode('utf-8')) != -1:
            min = 1000000000
            start = description.find('Wielkość:'.decode('utf-8')) + 9
            for dne in koncowki:
                if len(description[start: description.find(dne, start)].strip()) < min:
                    min = len(description[start: description.find(dne, start)].strip())
                    end = description.find(dne, start)
                    self.size = description[start: end].strip()

        self.date_of_birth = 'default date of birth'
        if description.find('urodzenia:') != -1:
            min = 1000000000
            start=description.find('urodzenia:')+10
            for dne in koncowki:
                if len(description[ start : description.find(dne, start)].strip()) < min:
                    min = len(description[start: description.find(dne, start)].strip())
                    end = description.find(dne, start)
                    self.date_of_birth = description[start: end].strip()

        self.accepted_on = 'default accepted on'
        if description.find('Data przyjęcia:'.decode('utf-8')) != -1:
            min = 1000000000
            start=description.find('Data przyjęcia:'.decode('utf-8'))+15
            for dne in koncowki:
                if len(description[ start : description.find(dne, start)].strip()) < min:
                    min = len(description[start: description.find(dne, start)].strip())
                    end = description.find(dne, start)
                    self.accepted_on = description[start: end].strip()


        self.pet_id = 'default pet id'
        if description.find('Nr ewidencyjny:') != -1:
            min = 1000000000
            start=description.find('Nr ewidencyjny:')+15
            for dne in koncowki:
                if len(description[ start : description.find(dne, start)].strip()) < min:
                    min = len(description[start: description.find(dne, start)].strip())
                    end = description.find(dne, start)
                    self.pet_id = description[start: end].strip()

        
    def serialize(self):
        return self.__dict__
               
class Extraction():

    def go_to(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = r.text
        return BeautifulSoup(data, "html.parser")
        
    def extract(self,url):

        petsToReturn = list()

        url_base='http://'+url if not url[:4].lower() == 'http' else url
        url = url_base
        
        soup = self.go_to(url)
        
        #KOTY
        li = soup.find('li', class_='item17')
        url = url_base+li.find('a')['href']

        soup = self.go_to(url)

        cats = list()




        for name in soup.find_all('td', class_='djcat_product'):
            description = name.parent.find('td', class_='djcat_intro')

            if 'Nazwa' in name.getText() and 'Opis' in description.getText():
                continue

            cats.append(
                Pet(
                    name.getText().replace("\n",""),
                    description.getText()
                    )
                    .serialize()
                )

        petsToReturn.append(cats)

        soup = self.go_to(url_base);

        li = soup.find('li', class_='item7')
        url = url_base + li.find('a')['href']

        soup = self.go_to(url)
        dogs = list()

        for name in soup.find_all('td', class_='djcat_product'):
            description = name.parent.find('td', class_='djcat_intro')

            if 'Nazwa' in name.getText() and 'Opis' in description.getText():
                continue

            dogs.append(
                Pet(
                    name.getText().replace("\n", ""),
                    description.getText()
                )
                    .serialize()
            )


        petsToReturn.append(dogs)


        return petsToReturn

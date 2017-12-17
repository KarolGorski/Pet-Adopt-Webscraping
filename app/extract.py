# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv
import re

class Pet():

    def __init__(self, name=None, description=None):
        self.init_details(description)
        
    def init_details(self, description):
        
        #TODO: description -> details
         
        self.name = 'some name'
        self.breed = 'some breed'
        self.sex = 'some sex'
        self.date_of_birth = 'some date of birth'
        self.accepted_on = 'some accepted on'
        self.pet_id = 'some pet id'
        
    def serialize(self):
        return self.__dict__
               
class Extraction():

    def go_to(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = r.text
        return BeautifulSoup(data, "html.parser")
        
    def extract(self,url):
        url_base='http://'+url if not url[:4].lower() == 'http' else url
        url = url_base
        
        soup = self.go_to(url)
        
        
        li = soup.find('li', class_='item17')
        url = url_base+li.find('a')['href']
        
        soup = self.go_to(url)
        
        pets = list()
        for name in soup.find_all('td', class_='djcat_product'):
            description = name.parent.find('td', class_='djcat_intro')
            
            if 'Nazwa' in name.getText() and 'Opis' in description.getText():
                continue                
              
            pets.append(
                Pet(
                    name.getText(),
                    description.getText()
                    )
                    .serialize()
            )
        return pets

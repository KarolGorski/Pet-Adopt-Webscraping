# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


class Pet():
    def __init__(self, name=None, all_info_about_pet=None):
        self.name = 'default name'
        self.dateOfBirth = 'default date of birth'
        self.dateOfArrival = 'default date of arrival in shelter'
        self.species = 'default species'
        self.breed = 'default breed'
        self.size = 'default size'
        self.shelter = 'default shelter'
        self.description = 'default description'

        self.init_details(name, all_info_about_pet)

    def init_details(self, name, all_info_about_pet):
        self.name = name.strip()

        endings = {'Data urodzenia',
                   'Wielkość',
                   'Rasa:',
                   'Płeć:',
                   'Rok urodzenia:',
                   'Data przyjęcia:',
                   'Nr ewidencyjny:'}

        attributes = {
            'breed': 'Rasa:',
            'sex': 'Płeć:',
            'size': 'Wielkość:',
            'dateOfBirth': 'urodzenia:',
            'dateOfArrival': 'Data przyjęcia:'
        }

        for english_word, polish_word in attributes.items():
            if all_info_about_pet.find(polish_word) != -1:
                min = 1000000000
                start = all_info_about_pet.find(polish_word) + len(polish_word)
                for dne in endings:
                    if len(all_info_about_pet[start: all_info_about_pet.find(dne, start)].strip()) < min:
                        min = len(all_info_about_pet[start: all_info_about_pet.find(dne, start)].strip())
                        end = all_info_about_pet.find(dne, start)
                        self.__dict__[english_word] = all_info_about_pet[start: end].strip()

    def serialize(self):
        return self.__dict__


class Extraction():
    def go_to(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = r.text
        return BeautifulSoup(data, "html.parser")

    def extract(self, url):

        petsToReturn = list()

        url_base = 'http://' + url if not url[:4].lower() == 'http' else url
        url = url_base

        soup = self.go_to(url)

        # KOTY
        li = soup.find('li', class_='item17')
        url = url_base + li.find('a')['href']

        soup = self.go_to(url)

        cats = list()

        for name in soup.find_all('td', class_='djcat_product'):
            all_info_about_pet = name.parent.find('td', class_='djcat_intro')

            if 'Nazwa' in name.getText() and 'Opis' in all_info_about_pet.getText():
                continue

            cats.append(
                Pet(
                    name.getText().replace("\n", ""),
                    all_info_about_pet.getText()
                )
                    .serialize()
            )

        petsToReturn.append(cats)

        # PSY
        soup = self.go_to(url_base);

        li = soup.find('li', class_='item7')
        url = url_base + li.find('a')['href']

        soup = self.go_to(url)
        dogs = list()

        for name in soup.find_all('td', class_='djcat_product'):
            all_info_about_pet = name.parent.find('td', class_='djcat_intro')

            if 'Nazwa' in name.getText() and 'Opis' in all_info_about_pet.getText():
                continue

            dogs.append(
                Pet(
                    name.getText().replace("\n", ""),
                    all_info_about_pet.getText()
                )
                    .serialize()
            )

        petsToReturn.append(dogs)

        return petsToReturn

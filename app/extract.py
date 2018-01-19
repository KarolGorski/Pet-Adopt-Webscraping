# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


class Pet():
    def __init__(self, name, all_info_about_pet, species, shelter, picture_url, description):
        self.name = 'default name'
        self.dateOfBirth = 'default date of birth'
        self.dateOfArrival = 'default date of arrival in shelter'
        self.species = species
        self.breed = 'default breed'
        self.size = ''
        self.shelter = shelter
        self.description = description
        self.pictureUrl = picture_url

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

        catsAndDogs = {'kot': 'item17', 'pies': 'item7'}

        for catOrDog, css_class in catsAndDogs.items():

            li = soup.find('li', class_=css_class)
            url = url_base + li.find('a')['href']

            # open cats/dogs page
            soup = self.go_to(url)

            pets = list()

            for name in soup.find_all('td', class_='djcat_product'):
                all_info_about_pet = name.parent.find('td', class_='djcat_intro')
                if 'Nazwa' in name.getText() and 'Opis' in all_info_about_pet.getText():
                    continue

                picture_box = name.parent.find('td', class_='djcat_picture')
                picture_url = picture_box.find('a')['href']

                site2 = self.go_to(url_base + name.find('a')['href'])
                description = site2.find('div', class_='article-inside').getText().strip()

                pets.append(
                    Pet(
                        name.getText().replace("\n", ""),
                        all_info_about_pet.getText(),
                        catOrDog,
                        'schronisko-zwierzaki.lublin.pl',
                        picture_url,
                        description
                    )
                        .serialize()
                )

        petsToReturn.append(pets)

        return petsToReturn

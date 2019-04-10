from app.extract import Extraction
from pony.orm import *


def sendToDB(pets):
    db = Database()

    class Pet(db.Entity):
        name = Required(str, max_len=1000)
        date_of_birth = Required(str, max_len=1000)
        age = Required(int)
        date_of_arrival = Required(str, max_len=1000)
        species = Required(str, max_len=1000)
        sex = Required(str, max_len=1000)
        sterilized = Required(bool)
        breed = Required(str, max_len=1000)
        size = Optional(str, max_len=1000)
        shelterID = Required(int) #hardcoded
        description = Required(str, max_len=1500)
        picture_url = Required(str, max_len=1000)
        page_url = Required(str, max_len=1000)

    #db.bind(provider='sqlite', filename=':memory:')

    # MySQL
    db.bind(provider='mysql', host='XXX', user='XXX', passwd='XXX', db='XXX')

    db.drop_table('pet', with_all_data=True, if_exists=True)

    db.generate_mapping(create_tables=True)

    set_sql_debug(True)

    with db_session:
        for dogsOrCats in pets:
            for pet in dogsOrCats:
                print(pet)

                Pet(name=pet['name'],
                    date_of_birth=pet['dateOfBirth'],
                    age=pet['age'],
                    date_of_arrival=pet['dateOfArrival'],
                    species=pet['species'],
                    sex=pet['sex'],
                    sterilized=pet['sterilized'],
                    breed=pet['breed'],
                    size=pet['size'],
                    shelterID=pet['shelterID'],
                    description=pet['description'],
                    page_url=pet['page_url'],
                    picture_url=pet['pictureUrl'])


class DbUpload():
    def run(self):
        extraction = Extraction()
        pets = extraction.extract("http://www.schronisko-zwierzaki.lublin.pl")
        sendToDB(pets)

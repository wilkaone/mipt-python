from person import Person
from family import Family
from city import City

class Aglomiration:
    def __init__(self, name, max_count_residents):
        self.__name = name
        self.__max_count_residents = max_count_residents
        self.__current_count_residents = 0
        self.__residents = list()
        self.__families = list()
        self.__cities = list()

    def add_person(self, name, surname, midname, city_name):
        for city in self.__cities:
            if city_name == city.get_name():
                person = Person(name, surname, midname, city_name)
                city.add_person(name, surname, midname)
                self.__residents.append(person)
                self.__current_count_residents += 1
                break

    def remove_person(self, name, surname, midname, city_name):
        for city in self.__cities:
            if city.get_name() != city_name:
                continue
            for resident in self.__residents:
                if resident.get_city() != city_name:
                    continue
                if resident.get_name() == name and resident.get_surname() == surname and resident.get_midname() == midname:
                    self.__residents.remove(resident)
                    city.remove_person(name, surname, midname)
                    break

    def add_family(self, name, husband, wife, city_name=''):
        husband_ = None
        wife_ = None
        for resident in self.__residents:
            if husband == resident.__str__():
                husband_ = resident
            elif wife == resident.__str__():
                wife_ = resident
        if husband_ != None and wife_ != None:
            self.__families.append(Family(name, husband_, wife_))

    def add_children(self, family_name, children):
        for family in self.__families:
            if family.get_name() == family_name:
                family.add_children(children)

    def add_city(self, name, count):
        if (self.__current_count_residents + count) < self.__max_count_residents:
            self.__cities.append(City(name, count))

    def get_cities(self):
        return self.__cities
    
    def get_families(self):
        return self.__families

    def __del__(self):
        pass
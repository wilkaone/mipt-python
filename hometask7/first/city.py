from person import Person

class City:
    def __init__(self, name, max_count_residents):
        self.__name = name
        self.__max_count_residents = max_count_residents
        self.__current_count_residents = 0
        self.__residents = list()
    
    def get_name(self):
        return self.__name
    
    def get_max_count_person(self):
        return self.__max_count_residents
    
    def get_current_count_person(self):
        return self.__current_count_residents
    
    def add_person(self, name, surname, midname):
        if self.__current_count_residents >= self.__max_count_residents:
            raise ValueError("[CITY ERROR]: current_count_residents >= max_count_residents (reason: add_person() ).")

        if self.__current_count_residents < self.__max_count_residents:
            self.__residents.append(Person(name, surname, midname, self.get_name()))
            self.__current_count_residents += 1

    def remove_person(self, name, surname, midname):
        for resident in self.__residents:
            if resident.get_name() == name and resident.get_surname() == surname and resident.get_midname() == midname:
                self.__residents.remove(resident)
                self.__current_count_residents -= 1
                return
        raise ValueError("[CITY ERROR]: Not found person (reason: remove_person())")
    
    def __str__(self):
        str_city = f"Name: {self.__name}\n"
        str_city += f"Count resident: {self.__current_count_residents}\n"
        str_city += "Residents:\n"
        for resident in self.__residents:
            str_city += f"{resident.get_name()} {resident.get_surname()} {resident.get_midname()}\n"
        return str_city

    def __del__(self):
        pass
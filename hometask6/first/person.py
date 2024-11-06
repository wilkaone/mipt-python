class Person:
    def __init__(self, name, surname, midname, city):
        self.__name = name
        self.__surname = surname
        self.__midname = midname
        self.__city = city

    def get_person(self):
        return list(self.__name, self.__surname, self.__midname)
    
    def get_name(self):
        return self.__name
    
    def get_surname(self):
        return self.__surname
    
    def get_midname(self):
        return self.__midname
    
    def get_city(self):
        return self.__city

    def __str__(self):
        return f"{self.__name} {self.__surname} {self.__midname}"
  
    def __del__(self):
        pass
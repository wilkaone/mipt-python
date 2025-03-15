class Family:
    def __init__(self, name, husband, wife):
        self.__name = name
        self.__husband = husband
        self.__wife = wife
        self.__childrens = list()
    def get_name(self):
        return self.__name
    def add_children(self, children):
        self.__childrens.append(children)
    def __del__(self):
        pass
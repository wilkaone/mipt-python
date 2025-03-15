from aglomiration import Aglomiration
from person import Person

if __name__ == "__main__":
    aglomiration = Aglomiration("Aglomiration", 100)

    aglomiration.add_city("City1", 25) # 25 in aglomiration
    aglomiration.add_city("City2", 50) # 75 in aglomiration

    aglomiration.add_person("Name1", "Surname1", "Midname1", "City1")
    aglomiration.add_person("Name2", "Surname2", "Midname2", "City1")
    aglomiration.add_person("Name3", "Surname3", "Midname3", "City1")

    aglomiration.add_person("Name4", "Surname4", "Midname4", "City2")
    aglomiration.add_person("Name5", "Surname5", "Midname5", "City2")

    print("Info Aglomiration:")
    for city in aglomiration.get_cities():
        print(str(city))

    aglomiration.add_family("FamilyName1", "Name1 Surname1 Midname1", "Name2 Surname2 Midname2")
    aglomiration.add_children("FamilyName1", Person("Name6", "Surname6", "Midname6", "City1"))

    print("Info Families in Aglomiration:")
    for family in aglomiration.get_families():
        print(f"{family.get_name()}")

    
from pymongo import MongoClient

uri = "mongodb://localhost:27017/"

client = MongoClient(uri)


database = client['users']

def import_data():
    print("Enter Databse Url ie localhost:27017")
    url = input("Url")

    print("Enter Databse name")
    data_b = input("Database Name")

    print("Enter Name Of Collection")
    coll = input("Collection Name")

    client = MongoClient(url)
    database = client['data_b']
    collec = database['coll']


    print("Enter File Name To Read Including the Extension")
    file = input("File Name >> ")

    read_dd = open(file, 'r')
    collec.insert({read_dd})






def export():
    print("Enter Databse Url  ")
    url = input("Url  ")

    print("Enter Databse name  ")
    data_b = input("Database Name  ")

    print("Enter Name Of Collection  ")
    coll = input("Collection Name  ")

    print("Enter Output File Name Without Extension  ")
    name = input("Name Of Output File  ")

    name2 = name + ".txt"
    client = MongoClient(url)
    database = client['data_b']
    collec = database['coll']

    data_found = collec.find({})
    for x in data_found:
        print(x)
        with open(name2 , "w") as file_opend:
            file_opend.write(x)
    print("Done If All Input Was Right")


print("""
Please Choose Your Action
[1] Import Data
[2] Export Data
""")

option = input("Option  ")

if option == "1":
    import_data()
if option == "2":
    export()
else:
    print("Wrong Option run Script Again")

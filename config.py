import pymongo
import certifi

con_str = "mongodb+srv://lrobinson:work1234@cluster0.syy3pt3.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("fequipment")

me = {
    "frist_name": "Chaka",
    "last_name": "Robinson",
    "age": "23",

}


def hello():
    print("Hello there!")

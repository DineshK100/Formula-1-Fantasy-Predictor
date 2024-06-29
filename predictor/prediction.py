import pandas as pd
from pymongo import MongoClient
import certifi

#Gets data ready by pulling that specific race data from the database
def loadDataBaseData(raceName) :
    client = MongoClient(
        'mongodb+srv://dineshrkarnati:Collegeadmissio@formulafantasy.v9quue6.mongodb.net/?retryWrites=true&w=majority',
        tlsCAFile=certifi.where()
    )
    db = client['formula']
    collection = db[raceName]

    data = pd.DataFrame(list(collection.find()))

    data['Pos'] = data['Pos'].astype(int)
    data['Points'] = data['Points'].astype(int)
    data = pd.get_dummies(data, columns=['Driver', 'Constructor'])

    return data


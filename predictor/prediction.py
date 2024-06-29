import pandas as pd
from pymongo import MongoClient
import certifi
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import classification_report


#Gets data ready by pulling that specific race data from the database
def loadDataBaseData(raceName):
    client = MongoClient(
        'mongodb+srv://dineshrkarnati:Collegeadmissio@formulafantasy.v9quue6.mongodb.net/?retryWrites=true&w=majority',
        tlsCAFile=certifi.where()
    )
    db = client['formula']
    collection = db[raceName]

    data = pd.DataFrame(list(collection.find()))

    # Handle non-integer and empty string values in 'Pos.' column
    data = data[data['Pos.'].apply(lambda x: x.isdigit() and x != '')]
    data['Pos.'] = data['Pos.'].astype(int)

    # Replace empty strings in 'Points' column with 0 and convert to integer
    data['Points'] = data['Points'].replace('', '0').astype(int)

    # Convert ordinal strings in 'Grid' column to numeric values in one line
    data['Grid'] = data['Grid'].apply(lambda x: int(x.rstrip('stndrdth')) if x.rstrip('stndrdth').isdigit() else None)
    data = data.dropna(subset=['Grid'])  # Drop rows where 'Grid' conversion failed
    data['Grid'] = data['Grid'].astype(int)

    data = pd.get_dummies(data, columns=['Driver', 'Constructor'])

    return data

def selectFeatures(data):

    features = ['Grid', 'Laps', 'Points'] + [col for col in data.columns if 'Driver_' in col or 'Constructor_' in col]
    X = data[features]
    #The important feature set for the prediction variable (like here name, constructor, etc)
    X = data[features]
    #What we want to predict i.e here what position each driver will land
    y = data['Pos.']

    return X,y

def trainModel(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    #Finally making predictions
    prediction = model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, prediction)
    print("Accuracy report : ", accuracy)

    #Maybe include classification report

    return model, X_train, y_train

def main():
    race_name = 'abu dhabi_grand_prix'
    data = loadDataBaseData(race_name)
    X, y = selectFeatures(data)
    model, X_train, y_train = trainModel(X, y)

if __name__ == "__main__":
    main() 
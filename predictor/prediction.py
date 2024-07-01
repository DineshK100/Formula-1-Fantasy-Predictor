import pandas as pd
from pymongo import MongoClient
import certifi
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb

# Gets data ready by pulling that specific race data from the database
def loadDataBaseData(raceName):
    client = MongoClient(
        'mongodb+srv://dineshrkarnati:Collegeadmissio@formulafantasy.v9quue6.mongodb.net/?retryWrites=true&w=majority',
        tlsCAFile=certifi.where()
    )
    db = client['formula']
    collection = db[raceName]

    data = pd.DataFrame(list(collection.find()))

    retired_drivers = ['Nigel Mansell', 'Alain Prost', 'Ayrton Senna', 'Gerhard Berger', 'Riccardo Patrese', 'Jean Alesi', 'Mika Häkkinen', 'Damon Hill', 'Johnny Herbert', 'Eddie Irvine', 'Michael Schumacher', 'David Coulthard', 'Rubens Barrichello', 'Felipe Massa', 'Jenson Button', 'Mark Webber', 'Nico Rosberg', 'Kimi Räikkönen', 'Sebastian Vettel', 'Romain Grosjean', 'Robert Kubica', 'Daniil Kvyat', 'Heikki Kovalainen', 'Pastor Maldonado', 'Bruno Senna', 'Paul di Resta', 'Marcus Ericsson', 'Pascal Wehrlein', 'Stoffel Vandoorne', 'Sergey Sirotkin', 'Esteban Gutierrez', 'Jolyon Palmer', 'Felipe Nasr', 'Kamui Kobayashi', 'Vitaly Petrov', 'Narain Karthikeyan', 'Karun Chandhok', 'Timo Glock', 'Nick Heidfeld', 'Jarno Trulli', 'Pedro de la Rosa', 'Vitantonio Liuzzi', 'Adrian Sutil', 'Jaime Alguersuari']

    data = data[~data['Driver'].isin(retired_drivers)]

    # Handle non-integer and empty string values in 'Pos.' column
    data = data[data['Pos.'].apply(lambda x: x.isdigit() and x != '')]
    data['Pos.'] = data['Pos.'].astype(int)

    # Replace empty strings in 'Points' column with 0 and convert to integer
    data['Points'] = data['Points'].replace('', '0').astype(int)

    # Convert ordinal strings in 'Grid' column to numeric values in one line
    data['Grid'] = data['Grid'].apply(lambda x: int(x.rstrip('stndrdth')) if x.rstrip('stndrdth').isdigit() else None)
    data = data.dropna(subset=['Grid'])  # Drop rows where 'Grid' conversion failed
    data['Grid'] = data['Grid'].astype(int)

    # Convert 'Laps' to integer
    data['Laps'] = data['Laps'].apply(lambda x: int(x) if x.isdigit() else None)
    data = data.dropna(subset=['Laps'])
    data['Laps'] = data['Laps'].astype(int)

    data = pd.get_dummies(data, columns=['Driver', 'Constructor'])

    return data

def selectFeatures(data):
    features = ['Grid', 'Laps', 'Points'] + [col for col in data.columns if 'Driver_' in col or 'Constructor_' in col]
    X = data[features]
    y = data['Pos.']
    return X, y

def trainModel(X, y):
    # Encode target variable
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.1, random_state=10)

    # Initialize the XGBoost model
    model = xgb.XGBClassifier(random_state=42, use_label_encoder=False)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Calculate and print the accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of XGBoost Model:", accuracy)

    return model
    

def main():
    race_name = 'austrian_grand_prix'
    data = loadDataBaseData(race_name)
    X, y = selectFeatures(data)
    model = trainModel(X, y)


if __name__ == "__main__":
    main()

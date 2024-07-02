import pandas as pd
from pymongo import MongoClient
import certifi
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb
from math import ceil

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

    data = data[data['Pos.'].apply(lambda x: x.isdigit() and x != '')]
    data['Pos.'] = data['Pos.'].astype(int)

    data['Points'] = data['Points'].replace('', '0').astype(float).apply(lambda x: ceil(x)).astype(int)

    data['Grid'] = data['Grid'].apply(lambda x: int(x.rstrip('stndrdth')) if isinstance(x, str) and x.rstrip('stndrdth').isdigit() else pd.NA)
    data = data.dropna(subset=['Grid'])
    data['Grid'] = data['Grid'].astype(int)

    data['Laps'] = data['Laps'].apply(lambda x: int(x) if x.isdigit() else None)
    data = data.dropna(subset=['Laps'])
    data['Laps'] = data['Laps'].astype(int)

    drivers = data['Driver']
    constructors = data['Constructor']

    data = pd.get_dummies(data, columns=['Driver', 'Constructor'])

    return data, drivers, constructors

def selectFeatures(data):
    features = ['Grid', 'Laps', 'Points'] + [col for col in data.columns if 'Driver_' in col or 'Constructor_' in col]
    X = data[features]
    y = data['Pos.']
    return X, y

def calculateSampleWeights(data):
    current_year = data['Year'].max()
    data['Weight'] = 1 / (current_year - data['Year'] + 1)
    return data['Weight']

def trainModel(X, y, sample_weights):
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)


    X_train, X_test, y_train, y_test, sample_weights_train, sample_weights_test = train_test_split(
        X, y_encoded, sample_weights, test_size=0.1, random_state=42
    )

    model = xgb.XGBClassifier(random_state=42, use_label_encoder=False)

    param_grid = {
        'n_estimators': [100],
        'max_depth': [3],
        'learning_rate': [0.1],
        'subsample': [0.8],
        'colsample_bytree': [0.8]
    }

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train, sample_weight=sample_weights_train)

    best_model = grid_search.best_estimator_

    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of XGBoost Model:", accuracy)

    return best_model, label_encoder

def predictPodium(best_model, label_encoder, new_data, original_drivers, original_constructors):
    new_predictions = best_model.predict(new_data)
    new_data['Predicted_Position'] = new_predictions
    new_data['Predicted_Position'] = label_encoder.inverse_transform(new_data['Predicted_Position'])
    new_data['Driver'] = original_drivers.head(len(new_data)).values
    new_data['Constructor'] = original_constructors.head(len(new_data)).values
    top_3_winners = new_data.sort_values(by='Predicted_Position').head(3)
    print(top_3_winners[['Driver', 'Constructor', 'Grid', 'Laps', 'Points', 'Predicted_Position']])

def main():
    race_name = 'qatar_grand_prix'
    data, drivers, constructors = loadDataBaseData(race_name)
    sample_weights = calculateSampleWeights(data)
    X, y = selectFeatures(data)
    model, label_encoder = trainModel(X, y, sample_weights)

    new_data = pd.DataFrame({
        'Grid': [1, 2, 3],
        'Laps': [71, 71, 71],
        'Points': [26, 18, 15]
    })

    # Saudi = 3, Miami = 2 , emilia romagna = 3, dutch = 3, las vegas = 1, qatar = 2
    
    dummy_columns = {col: [0, 0, 0] for col in X.columns if col not in new_data.columns}
    dummy_df = pd.DataFrame(dummy_columns)

    new_data = pd.concat([new_data, dummy_df], axis=1)

    predictPodium(model, label_encoder, new_data, drivers, constructors)

if __name__ == "__main__":
    main()
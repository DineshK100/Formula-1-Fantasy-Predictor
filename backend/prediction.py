# # Saudi = 3, Miami = 2 , emilia romagna = 3, dutch = 3, las vegas = 1, qatar = 2, azerbaijan, usa
# # Optimize fantasy pics to make more use of the budget more price = more valuab
# # Make it so that the fantasy prices are pulled from the website so the user doesnt enter them
# # CV should equal lenght of dataframe/# of racers
# # Maybe instead of getting rid of the DNF give them 20
# # Get rid of redundancy if 

import pandas as pd
import numpy as np
from pymongo import MongoClient
import certifi
from sklearn.model_selection import train_test_split, GridSearchCV
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

    data['Driver'] = drivers
    data['Constructor'] = constructors

    return data, drivers, constructors

def selectFeatures(data):
    data['Grid_Laps'] = data['Grid'] * data['Laps']
    data['Grid_Points'] = data['Grid'] * data['Points']
    
    features = ['Grid', 'Laps', 'Points', 'Grid_Laps', 'Grid_Points'] + [col for col in data.columns if 'Driver_' in col or 'Constructor_' in col]
    X = data[features]
    y = data['Pos.']
    
    unique_positions = np.unique(y)
    for pos in range(1, 21):
        if pos not in unique_positions:
            X = X.append(pd.Series(), ignore_index=True)
            y = y.append(pd.Series(pos), ignore_index=True)
    
    return X, y

def handle_rare_classes(y):
    counts = y.value_counts()
    rare_classes = counts[counts < 2].index
    for rare_class in rare_classes:
        y = y.replace(rare_class, rare_class - 1)
    return y

def calculateSampleWeights(data):
    current_year = data['Year'].max()
    
    data['Weight'] = 1 / (current_year - data['Year'] + 1)
    data['Year_Weight'] = data['Year'].apply(lambda x: 1.5 if current_year - x <= 2 else 1)
    data['Grid_Weight'] = data['Grid'].apply(lambda x: 2 if x <= 5 else 1.5)
    data['Weight'] *= data['Year_Weight'] * data['Grid_Weight']
    
    return data['Weight']

def trainModel(X, y, sample_weights):
    y = handle_rare_classes(y)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print("Unique values in y before encoding:", y.unique())
    print("Unique values in y after encoding:", np.unique(y_encoded))

    X['Grid'] *= 5

    X_train, X_test, y_train, y_test, sample_weights_train, sample_weights_test = train_test_split(
        X, y_encoded, sample_weights, test_size=0.1, random_state=42
    )

    model = xgb.XGBClassifier(random_state=42)

    param_grid = {
        'n_estimators': [100],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8,  1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', n_jobs=-1, cv=5, error_score='raise')
    grid_search.fit(X_train, y_train, sample_weight=sample_weights_train)

    best_model = grid_search.best_estimator_

    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of XGBoost Model:", accuracy)

    return best_model, label_encoder

def predictTop20(best_model, label_encoder, new_data, original_drivers, original_constructors, allowed_drivers):
    new_predictions = best_model.predict(new_data)
    new_data['Predicted_Position'] = new_predictions
    new_data['Driver'] = original_drivers.head(len(new_data)).values
    new_data['Constructor'] = original_constructors.head(len(new_data)).values

    new_data = new_data[new_data['Driver'].isin(allowed_drivers)]

    new_data = new_data.sort_values(by='Predicted_Position').drop_duplicates(subset=['Driver'])

    new_data['Predicted_Position'] = range(1, len(new_data) + 1)

    driver_constructor_mapping = {
        '#1 Max Verstappen': 'Red Bull',
        '#4 Lando Norris': 'McLaren',
        '#16 Charles Leclerc': 'Ferrari',
        '#55 Carlos Sainz Jr.': 'Ferrari',
        '#11 Sergio Pérez': 'Red Bull',
        '#81 Oscar Piastri': 'McLaren',
        '#63 George Russell': 'Mercedes',
        '#44 Lewis Hamilton': 'Mercedes',
        '#14 Fernando Alonso': 'Aston Martin',
        '#22 Yuki Tsunoda': 'AlphaTauri',
        '#10 Pierre Gasly': 'Alpine',
        '#31 Esteban Ocon': 'Alpine',
        '#77 Valtteri Bottas': 'Alfa Romeo',
        '#24 Guanyu Zhou': 'Alfa Romeo',
        '#27 Nico Hülkenberg': 'Haas',
        '#20 Kevin Magnussen': 'Haas',
        '#23 Alexander Albon': 'Williams',
        '#2 Logan Sargeant': 'Williams',
        '#18 Lance Stroll': 'Aston Martin',
        '#3 Daniel Ricciardo': 'McLaren'
    }

    missing_drivers = [driver for driver in allowed_drivers if driver not in new_data['Driver'].values]
    for i, driver in enumerate(missing_drivers):
        new_row = pd.DataFrame({
            'Grid': [0], 'Laps': [0], 'Points': [0], 
            'Predicted_Position': [len(new_data) + 1 + i], 
            'Driver': [driver], 'Constructor': [driver_constructor_mapping[driver]]
        })
        new_data = pd.concat([new_data, new_row], ignore_index=True)

    new_data['Predicted_Position'] = range(1, len(new_data) + 1)

    print(new_data[['Driver', 'Constructor', 'Grid', 'Laps', 'Points', 'Predicted_Position']])
    return new_data

def main(race):
    
    race_name = race
    allowed_drivers = [
        '#1 Max Verstappen', '#4 Lando Norris', '#16 Charles Leclerc', 
        '#55 Carlos Sainz Jr.', '#11 Sergio Pérez', '#81 Oscar Piastri', 
        '#63 George Russell', '#44 Lewis Hamilton', '#14 Fernando Alonso', 
        '#22 Yuki Tsunoda', '#10 Pierre Gasly', '#31 Esteban Ocon', 
        '#77 Valtteri Bottas', '#24 Guanyu Zhou', '#27 Nico Hülkenberg', 
        '#20 Kevin Magnussen', '#23 Alexander Albon', '#2 Logan Sargeant', 
        '#18 Lance Stroll', '#3 Daniel Ricciardo'
    ]

    data, drivers, constructors = loadDataBaseData(race_name)
    sample_weights = calculateSampleWeights(data)
    X, y = selectFeatures(data)

    print("Unique values in y:", y.unique())


    model, label_encoder = trainModel(X, y, sample_weights)

    new_data = pd.DataFrame({
        'Grid': [i for i in range(1, 21)],
        'Laps': [71 for _ in range(20)],
        'Points': [26 - i for i in range(20)]
    })

    dummy_columns = {col: [0] * 20 for col in X.columns if col not in new_data.columns}
    dummy_df = pd.DataFrame(dummy_columns)

    new_data = pd.concat([new_data, dummy_df], axis=1)

    result_data = predictTop20(model, label_encoder, new_data, drivers, constructors, allowed_drivers)
    return result_data[['Driver', 'Constructor', 'Grid', 'Laps', 'Points', 'Predicted_Position']].to_dict(orient='records')
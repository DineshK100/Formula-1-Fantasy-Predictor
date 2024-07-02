import pandas as pd
from pymongo import MongoClient
import certifi
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb

def loadDataBaseData(raceName):

    # Connects to MongoDB server
    client = MongoClient(
        'mongodb+srv://dineshrkarnati:Collegeadmissio@formulafantasy.v9quue6.mongodb.net/?retryWrites=true&w=majority',
        tlsCAFile=certifi.where()
    )

    db = client['formula']
    collection = db[raceName]

    data = pd.DataFrame(list(collection.find()))

    # list of retired f1 drivers (not comprehensive) I found online
    retired_drivers = ['Nigel Mansell', 'Alain Prost', 'Ayrton Senna', 'Gerhard Berger', 'Riccardo Patrese', 'Jean Alesi', 'Mika Häkkinen', 'Damon Hill', 'Johnny Herbert', 'Eddie Irvine', 'Michael Schumacher', 'David Coulthard', 'Rubens Barrichello', 'Felipe Massa', 'Jenson Button', 'Mark Webber', 'Nico Rosberg', 'Kimi Räikkönen', 'Sebastian Vettel', 'Romain Grosjean', 'Robert Kubica', 'Daniil Kvyat', 'Heikki Kovalainen', 'Pastor Maldonado', 'Bruno Senna', 'Paul di Resta', 'Marcus Ericsson', 'Pascal Wehrlein', 'Stoffel Vandoorne', 'Sergey Sirotkin', 'Esteban Gutierrez', 'Jolyon Palmer', 'Felipe Nasr', 'Kamui Kobayashi', 'Vitaly Petrov', 'Narain Karthikeyan', 'Karun Chandhok', 'Timo Glock', 'Nick Heidfeld', 'Jarno Trulli', 'Pedro de la Rosa', 'Vitantonio Liuzzi', 'Adrian Sutil', 'Jaime Alguersuari']

    # ignores data of older drivers as we only want to predict for active ones
    data = data[~data['Driver'].isin(retired_drivers)]
    # Makes sure all positions are digits
    data = data[data['Pos.'].apply(lambda x: x.isdigit() and x != '')]
    data['Pos.'] = data['Pos.'].astype(int)
    # If someone doesnt have points (places outside of 10th place) they are allocated
    # 0 points
    data['Points'] = data['Points'].replace('', '0').astype(int)
    # Converts grid data from things like 1st, 2nd etc to 1, 2 etc
    data['Grid'] = data['Grid'].apply(lambda x: int(x.rstrip('stndrdth')) if isinstance(x, str) and x.rstrip('stndrdth').isdigit() else None)
    data = data.dropna(subset=['Grid'])
    data['Grid'] = data['Grid'].astype(int)

    data['Laps'] = data['Laps'].apply(lambda x: int(x) if x.isdigit() else None)
    data = data.dropna(subset=['Laps'])
    data['Laps'] = data['Laps'].astype(int)

    drivers = data['Driver']
    constructors = data['Constructor']

    #Converts categorical data into numerical
    data = pd.get_dummies(data, columns=['Driver', 'Constructor'])

    return data, drivers, constructors

def selectFeatures(data):

    features = ['Grid', 'Laps', 'Points'] + [col for col in data.columns if 'Driver_' in col or 'Constructor_' in col]
    # What is being used to predict
    X = data[features] 
    # What we are trying to predict
    y = data['Pos.']
    return X, y

def calculateSampleWeights(data):
    current_year = data['Year'].max()
    # Algorithm to give weights to the data so more recent data is given more
    # emphasis
    data['Weight'] = 1 / (current_year - data['Year'] + 1)
    return data['Weight']


def trainModel(X, y, sample_weights):

    #Converts categorical data into numerical
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)


    X_train, X_test, y_train, y_test, sample_weights_train, sample_weights_test = train_test_split(
        X, y_encoded, sample_weights, test_size=0.1, random_state=42, stratify=y_encoded
    )

    model = xgb.XGBClassifier(random_state=42, use_label_encoder=False)

    param_grid = {
        'n_estimators': [100],
        'max_depth': [3],
        'learning_rate': [0.1],
        'subsample': [0.8],
        'colsample_bytree': [0.8]
    }

    # Searches for the best combination of Hyperparamaters to provide best 
    # estimators
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train, sample_weight=sample_weights_train)

    best_model = grid_search.best_estimator_

    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of XGBoost Model:", accuracy)

    return best_model, label_encoder

def predictPodium(best_model, label_encoder, new_data, original_drivers, original_constructors):
    
    new_predictions = best_model.predict(new_data)

    # Moving the predictions the model made into the pandas dataframe
    new_data['Predicted_Position'] = new_predictions
    # Unconverts the numerical data that was label encoded back into categorical data
    new_data['Predicted_Position'] = label_encoder.inverse_transform(new_data['Predicted_Position'])
    # adds the driver names from the original drivers list
    new_data['Driver'] = original_drivers.head(len(new_data)).values
    # adds the constructor names from the original drivers list
    new_data['Constructor'] = original_constructors.head(len(new_data)).values
    
    top_3_winners = new_data.sort_values(by='Predicted_Position').head(3)
    
    print(top_3_winners[['Driver', 'Constructor', 'Grid', 'Laps', 'Points', 'Predicted_Position']])

def main():

    race_name = 'monaco_grand_prix'

    data, drivers, constructors = loadDataBaseData(race_name)

    sample_weights = calculateSampleWeights(data)

    X, y = selectFeatures(data)

    model, label_encoder = trainModel(X, y, sample_weights)

    # Format for the output
    new_data = pd.DataFrame({
        'Grid': [1, 2, 3],
        'Laps': [71, 71, 71],
        'Points': [26, 18, 15]
    })

    # Below three lines of code is to avoid warnings in terminal about \
    # adding all the columns at once instead of one by one
    dummy_columns = {col: [0, 0, 0] for col in X.columns if col not in new_data.columns}
    dummy_df = pd.DataFrame(dummy_columns)

    new_data = pd.concat([new_data, dummy_df], axis=1)

    predictPodium(model, label_encoder, new_data, drivers, constructors)

# Starts the main method
if __name__ == "__main__":
    main()

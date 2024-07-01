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

    # Found a list online
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

    drivers = data['Driver']
    constructors = data['Constructor']

    data = pd.get_dummies(data, columns=['Driver', 'Constructor'])

    return data, drivers, constructors

def selectFeatures(data):
    features = ['Grid', 'Laps', 'Points'] + [col for col in data.columns if 'Driver_' in col or 'Constructor_' in col]
    X = data[features]
    y = data['Pos.']
    return X, y

def trainModel(X, y, sample_weights):
    # Encode target variable
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.1, random_state=10)

    # Initialize the XGBoost model
    model = xgb.XGBClassifier(random_state=42, use_label_encoder=False)

    # Fit the model to the training data with sample weights
    model.fit(X_train, y_train, sample_weight=sample_weights[X_train.index])

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Calculate and print the accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of XGBoost Model:", accuracy)

    return model, label_encoder

def predictPodium(best_model, label_encoder, new_data, original_drivers, original_constructors):
    new_predictions = best_model.predict(new_data)
    new_data['Predicted_Position'] = new_predictions

    # Reverse the label encoding to get original positions
    new_data['Predicted_Position'] = label_encoder.inverse_transform(new_data['Predicted_Position'])

    # Add driver and constructor information
    new_data['Driver'] = original_drivers.head(len(new_data)).values
    new_data['Constructor'] = original_constructors.head(len(new_data)).values

    # Sort and get top 3
    top_3_winners = new_data.sort_values(by='Predicted_Position').head(3)
    print(top_3_winners[['Driver', 'Constructor', 'Grid', 'Laps', 'Points', 'Predicted_Position']])

def main():
    race_name = 'italian_grand_prix'
    data, drivers, constructors = loadDataBaseData(race_name)
    X, y = selectFeatures(data)

    # Apply weights based on the 'Year' column
    year_weights = data['Year'].apply(lambda x: 1 + (x - data['Year'].min()) / (data['Year'].max() - data['Year'].min()))
    sample_weights = year_weights / year_weights.sum()

    model, label_encoder = trainModel(X, y, sample_weights)

    new_data = pd.DataFrame({
        'Grid': [1, 2, 3], 
        'Laps': [71, 71, 71],
        'Points': [26, 18, 15]
    })

    # Create a DataFrame with dummy columns for drivers and constructors
    dummy_columns = {col: [0, 0, 0] for col in X.columns if col not in new_data.columns}
    dummy_df = pd.DataFrame(dummy_columns)

    # Concatenate the new_data and dummy_df DataFrames
    new_data = pd.concat([new_data, dummy_df], axis=1)

    predictPodium(model, label_encoder, new_data, drivers, constructors)

if __name__ == "__main__":
    main()


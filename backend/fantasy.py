import pandas as pd
from prediction import loadDataBaseData, selectFeatures, calculateSampleWeights, trainModel

def simulate_event(data, event_name):
    data = data.copy()
    X, y = selectFeatures(data)
    sample_weights = calculateSampleWeights(data)
    model, label_encoder = trainModel(X, y, sample_weights)

    if event_name == "qualifying":
        event_positions = model.predict(X)
        data['Qualifying_Pos'] = label_encoder.inverse_transform(event_positions)
        data['Qualifying_Points'] = data['Qualifying_Pos'].apply(lambda x: max(10 - x + 1, 0))

    elif event_name == "sprint":
        event_positions = model.predict(X)
        data['Sprint_Pos'] = label_encoder.inverse_transform(event_positions)
        data['Sprint_Points'] = data['Sprint_Pos'].apply(lambda x: max(8 - x + 1, 0))
        data['Sprint_Points'] += 5  # Simulating overtakes and positions gained

    return data

def calculate_fantasy_points(data):
    data = simulate_event(data, "qualifying")
    data = simulate_event(data, "sprint")

    data['Fantasy_Points'] = 0

    race_points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

    data['Fantasy_Points'] += data['Pos.'].apply(lambda x: race_points.get(x, 0) if x <= 10 else 0)

    data['Fantasy_Points'] += data['Grid'] - data['Pos.']

    fastest_lap_driver = data.sample(n=1).index[0]
    data.loc[fastest_lap_driver, 'Fantasy_Points'] += 10

    driver_of_the_day = data.sample(n=1).index[0]
    data.loc[driver_of_the_day, 'Fantasy_Points'] += 10

    data['Fantasy_Points'] += data['Qualifying_Points'] + data['Sprint_Points']

    return data

def optimize_team(drivers_data, budget, driver_prices, constructor_prices):

    drivers_data = calculate_fantasy_points(drivers_data)
    drivers_data['Price'] = drivers_data['Driver'].map(driver_prices)

    # Handle NaN prices by removing those drivers
    drivers_data = drivers_data.dropna(subset=['Price'])

    driver_items = list(drivers_data[['Driver', 'Price', 'Fantasy_Points']].drop_duplicates().itertuples(index=False, name=None))

    constructor_items = [(name, price, drivers_data[drivers_data['Constructor_' + name] == 1]['Fantasy_Points'].sum()) for name, price in constructor_prices.items()]

    combined_items = driver_items + constructor_items
    combined_items = sorted(combined_items, key=lambda x: x[2] / x[1], reverse=True)  # Sort by points per cost

    selected_items = []
    total_cost = 0
    drivers_selected = set()
    constructors_selected = set()

    for item in combined_items:
        if total_cost + item[1] <= budget:
            if item[0] in driver_prices and len(drivers_selected) < 5 and item[0] not in drivers_selected:
                selected_items.append(item)
                total_cost += item[1]
                drivers_selected.add(item[0])
            elif item[0] in constructor_prices and len(constructors_selected) < 2 and item[0] not in constructors_selected:
                selected_items.append(item)
                total_cost += item[1]
                constructors_selected.add(item[0])
        if len(drivers_selected) >= 5 and len(constructors_selected) >= 2:
            break

    selected_drivers = [item for item in selected_items if item[0] in driver_prices]
    selected_constructors = [item for item in selected_items if item[0] in constructor_prices]

    return selected_drivers, selected_constructors

def main():
    race_name = 'australian_grand_prix'
    budget = 100
    
    driver_prices = {
        '#1 Max Verstappen': 31.0,
        '#4 Lando Norris': 26.1,
        '#16 Charles Leclerc': 23.0,
        '#55 Carlos Sainz Jr.': 22.2,
        '#11 Sergio Pérez': 22.7,
        '#81 Oscar Piastri': 22.3,
        '#63 George Russell': 20.9,
        '#44 Lewis Hamilton': 22.8,
        '#14 Fernando Alonso': 16.6,
        '#22 Yuki Tsunoda': 10.5,
        '#10 Pierre Gasly': 9.9,
        '#31 Esteban Ocon': 10.5,
        '#77 Valtteri Bottas': 7.7,
        '#24 Guanyu Zhou': 7.5,
        '#27 Nico Hülkenberg': 9.7,
        '#20 Kevin Magnussen': 10.8,
        '#23 Alexander Albon': 9.0,
        '#2 Logan Sargeant': 5.2,
        '#18 Lance Stroll': 15.1,
        '#3 Daniel Ricciardo': 10.9
    }
    constructor_prices = {
        'Red Bull': 29.0,
        'Mercedes': 22.6,
        'Ferrari': 23.1,
        'McLaren': 25.8,
        'Alpine': 9.9,
        'AlphaTauri': 7.0,
        'Aston Martin': 15.4,
        'Williams': 6.6,
        'Haas': 10.4,
        'Alfa Romeo': 10.7
    }

    data, drivers, constructors = loadDataBaseData(race_name)
    drivers_data = data[['Driver', 'Grid', 'Pos.', 'Constructor', 'Laps', 'Year', 'Points']]

    for constructor in constructor_prices.keys():
        drivers_data['Constructor_' + constructor] = (drivers_data['Constructor'] == constructor).astype(int)

    top_5_drivers, top_2_constructors = optimize_team(drivers_data, budget, driver_prices, constructor_prices)

    print("Top 5 Drivers to Select:")
    print(pd.DataFrame(top_5_drivers, columns=['Driver', 'Price', 'Fantasy_Points']))

    print("\nTop 2 Constructors to Select:")
    print(pd.DataFrame(top_2_constructors, columns=['Constructor', 'Price', 'Fantasy_Points']))

if __name__ == "__main__":
    main()

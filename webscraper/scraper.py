import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient, errors
from datetime import datetime
import time
import certifi

# Function to get all race URLs for a given year
def get_race_urls(year):
    url = f"https://pitwall.app/seasons/{year}-formula-1-world-championship"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all links to races
    race_links = soup.find_all('a', href=True)
    race_urls = []
    for link in race_links:
        href = link['href']
        if f"{year}-" in href and "-grand-prix" in href:
            race_urls.append(f"https://pitwall.app{href}")

    # Sort URLs based on appearance (alphabetically to maintain order even if the order of GPs changes)
    race_urls = sorted(set(race_urls))
    return race_urls

# Function to scrape data from a race page
def get_race_results(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find('table')
    
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')

    results = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        results.append(cols)

    df = pd.DataFrame(results, columns=headers)
    return df

# Connect to MongoDB with certifi for SSL certificates needed to do it this way because of multitude of connectivity issues
client = MongoClient(
    'mongodb+srv://dineshrkarnati:Collegeadmissio@formulafantasy.v9quue6.mongodb.net/?retryWrites=true&w=majority',
    tlsCAFile=certifi.where()
)
db = client['formula']

# Scrape data for the specified years and save to MongoDB
start_year = 2003
end_year = 1990

for year in range(start_year, end_year - 1, -1):
    race_urls = get_race_urls(year)
    for race_url in race_urls:
        df = get_race_results(race_url)
        if df is not None:
            df['Year'] = year
            race_name = race_url.split('/')[-1].replace(f'{year}-', '').replace('-grand-prix', '').replace('-', ' ')
            collection_name = f"{race_name}_grand_prix"
            collection = db[collection_name]
            print(f"Scraped data for year: {year}, race: {race_url}, storing in collection: {collection_name}")
            data_dict = df.to_dict("records")
            collection.insert_many(data_dict)

print("Data collection and insertion into MongoDB complete.")

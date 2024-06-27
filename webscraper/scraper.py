import requests
from bs4 import BeautifulSoup
import pandas as pd

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

    # Sort URLs based on appearance (usually corresponds to the order of races)
    race_urls = sorted(set(race_urls))
    return race_urls

# Function to scrape data from a race page
def get_race_results(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find('table')
    if not table:
        print(f"No table found for URL: {url}")
        return None
    
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')

    results = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        results.append(cols)

    df = pd.DataFrame(results, columns=headers)
    return df

# Scrape data for the specified years and save to CSV
start_year = 2023
end_year = 2015
all_results = []

for year in range(start_year, end_year - 1, -1):
    race_urls = get_race_urls(year)
    for race_url in race_urls:
        df = get_race_results(race_url)
        if df is not None:
            df['Year'] = year
            print(f"Scraped data for year: {year}, race: {race_url}")
            all_results.append(df)

if all_results:
    final_df = pd.concat(all_results, ignore_index=True)
    final_df.to_csv('f1_grand_prix_2015_2023.csv', index=False)

print("Finished collecting all the data!")

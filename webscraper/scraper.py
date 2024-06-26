import requests
from bs4 import BeautifulSoup
import pandas as pd

proceed = True
current_year = 2024
all_results = []

while proceed:
    url = f"https://pitwall.app/races/{current_year}-bahrain-grand-prix"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.find('table')
    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = table.find_all('tr')

        results = []
        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            results.append(cols)

        df = pd.DataFrame(results, columns=headers)
        df['Year'] = current_year
        print(str(current_year)+ "\n")
        all_results.append(df)

    current_year -= 1
    if current_year < 2015:
        proceed = False

final_df = pd.concat(all_results, ignore_index=True)
final_df.to_csv('bahrain_grand_prix_2015_2024.csv', index=False)
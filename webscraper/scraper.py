import requests
from bs4 import BeautifulSoup
import pandas as pd

proceed = True
current_year = ["2023-bahrain-grand-prix"]

while(proceed):
    url = "https://pitwall.app/races/2023-bahrain-grand-prix"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.find('table')
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')

    results = []

    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        results.append(cols)

    df = pd.DataFrame(results, columns=headers)
    print(df)
   
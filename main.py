import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"

# Add headers to prevent request blocking
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "lxml")

# Locate the table using ID (more reliable than class names)
table = soup.find("table", {"id": "per_game_stats"})

if table:
    # Find header row
    thead = table.find("thead")
    if thead:
        header_row = thead.find("tr")
        headers = [th.get_text(strip=True) for th in header_row.find_all("th")]
        print("Headers:", headers)

    else:
        print("No <thead> found!")
        headers = []  # Avoid errors if thead is missing

    # Extract data from table body
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else []

    data = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        if len(cols) == len(headers):  # Ensure the row has the correct number of columns
            data.append(cols)
        else:
            print(f"Skipping row with {len(cols)} columns (expected {len(headers)})")

    # Save to CSV
    df = pd.DataFrame(data, columns=headers)
    df.to_csv("nba_stats.csv", index=False)
    print(df.head())

else:
    print("Table not found!")

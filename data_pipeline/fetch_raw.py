import requests
from datetime import datetime
import os

def fetch_and_store_raw():
    url = "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"
    response = requests.get(url)

    if response.status_code == 200:
        today = datetime.today().strftime('%Y_%m_%d')
        os.makedirs("data_pipeline/logs", exist_ok=True)
        filepath = f"data_pipeline/logs/raw_{today}.xml"
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(response.text)
        print(f"Raw data saved to {filepath}")
    else:
        print("Failed to fetch")

if __name__ == "__main__":
    fetch_and_store_raw()

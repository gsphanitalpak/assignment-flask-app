import mysql.connector
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def load_data_into_mysql():
    today = datetime.today().strftime('%Y_%m_%d')
    processed_path = f"data_pipeline/logs/processed_{today}.json"

    if not os.path.exists(processed_path):
        print("Processed file not found.")
        return

    with open(processed_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()

        for item in records:
            try:
                date = item.get("date", "").strip()
                if not date:
                    date = None  # or set to "Unknown" if preferred

                cursor.execute("""
                    INSERT INTO pib_releases (title, summary, publication_date, url)
                    VALUES (%s, %s, %s, %s)
                """, (
                    item.get("title", ""),
                    item.get("summary", ""),
                    date,
                    item.get("url", "")
                ))
            except Exception as e:
                print(f"Error: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Data insertion successful.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

if __name__ == "__main__":
    load_data_into_mysql()

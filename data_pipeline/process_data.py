import xml.etree.ElementTree as ET
import json
from datetime import datetime
import os
import html

def parse_rss_to_json():
    today = datetime.today().strftime('%Y_%m_%d')
    raw_path = f"data_pipeline/logs/raw_{today}.xml"
    processed_path = f"data_pipeline/logs/processed_{today}.json"

    if not os.path.exists(raw_path):
        print("Raw file not found")
        return

    tree = ET.parse(raw_path)
    root = tree.getroot()

    items = []
    for item in root.findall('.//item'):
        try:
            title = item.find('title').text or ""
            link = item.find('link').text or ""

            # Fallback values for missing tags
            description = item.find('description').text if item.find('description') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""

            # Clean weird characters
            clean_title = html.unescape(title.strip())
            clean_description = html.unescape(description.strip())
            clean_link = html.unescape(link.strip())
            clean_pub_date = html.unescape(pub_date.strip())

            items.append({
                "title": clean_title,
                "summary": clean_description,
                "date": clean_pub_date,
                "url": clean_link
            })

        except Exception as e:
            print(f"Skipped item due to error: {e}")

    with open(processed_path, "w", encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Data saved to {processed_path}")

if __name__ == "__main__":
    parse_rss_to_json()

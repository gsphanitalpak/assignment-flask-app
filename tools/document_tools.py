import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_recent_documents(keyword: str, days: int = 7) -> str:
    """
    Query recent PIB documents containing a keyword within the last `days`.
    Returns a human-readable summary string.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT title, summary, publication_date
        FROM pib_releases
        WHERE (title LIKE %s OR summary LIKE %s)
          AND publication_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        ORDER BY publication_date DESC
        LIMIT 5;
    """

    like_term = f"%{keyword}%"
    try:
        cursor.execute(query, (like_term, like_term, days))
        results = cursor.fetchall()
    except Exception as e:
        return f"Error querying the database: {e}"

    cursor.close()
    conn.close()

    if not results:
        return f"No recent documents found for keyword '{keyword}'."

    summary = f"🔍 Found {len(results)} recent documents related to '{keyword}':\n\n"
    for i, row in enumerate(results, start=1):
        summary += f"{i}. {row['title']} ({row['publication_date']})\n"
        summary += f"    {row['summary'][:150]}...\n\n"

    return summary.strip()

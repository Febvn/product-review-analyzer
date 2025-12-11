
import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('review_analyzer.db')
        cursor = conn.cursor()
        
        # Check count of sentiments
        cursor.execute("SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment")
        results = cursor.fetchall()
        
        print("Sentiment distribution in DB:")
        for sentiment, count in results:
            print(f"- {sentiment}: {count}")
            
        conn.close()
    except Exception as e:
        print(f"Error checking DB: {e}")

if __name__ == "__main__":
    check_db()

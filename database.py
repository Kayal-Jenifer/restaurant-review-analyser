import sqlite3

DB_NAME = "reviews.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    # This allows us to access columns by name (e.g., row['username'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the reviews table if it doesn't already exist."""
    conn = get_db_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                review_text TEXT NOT NULL,
                entities TEXT,
                keywords TEXT,
                score REAL,
                label TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

def save_review(data):
    conn = get_db_connection()
    # Count your columns: 1.username, 2.review_text, 3.entities, 4.keywords, 5.score, 6.label, 7.timestamp
    query = '''
        INSERT INTO reviews 
        (username, review_text, entities, keywords, score, label, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    try:
        conn.execute(query, (
            data['username'], 
            data['text'],     # This matches 'text' from the record in app.py
            data['entities'], 
            data['keywords'], 
            data['score'], 
            data['label'], 
            data['timestamp']
        ))
        conn.commit()
    except Exception as e:
        print(f"Database Save Error: {e}") # This will show in your terminal if it fails
    finally:
        conn.close()

def fetch_all_reviews():
    """Retrieves all reviews, newest first."""
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_review_by_id(review_id):
    """Deletes a specific review record by its ID."""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Delete Error: {e}")
        return False
    finally:
        conn.close()
# risk_assessment_db.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
import sqlite3

def setup_database():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Risks (
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        impact INTEGER NOT NULL,
        likelihood INTEGER NOT NULL,
        risk_score INTEGER NOT NULL,
        category_id INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def setup_users_table():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def setup_categories_table():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    ''')
    conn.commit()
    conn.close()

def add_risk(description, impact, likelihood, category_id):
    risk_score = impact * likelihood
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Risks (description, impact, likelihood, risk_score, category_id) VALUES (?, ?, ?, ?, ?)", (description, impact, likelihood, risk_score, category_id))
    conn.commit()
    conn.close()

def add_user(username, password_hash):
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()

def add_category(name):
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_all_risks():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Risks.*, Categories.name, Statuses.status_name
    FROM Risks 
    LEFT JOIN Categories ON Risks.category_id = Categories.id
    LEFT JOIN Statuses ON Risks.status_id = Statuses.id
    """)
    risks = cursor.fetchall()
    conn.close()
    return risks

def get_all_categories():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_user_by_username(username):
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def setup_comments_table():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
        id INTEGER PRIMARY KEY,
        risk_id INTEGER,
        comment_text TEXT NOT NULL,
        FOREIGN KEY (risk_id) REFERENCES Risks(id)
    )
    ''')
    conn.commit()
    conn.close()

def add_comment(risk_id, comment_text):
    print(f"Adding comment: {comment_text} for risk: {risk_id}")  # Debug print
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Comments (risk_id, comment_text) VALUES (?, ?)", (risk_id, comment_text))
    conn.commit()
    conn.close()

def get_comments_for_risk(risk_id):
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Comments WHERE risk_id=?", (risk_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

def setup_status_table():
    with sqlite3.connect('risks.db') as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Statuses (
            id INTEGER PRIMARY KEY,
            status_name TEXT NOT NULL
        );
        """)
def add_status(status_name):
    with sqlite3.connect('risks.db') as conn:
        conn.execute("INSERT INTO Statuses (status_name) VALUES (?)", (status_name,))

def get_all_statuses():
    with sqlite3.connect('risks.db') as conn:
        return conn.execute("SELECT * FROM Statuses").fetchall()

def alter_risks_for_status():
    with sqlite3.connect('risks.db') as conn:
        try:
            # Try to add a new column for status_id
            conn.execute("ALTER TABLE Risks ADD COLUMN status_id INTEGER REFERENCES Statuses(id)")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e):
                pass  # Column already exists, so we skip adding it
            else:
                raise  # Some other error occurred

def add_risk(description, impact, likelihood, category_id, status_id):
    risk_score = impact * likelihood
    with sqlite3.connect('risks.db') as conn:
        conn.execute("""
        INSERT INTO Risks (description, impact, likelihood, risk_score, category_id, status_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (description, impact, likelihood, risk_score, category_id, status_id))

def update_risk(risk_id, description, impact, likelihood, category_id, status_id):
    risk_score = impact * likelihood
    with sqlite3.connect('risks.db') as conn:
        conn.execute("""
        UPDATE Risks 
        SET description = ?, impact = ?, likelihood = ?, risk_score = ?, category_id = ?, status_id = ?
        WHERE id = ?
        """, (description, impact, likelihood, risk_score, category_id, status_id, risk_id))

def get_risk_by_id(risk_id):
    with sqlite3.connect('risks.db') as conn:
        return conn.execute("SELECT * FROM Risks WHERE id = ?", (risk_id,)).fetchone()

def delete_risk(risk_id):
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Risks WHERE id=?", (risk_id,))
    conn.commit()
    conn.close()

def get_risk_count_by_status():
    with sqlite3.connect('risks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT Statuses.status_name, COUNT(Risks.id)
        FROM Risks
        LEFT JOIN Statuses ON Risks.status_id = Statuses.id
        GROUP BY Statuses.status_name
        """)
        counts = cursor.fetchall()
        return dict(counts)
def get_total_risks():
    with sqlite3.connect('risks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Risks")
        total = cursor.fetchone()[0]
        return total

def get_risks_by_status():
    conn = sqlite3.connect('risks.db')
    cursor = conn.cursor()
    
    # Query to get the count of risks for each status
    cursor.execute("""
    SELECT Statuses.status_name, COUNT(Risks.id)
    FROM Risks
    LEFT JOIN Statuses ON Risks.status_id = Statuses.id
    GROUP BY Risks.status_id
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    # Convert the result into a dictionary
    status_counts = {result[0]: result[1] for result in results}
    
    return status_counts

def setup_subscribers_table():
    try:
        with sqlite3.connect('risks.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """)
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

def add_subscriber(email):
    try:
        with sqlite3.connect('risks.db') as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO Subscribers (email, timestamp) VALUES (?, ?)", (email, timestamp))
            conn.commit()
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def get_subscribers():
    try:
        with sqlite3.connect('risks.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email, timestamp FROM Subscribers")
            subscribers = cursor.fetchall()
            return subscribers
    except Exception as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list instead of None

if __name__ == '__main__':
    setup_database()
    setup_users_table()
    setup_categories_table()
    setup_comments_table()
    setup_status_table()
    setup_subscribers_table()
    alter_risks_for_status()
    add_category('Financial')
    add_category('Operational')
    add_category('Strategic')
    add_status("Open")
    add_status("Closed")
    add_status("In Progress")
    print(get_all_statuses())





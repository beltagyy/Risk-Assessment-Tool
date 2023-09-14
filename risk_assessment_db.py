# risk_assessment_db.py

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
    SELECT Risks.*, Categories.name 
    FROM Risks 
    LEFT JOIN Categories ON Risks.category_id = Categories.id
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


if __name__ == '__main__':
    setup_database()
    setup_users_table()
    setup_categories_table()
    setup_comments_table()
    add_category('Financial')
    add_category('Operational')
    add_category('Strategic')






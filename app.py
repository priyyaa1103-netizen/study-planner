from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')

# Database setup
def init_db():
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subjects 
                 (id INTEGER PRIMARY KEY, name TEXT, hours REAL, priority INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY, subject_id INTEGER, date TEXT, 
                  duration REAL, notes TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    init_db()
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute("SELECT * FROM subjects ORDER BY priority DESC")
    subjects = c.fetchall()
    conn.close()
    return render_template('index.html', subjects=subjects)

# Add your full routes here (login, add_subject, etc.)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
**GitHub → app.py → FULL REPLACE:**
```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subjects 
                 (id INTEGER PRIMARY KEY, name TEXT, hours REAL, priority INTEGER)''')
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

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        name = request.form['name']
        hours = float(request.form['hours'])
        priority = int(request.form['priority'])
        conn = sqlite3.connect('study.db')
        c = conn.cursor()
        c.execute("INSERT INTO subjects (name, hours, priority) VALUES (?, ?, ?)", 
                  (name, hours, priority))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_subject.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

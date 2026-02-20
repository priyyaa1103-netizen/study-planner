from flask import Flask, request, redirect, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-2026'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT PRIMARY KEY, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE email=?", (email,))
        result = c.fetchone()
        conn.close()
        
        if result and check_password_hash(result[0], password):
            session['user'] = email
            return redirect('/dashboard')
        return '''
        <h1 style="color:red;">❌ Wrong Email or Password!</h1>
        <a href="/" style="color:blue;">Try Again</a>
        '''
    
    return '''
    <div style="max-width:400px; margin:50px auto; padding:30px; border:1px solid #ddd; border-radius:10px;">
    <h1 style="text-align:center;">📚 Study Planner Login</h1>
    <form method="POST">
        <input type="email" name="email" placeholder="Your Email" required 
               style="width:100%; padding:12px; margin:10px 0; border:1px solid #ccc; border-radius:5px;">
        <input type="password" name="password" placeholder="Password" required 
               style="width:100%; padding:12px; margin:10px 0; border:1px solid #ccc; border-radius:5px;">
        <button style="width:100%; padding:12px; background:#4CAF50; color:white; border:none; border-radius:5px; font-size:16px;">Login 🚀</button>
    </form>
    <p style="text-align:center; margin-top:20px;"><a href="/register" style="color:blue;">Register ➕</a></p>
    </div>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT email FROM users WHERE email=?", (email,))
        if c.fetchone():
            conn.close()
            return '''
            <h1 style="color:red;">❌ Email already exists!</h1>
            <a href="/register">Try Again</a>
            '''
        
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
        conn.close()
        
        return '''
        <h1 style="color:green;">✅ Account Created! <a href="/">Login Now</a></h1>
        '''
    
    return '''
    <div style="max-width:400px; margin:50px auto; padding:30px; border:1px solid #ddd; border-radius:10px;">
    <h1 style="text-align:center;">➕ Create Account</h1>
    <form method="POST">
        <input type="email" name="email" placeholder="Your Email" required 
               style="width:100%; padding:12px; margin:10px 0; border:1px solid #ccc; border-radius:5px;">
        <input type="password" name="password" placeholder="Password" required 
               style="width:100%; padding:12px; margin:10px 0; border:1px solid #ccc; border-radius:5px;">
        <button style="width:100%; padding:12px; background:#2196F3; color:white; border:none; border-radius:5px;">Register ✅</button>
    </form>
    <p style="text-align:center;"><a href="/" style="color:blue;">Have account? Login</a></p>
    </div>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    
    user_email = session['user']
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Study Planner</title></head>
    <body style="font-family:Arial; margin:0; padding:0;">
    <h1 style="text-align:center; color:white; background:linear-gradient(45deg, blue, purple); padding:30px; margin:0;">Welcome {user_email}! 🎓</h1>
    <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap; padding:50px;">
    <div style="background:linear-gradient(45deg, #2196F3, blue); color:white; padding:30px; border-radius:15px;">
    <h2>📚 Study Dashboard</h2><p>1st,2nd,3rd Year</p></div>
    <div style="background:linear-gradient(45deg, #4CAF50, green); color:white; padding:30px; border-radius:15px;">
    <h2>🎯 Set Goal</h2><p>Target Score</p></div>
    <div style="background:linear-gradient(45deg, #FF9800, orange); color:white; padding:30px; border-radius:15px;">
    <h2>📊 View Progress</h2><p>Your Goals</p></div>
    </div>
    <div style="text-align:center; margin-top:30px;">
    <a href="/logout" style="background:red; color:white; padding:10px 20px; border-radius:5px; text-decoration:none;">Logout 🚪</a>
    </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)

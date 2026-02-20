GitHub → study-planner-pro → **app.py** create → Paste:

```python
from flask import Flask, request, render_template_string, session
import os

app = Flask(__name__)
app.secret_key = 'study-planner-pro'
app.config['DEBUG'] = True

# Fake users database
users = {'priyyaa@gmail.com': {'name': 'Priyyaa', 'password': '123456'}}
goals = {}

# HTML Templates
LOGIN = '''
<!DOCTYPE html>
<html>
<head>
    <title>Study Planner Pro</title>
    <style>body{font-family:Arial;padding:50px;background:#f0f8ff}</style>
</head>
<body>
    <h1>🎓 Study Planner Pro</h1>
    <form method="POST">
        <input name="email" placeholder="Email" style="padding:10px;width:250px;margin:5px" required><br>
        <input name="password" type="password" placeholder="Password" style="padding:10px;width:250px;margin:5px" required><br>
        <button type="submit" style="padding:10px 20px;background:#4CAF50;color:white;border:none;cursor:pointer">Login</button>
    </form>
</body>
</html>
'''

DASHBOARD = '''
<!DOCTYPE html>
<html>
<head><title>Dashboard</title>
<style>body{font-family:Arial;padding:50px;background:#e8f5e8} button{padding:15px 25px;margin:10px;font-size:18px;background:#2196F3;color:white;border:none;border-radius:5px;cursor:pointer}</style>
</head>
<body>
    <h1>👋 Welcome {{name}}! Study Planner Pro</h1>
    <div style="margin:30px 0">
        <a href="/study"><button>📚 Study Dashboard</button></a>
        <a href="/goals"><button>🎯 Set Goal</button></a>
        <a href="/reminders"><button>⏰ Reminders</button></a>
    </div>
    <a href="/"><button style="background:#f44336">Logout</button></a>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user'] = email
            return render_template_string(DASHBOARD, name=users[email]['name'])
    return render_template_string(LOGIN)

@app.route('/study')
def study():
    if 'user' not in session:
        return '<h1>Please login first!</h1><a href="/">Login</a>'
    return '<h1>📚 Study Dashboard (Coming Soon!)</h1><a href="/">← Back</a>'

@app.route('/goals')
def goals():
    if 'user' not in session:
        return '<h1>Please login first!</h1><a href="/">Login</a>'
    return '<h1>🎯 Goals (Coming Soon!)</h1><a href="/">← Back</a>'

@app.route('/reminders')
def reminders():
    if 'user' not in session:
        return '<h1>Please login first!</h1><a href="/">Login</a>'
    return '<h1>⏰ Reminders (Coming Soon!)</h1><a href="/">← Back</a>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)

from flask import Flask, request, render_template_string, jsonify
import os

app = Flask(__name__)
app.config['DEBUG'] = True

# HTML Templates
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Study Planner</title></head>
<body>
    <h1>🎓 Study Planner LIVE!</h1>
    <form method="POST">
        <input name="email" placeholder="Email" required><br>
        <input name="password" type="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <p><a href="/dashboard">Dashboard →</a></p>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
    <h1>📚 Study Planner Dashboard</h1>
    <h3>File Upload</h3>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required><br>
        <button type="submit">Upload File</button>
    </form>
    <p><a href="/">← Home</a></p>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email', 'guest')
        return f'<h1>Welcome {email}! 🎉</h1><a href="/dashboard">Dashboard →</a>'
    return LOGIN_HTML

@app.route('/login', methods=['GET', 'POST'])
def login():
    return home()  # Same as home

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        return '<h1>File Upload Success! ✅</h1><a href="/dashboard">Upload More</a>'
    return DASHBOARD_HTML

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "Study Planner LIVE!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

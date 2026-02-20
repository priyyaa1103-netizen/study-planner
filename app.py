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

@app.route('/delete/<int:subject_id>')
def delete_subject(subject_id):
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))
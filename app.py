@app.route('/delete/<int:subject_id>')
def delete_subject(subject_id):
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

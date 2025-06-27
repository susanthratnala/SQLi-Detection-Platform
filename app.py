from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for, session
from flask_cors import CORS
from detector import is_sqli
from logger import log_sqli_attempt
from notifier import send_email, send_slack
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import csv
import io
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)
limiter = Limiter(get_remote_address, app=app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
@limiter.limit("10 per minute")
def submit():
    user_input = request.form.get('input')
    honeypot = request.form.get('honeypot')
    ip = request.remote_addr

    if honeypot:
        return jsonify({"alert": "Bot detected"}), 403

    if is_sqli(user_input):
        log_sqli_attempt(ip, user_input)
        send_email(ip, user_input)
        send_slack(user_input)
        return jsonify({"alert": "⚠️ SQL Injection attempt detected!"}), 400
    return jsonify({"message": "✅ Input accepted."})

@app.route('/logs')
def view_logs():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("SELECT ip, payload, timestamp FROM sqli_logs ORDER BY timestamp DESC")
    logs = c.fetchall()
    conn.close()
    return render_template('dashboard.html', logs=logs)

@app.route('/export/csv')
def export_csv():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("SELECT ip, payload, timestamp FROM sqli_logs ORDER BY timestamp DESC")
    logs = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['IP Address', 'Payload', 'Timestamp'])
    writer.writerows(logs)

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                     as_attachment=True, download_name='sqli_logs.csv')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'adminpass':
            session['logged_in'] = True
            return redirect(url_for('view_logs'))
    return render_template('login.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

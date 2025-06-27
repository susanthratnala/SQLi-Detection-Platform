# SQL Injection Detection Platform

This project is a simple yet effective web platform for detecting SQL Injection attacks in web applications. It logs attack data, provides a dashboard, and sends real-time alerts via email and Slack.

## 🚀 Features

- Regex-based detection of common SQLi payloads
- Logs suspicious inputs to SQLite database
- Rate limiting to prevent brute-force attacks
- Admin dashboard to review logs
- Email and Slack notifications
- Honeypot field to detect bots
- Clean dark theme UI

## 💻 Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS (Dark Theme)
- **Database:** SQLite
- **Notifications:** smtplib (Email), Slack Webhooks
- **Environment:** Python 3.x

## 🧰 Installation

1. Clone the repository:

git clone https://github.com/susanthratnala/SQLi-Detection-Platform

   cd SQLi-Detection-Platform

2. Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Copy `.env.example` to `.env` and fill in your credentials:

cp .env.example .env

- `EMAIL_USER` - Your email (e.g., Gmail)
- `EMAIL_PASS` - Your app-specific password
- `SLACK_WEBHOOK` - Your Slack webhook URL

5. Initialize the logs database (first run creates it automatically).

## 🏃 Running the App

python3 app.py

Open your browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔑 Admin Login

- **Username:** admin
- **Password:** adminpass

## 🛡️ Disclaimer

This project is for educational purposes only. Use responsibly.

## ✨ Credits

Developed by Team Gray_Alpha.


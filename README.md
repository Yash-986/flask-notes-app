📝 NoteSpace – Flask Notes App

A modern, dark-themed Notes Management Application built using Python Flask and SQLite.

✨ Features :-
User registration and login
Secure password hashing
Create, read, update and delete notes
Search notes by title and content
Filter notes by category
Personal user dashboard
User-specific private notes
Profile management
CSRF protection
Responsive dark-themed interface

🛠️ Technologies Used :-
Python
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
SQLite
HTML5
CSS3
Bootstrap 5
JavaScript

📁 Project Structure :-
notes_app/
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
├── templates/
├── static/
└── instance/

🚀 Installation
Clone the repository: git clone https://github.com/YOUR_USERNAME/flask-notes-app.git

Navigate to the project: cd flask-notes-app

Create a virtual environment: python -m venv venv

Activate the environment: venv\Scripts\activate

Install dependencies: pip install -r requirements.txt

Set a secure Flask secret key using an environment variable.
Paste this command in termial to set secret-key: $env:SECRET_KEY="your-random-secret-key"

Run the application: python app.py
Open:
http://127.0.0.1:5000/

🔒 Security
Passwords are stored as hashes.
CSRF protection is enabled.
Users can only access their own notes.
Secret keys should be configured through environment variables.

👨‍💻 Author : Yash-986

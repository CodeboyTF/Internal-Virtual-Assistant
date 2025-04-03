from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz
import csv
import datetime
import secrets
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

# Load environment variables
load_dotenv()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'admin_login'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key')

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://flask_user:sisal33@localhost:5432/enquiries_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app)

# Encryption key management
KEY_FILE = "secret.key"

if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_file(input_file, output_file):
    key = load_key()
    cipher = Fernet(key)
    with open(input_file, "rb") as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)
    with open(output_file, "wb") as file:
        file.write(encrypted_data)
    os.remove(input_file)

def decrypt_file(input_file, output_file):
    key = load_key()
    cipher = Fernet(key)
    with open(input_file, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    with open(output_file, "wb") as file:
        file.write(decrypted_data)

# Decrypt Enquiries.csv for reading
if os.path.exists("Enquiries_encrypted.csv"):
    decrypt_file("Enquiries_encrypted.csv", "Enquiries.csv")

# Load the cleaned CSV file
data = pd.read_csv('Enquiries.csv')

# Encrypt it again after loading
encrypt_file("Enquiries.csv", "Enquiries_encrypted.csv")

# Database Models
class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    enquiry = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables and default admin
with app.app_context():
    db.create_all()
    if not AdminUser.query.filter_by(username='sisalgroup33').first():
        admin = AdminUser(username='sisalgroup33')
        admin.set_password('admin@sisalcbot33') 
        db.session.add(admin)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = AdminUser.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    enquiries = Enquiry.query.order_by(Enquiry.timestamp.desc()).all()
    return render_template('admin_dashboard.html', enquiries=enquiries)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

# Main Chat Routes
@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('user_message')
def handle_message(data):
    user_message = data.get('message', '')
    name = data.get('name', '')
    surname = data.get('surname', '')
    email = data.get('email', '')
    enquiry = data.get('enquiry', '')
    response = find_best_response(user_message)
    
    if name and surname and email and enquiry:
        save_enquiry(name, surname, email, enquiry)
        response = "Thank you! Your enquiry has been submitted."
    
    log_chat_data_to_csv(user_message, response)
    emit('bot_response', {'message': response})

# Helper Functions
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

def find_best_response(user_message):
    user_tokens = preprocess_text(user_message)
    best_score = 0
    best_response = "I'm sorry, I didn't understand that. Could you rephrase?"
    
    for _, row in data.iterrows():
        row_tokens = preprocess_text(row['question'])
        score = fuzz.partial_ratio(" ".join(user_tokens), " ".join(row_tokens))
        if score > best_score:
            best_score = score
            best_response = row['response']
    return best_response

def log_chat_data_to_csv(user_message, bot_response):
    if os.path.exists("chat_logs_encrypted.csv"):
        decrypt_file("chat_logs_encrypted.csv", "chat_logs.csv")
    with open("chat_logs.csv", "a", newline="") as log_file:
        writer = csv.writer(log_file)
        writer.writerow([datetime.datetime.now(), user_message, bot_response])
    encrypt_file("chat_logs.csv", "chat_logs_encrypted.csv")

def save_enquiry(name, surname, email, enquiry):
    new_enquiry = Enquiry(name=name, surname=surname, email=email, enquiry=enquiry)
    db.session.add(new_enquiry)
    db.session.commit()

    # Add this route before if __name__ == '__main__':
@app.route('/admin/delete/<int:enquiry_id>', methods=['POST'])
@login_required
def delete_enquiry(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    db.session.delete(enquiry)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
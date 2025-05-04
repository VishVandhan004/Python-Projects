from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, User, Subscription
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/subscriptions')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

db.init_app(app)
mail = Mail(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def home():
    return redirect(url_for('calendar_view'))

@app.route('/calendar')
@login_required
def calendar_view():
    return render_template('calendar.html')

@app.route('/api/subscriptions')
@login_required
def get_subscriptions():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    events = []
    for sub in subscriptions:
        events.append({
            'title': f"{sub.name} (${sub.cost})",
            'start': sub.next_payment_date.isoformat(),
            'color': 'red' if sub.cost > 10 else 'green'
        })
    return jsonify(events)

@app.route('/dashboard')
@login_required
def dashboard():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    categories = {}
    for sub in subscriptions:
        categories[sub.category] = categories.get(sub.category, 0) + sub.cost
    return render_template('dashboard.html', categories=categories)

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Email reminders
def send_reminders():
    with app.app_context():
        due_subs = Subscription.query.filter(
            Subscription.next_payment_date == datetime.today().date()
        ).all()
        for sub in due_subs:
            msg = Message(
                "Payment Due Today!",
                recipients=[sub.user.email],
                body=f"Don't forget to pay ${sub.cost} for {sub.name}!"
            )
            mail.send(msg)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminders, 'cron', hour=9)  # Run daily at 9 AM
scheduler.start()

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
import logging

# Configure logging to output messages to both a file and the console.
# This helps in debugging by preserving logs with timestamps and severity levels.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Import required libraries for web handling, database interaction, and security.
# These are essential for building the web server and managing user data securely.
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2 import sql
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from a `.env` file for secure configuration.
# This allows keeping sensitive values like DB credentials out of the codebase.
load_dotenv()

# Initialize Flask application with paths to templates and static files.
# The `app` object will be used to define routes and start the server.
app = Flask(__name__, template_folder='templates', static_folder='static')

# Set a secret key for session encryption and CSRF protection.
# It uses a secure environment variable if available, otherwise falls back to a default.
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Establish a connection to the PostgreSQL database based on environment configuration.
# If deployed, it uses the DATABASE_URL; otherwise, it connects to a local database.
def get_db_connection():
    try:
        if os.environ.get('DATABASE_URL'):
            logging.debug(f"Connecting to database using URL: {os.environ['DATABASE_URL']}")
            conn = psycopg2.connect(
                os.environ['DATABASE_URL'],
                sslmode='prefer',
                connect_timeout=5
            )
        else:
            logging.debug("Using local database connection")
            conn = psycopg2.connect(
                dbname='finance_tracker',
                user='finance_user',
                password=os.environ.get('DB_PASSWORD', 'yourpassword'),
                host='localhost',
                port=5432,
                sslmode='prefer',
                connect_timeout=5
            )
        logging.debug("Database connection successful")
        return conn
    except Exception as e:
        # Log critical error and raise it for visibility if DB connection fails.
        # This prevents silent failures during development or production.
        logging.critical(f"Database connection failed: {e}")
        raise

# Create necessary tables and indexes if they do not exist in the database.
# This function ensures the application has a working schema before user access.
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create users table to store user credentials and account info.
        # This includes a unique username and email for login and communication.
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        # Try to alter columns to increase capacity and maintain schema integrity.
        # If the changes already exist, log that it's skipped without interrupting flow.
        try:
            cur.execute("""
                ALTER TABLE users
                ALTER COLUMN email TYPE VARCHAR(255),
                ALTER COLUMN password TYPE VARCHAR(255)
            """)
        except Exception as e:
            logging.info("Alter skipped or unnecessary: " + str(e))

        # Create the expenses table to log transactions tied to each user.
        # Each record includes amount, category, note, and timestamp.
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                amount NUMERIC(12,2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                note TEXT,
                date TIMESTAMP NOT NULL
            )
        ''')

        # Add indexes to optimize performance on common queries like filtering by date.
        # These improve loading time on dashboards and stats views.
        cur.execute('CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)')

        conn.commit()
    except Exception as e:
        # Log database initialization errors to help diagnose schema problems.
        logging.error(f"Database initialization error: {e}")
        raise
    finally:
        # Close resources to avoid memory leaks and keep DB connections clean.
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

# Run the database setup to ensure tables exist before handling user requests.
# This prevents runtime errors due to missing tables during app usage.
init_db()

# Display the home page with links or intro information.
# Acts as the landing page for both new and returning users.
@app.route('/')
def index():
    return render_template('index.html')

# Handle both display and processing of the login form.
# Validates user credentials and starts a session on success.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Fetch hashed password and user ID for the provided username.
            # If the user exists, verify the password hash.
            cur.execute('SELECT id, password FROM users WHERE username = %s', (username,))
            user = cur.fetchone()
            
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')
        except Exception as e:
            flash('Database error occurred')
            print(e)
        finally:
            cur.close()
            conn.close()
    
    return render_template('login.html')

# Register a new user by validating and storing their credentials.
# Ensures username/email uniqueness and hashes passwords before storing.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '')[:50]
        email = request.form.get('email', '')[:100]
        password = request.form.get('password', '')
        
        if not all([username, email, password]):
            flash('All fields are required')
            return render_template('signup.html')
            
        if len(username) < 3:
            flash('Username must be at least 3 characters')
            return render_template('signup.html')
            
        if len(password) < 8:
            flash('Password must be at least 8 characters')
            return render_template('signup.html')
            
        if '@' not in email:
            flash('Invalid email format')
            return render_template('signup.html')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            hashed_pw = generate_password_hash(password)

            cur.execute(
                'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                (username, email, hashed_pw)
            )
            conn.commit()
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            flash('Username or email already exists')
        except Exception as e:
            print(f"Signup error: {str(e)}")
            flash('Database error occurred')
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()
    
    return render_template('signup.html')

# End the user session and show a logout confirmation.
# Clears session data to ensure secure sign-out.
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template('logout.html')

# Show dashboard with recent transactions and total expenses.
# Only accessible to authenticated users with valid sessions.
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Retrieve the 5 most recent expenses for display.
        # Also compute the total amount spent by the user.
        cur.execute('''
            SELECT amount, category, note, date 
            FROM expenses 
            WHERE user_id = %s 
            ORDER BY date DESC LIMIT 5
        ''', (session['user_id'],))
        recent_expenses = cur.fetchall()
        
        cur.execute('''
            SELECT COALESCE(SUM(amount), 0) 
            FROM expenses 
            WHERE user_id = %s
        ''', (session['user_id'],))
        total_spent = cur.fetchone()[0]
        
        return render_template('dashboard.html', 
                             expenses=recent_expenses,
                             total=total_spent)
    except Exception as e:
        flash('Error loading dashboard')
        print(e)
        return redirect(url_for('index'))
    finally:
        cur.close()
        conn.close()

# Display a form to add new expenses and insert them into the DB.
# After submission, redirect back to the dashboard for feedback.
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        note = request.form.get('note', '')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('''
                INSERT INTO expenses (user_id, amount, category, note, date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (session['user_id'], amount, category, note, date))
            conn.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Error saving expense')
            print(e)
        finally:
            cur.close()
            conn.close()
    
    return render_template('add_expense.html')

# Provide analytical summaries of user spending by date ranges.
# Displays daily, monthly, and yearly aggregates of expenses.
@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT TO_CHAR(date, 'DD Mon YYYY') as day, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s 
            GROUP BY day 
            ORDER BY MAX(date) DESC
        ''', (session['user_id'],))
        daily_stats = cur.fetchall()
        
        cur.execute('''
            SELECT TO_CHAR(date, 'Mon YYYY') as month, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s 
            GROUP BY month 
            ORDER BY MAX(date) DESC
        ''', (session['user_id'],))
        monthly_stats = cur.fetchall()
        
        cur.execute('''
            SELECT TO_CHAR(date, 'YYYY') as year, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s 
            GROUP BY year 
            ORDER BY year DESC
        ''', (session['user_id'],))
        yearly_stats = cur.fetchall()
        
        return render_template('stats.html', 
                            daily_stats=daily_stats,
                            monthly_stats=monthly_stats,
                            yearly_stats=yearly_stats)
    except Exception as e:
        flash('Error loading statistics')
        print(e)
        return redirect(url_for('dashboard'))
    finally:
        cur.close()
        conn.close()

# Start the Flask development server with a default port or custom port.
# Binding to 0.0.0.0 allows containerized or cloud-based hosting.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

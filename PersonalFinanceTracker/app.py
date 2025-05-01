import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2 import sql
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Database connection
def get_db_connection():
    if os.environ.get('DATABASE_URL'):
        result = urlparse(os.environ['DATABASE_URL'])
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
            sslmode='require'
        )
    else:
        conn = psycopg2.connect(
            dbname='finance_tracker',
            user='postgres',
            password=os.environ.get('DB_PASSWORD', 'postgres'),
            host='localhost'
        )
    return conn

# Initialize database
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                note TEXT,
                date TIMESTAMP NOT NULL
            )
        ''')
        
        cur.execute('CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)')
        
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        cur.close()
        conn.close()

init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                (username, email, password)
            )
            conn.commit()
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            flash('Username or email already exists')
        except Exception as e:
            flash('Database error occurred')
            print(e)
        finally:
            cur.close()
            conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template('logout.html')  # Changed from redirect to template render


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT amount, category, note, date 
            FROM expenses 
            WHERE user_id = %s 
            ORDER BY date DESC LIMIT 5
        ''', (session['user_id'],))
        recent_expenses = cur.fetchall()
        
        # Get total spending
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

@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Daily stats
        cur.execute('''
            SELECT TO_CHAR(date, 'DD Mon YYYY') as day, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s 
            GROUP BY day 
            ORDER BY MAX(date) DESC
        ''', (session['user_id'],))
        daily_stats = cur.fetchall()
        
        # Monthly stats
        cur.execute('''
            SELECT TO_CHAR(date, 'Mon YYYY') as month, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s 
            GROUP BY month 
            ORDER BY MAX(date) DESC
        ''', (session['user_id'],))
        monthly_stats = cur.fetchall()
        
        # Yearly stats
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

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
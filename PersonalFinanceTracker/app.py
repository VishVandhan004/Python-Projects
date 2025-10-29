import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

def get_db_connection():
    try:
        # ALWAYS use SQLite locally - simple fix
        import sqlite3
        conn = sqlite3.connect('finance_tracker.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logging.critical(f"Database connection failed: {e}")
        raise

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create tables with SQLite syntax
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category VARCHAR(50) NOT NULL,
                note TEXT,
                date TIMESTAMP NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category VARCHAR(50) NOT NULL,
                name VARCHAR(100),
                amount REAL NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')

        # Create indexes
        cur.execute('CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_investments_user_id ON investments(user_id)')

        conn.commit()
    except Exception as e:
        logging.error(f"Database initialization error: {e}")
        raise
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

init_db()

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

            # Use ? for SQLite parameter placeholder
            cur.execute('SELECT id, password FROM users WHERE username = ?', (username,))
            user = cur.fetchone()
            
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')
        except Exception as e:
            flash('Database error occurred')
            print(f"Login error: {e}")
        finally:
            cur.close()
            conn.close()
    
    return render_template('login.html')

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

            # Use ? for SQLite parameter placeholder
            cur.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_pw)
            )
            conn.commit()
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            if 'UNIQUE' in str(e) or 'unique' in str(e):
                flash('Username or email already exists')
            else:
                print(f"Signup error: {str(e)}")
                flash('Database error occurred')
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template('logout.html')

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
            WHERE user_id = ? 
            ORDER BY date DESC LIMIT 5
        ''', (session['user_id'],))
        recent_expenses = cur.fetchall()
        
        cur.execute('''
            SELECT COALESCE(SUM(amount), 0) 
            FROM expenses 
            WHERE user_id = ?
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
                VALUES (?, ?, ?, ?, ?)
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

@app.route('/investments')
def investments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            SELECT id, category, name, amount, date_added, notes 
            FROM investments 
            WHERE user_id = ? 
            ORDER BY date_added DESC
        ''', (session['user_id'],))
        investments = cur.fetchall()
        
        total_value = sum(inv[3] for inv in investments) if investments else 0
        
        categories = {}
        for inv in investments:
            category = inv[1]
            amount = inv[3]
            categories[category] = categories.get(category, 0) + amount
        
        chart_labels = list(categories.keys())
        chart_values = list(categories.values())
        
        return render_template('investments.html', 
                             investments=investments,
                             total_value=total_value,
                             categories_count=len(categories),
                             chart_labels=chart_labels,
                             chart_values=chart_values)
    except Exception as e:
        flash('Error loading investments')
        logging.error(f"Investments error: {e}")
        return redirect(url_for('dashboard'))
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()
        
@app.route('/add_investment', methods=['POST'])
def add_investment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form['category']
        name = request.form.get('name', '')
        amount = float(request.form['amount'])
        notes = request.form.get('notes', '')
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('''
                INSERT INTO investments (user_id, category, name, amount, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], category, name, amount, notes))
            
            conn.commit()
            flash('Investment added successfully!', 'success')
        except Exception as e:
            flash('Error saving investment')
            logging.error(f"Add investment error: {e}")
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()
    
    return redirect(url_for('investments'))

@app.route('/delete_investment/<int:id>', methods=['POST'])
def delete_investment(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT user_id FROM investments WHERE id = ?', (id,))
        investment = cur.fetchone()
        
        if investment and investment[0] == session['user_id']:
            cur.execute('DELETE FROM investments WHERE id = ?', (id,))
            conn.commit()
            flash('Investment deleted successfully!', 'success')
        else:
            flash('Investment not found or unauthorized', 'error')
    except Exception as e:
        flash('Error deleting investment')
        logging.error(f"Delete investment error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()
    
    return redirect(url_for('investments'))

@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # SQLite date formatting
        cur.execute('''
            SELECT strftime('%d %m %Y', date) as day, SUM(amount) 
            FROM expenses 
            WHERE user_id = ? 
            GROUP BY day 
            ORDER BY date DESC
        ''', (session['user_id'],))
        daily_stats = cur.fetchall()
        
        cur.execute('''
            SELECT strftime('%m %Y', date) as month, SUM(amount) 
            FROM expenses 
            WHERE user_id = ? 
            GROUP BY month 
            ORDER BY date DESC
        ''', (session['user_id'],))
        monthly_stats = cur.fetchall()
        
        cur.execute('''
            SELECT strftime('%Y', date) as year, SUM(amount) 
            FROM expenses 
            WHERE user_id = ? 
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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
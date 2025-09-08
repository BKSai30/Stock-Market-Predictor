import os
import sqlite3
import logging

def setup_directories():
    """Create necessary directories"""
    directories = [
        'data/cache',
        'data/models', 
        'logs',
        'static/css',
        'static/js',
        'static/images'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def setup_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('stock_app.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Portfolio table  
    c.execute('''CREATE TABLE IF NOT EXISTS portfolio
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  symbol TEXT NOT NULL,
                  shares INTEGER NOT NULL,
                  purchase_price REAL NOT NULL,
                  purchase_date DATE NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Calibrations table
    c.execute('''CREATE TABLE IF NOT EXISTS calibrations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  symbol TEXT NOT NULL,
                  calibration_data TEXT,
                  accuracy_score REAL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    print("Logging configured successfully")

if __name__ == '__main__':
    print("Setting up Stock Market Predictor environment...")
    setup_directories()
    setup_database()
    setup_logging()
    print("Environment setup completed!")

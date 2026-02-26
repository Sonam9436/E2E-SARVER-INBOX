import sqlite3
import os

DB_NAME = "automation_app.db"

def get_db_connection():
    """Database connection create karne ke liye"""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Table create karne ka function"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Single line execution for stability
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                password TEXT,
                cookies TEXT,
                chat_id TEXT,
                delay INTEGER DEFAULT 5,
                messages TEXT,
                name_prefix TEXT,
                is_running INTEGER DEFAULT 0,
                admin_e2ee_thread_id TEXT
            )
        ''')
        conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# --- Automation Status Functions ---

def set_automation_running(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_running = ? WHERE user_id = ?",
        (1 if status else 0, user_id)
    )
    conn.commit()
    conn.close()

def is_automation_running(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT is_running FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return True if user['is_running'] == 1 else False
    return False

# --- Admin & Thread Functions ---

def get_admin_e2ee_thread_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT admin_e2ee_thread_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user['admin_e2ee_thread_id'] if user else None

def save_admin_e2ee_thread_id(user_id, thread_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET admin_e2ee_thread_id = ? WHERE user_id = ?",
        (thread_id, user_id)
    )
    conn.commit()
    conn.close()

# --- User Data Management ---

def save_user_config(user_id, config_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    user = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    
    if user:
        cursor.execute('''
            UPDATE users SET 
            cookies = ?, chat_id = ?, delay = ?, messages = ?, name_prefix = ?
            WHERE user_id = ?
        ''', (
            config_data.get('cookies'),
            config_data.get('chat_id'),
            config_data.get('delay'),
            config_data.get('messages'),
            config_data.get('name_prefix'),
            user_id
        ))
    else:
        cursor.execute('''
            INSERT INTO users (user_id, cookies, chat_id, delay, messages, name_prefix, is_running)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        ''', (
            user_id,
            config_data.get('cookies'),
            config_data.get('chat_id'),
            config_data.get('delay'),
            config_data.get('messages'),
            config_data.get('name_prefix')
        ))
    
    conn.commit()
    conn.close()

def get_user_config(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

# Database ko initialize karein jab file load ho
init_db()
def set_automation_running(user_id, status):
    """User ki automation state (running/stopped) update karein"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_running = ? WHERE user_id = ?",
        (1 if status else 0, user_id)
    )
    conn.commit()
    conn.close()

def is_automation_running(user_id):
    """Check karein ke kya automation chal rahi hai"""
    conn = get_db_connection()
    user = conn.execute("SELECT is_running FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user['is_running'] if user else False

# --- Admin & Thread Functions ---

def get_admin_e2ee_thread_id(user_id):
    """Admin ki encrypted chat ID nikalne ke liye"""
    conn = get_db_connection()
    user = conn.execute("SELECT admin_e2ee_thread_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user['admin_e2ee_thread_id'] if user else None

def save_admin_e2ee_thread_id(user_id, thread_id):
    """Admin thread ID save karne ke liye"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET admin_e2ee_thread_id = ? WHERE user_id = ?",
        (thread_id, user_id)
    )
    conn.commit()
    conn.close()

# --- User Data Management ---

def save_user_config(user_id, config_data):
    """User ki settings (cookies, messages, delay) save karein"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    user = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    
    if user:
        cursor.execute('''
            UPDATE users SET 
            cookies = ?, chat_id = ?, delay = ?, messages = ?, name_prefix = ?
            WHERE user_id = ?
        ''', (
            config_data.get('cookies'),
            config_data.get('chat_id'),
            config_data.get('delay'),
            config_data.get('messages'),
            config_data.get('name_prefix'),
            user_id
        ))
    else:
        cursor.execute('''
            INSERT INTO users (user_id, cookies, chat_id, delay, messages, name_prefix)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            config_data.get('cookies'),
            config_data.get('chat_id'),
            config_data.get('delay'),
            config_data.get('messages'),
            config_data.get('name_prefix')
        ))
    
    conn.commit()
    conn.close()

def get_user_config(user_id):
    """User ki configuration wapis lane ke liye"""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

# Database initialize karein
if not os.path.exists(DB_NAME):
    init_db()    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id TEXT,
            name_prefix TEXT,
            delay INTEGER DEFAULT 30,
            cookies_encrypted TEXT,
            messages TEXT,
            automation_running INTEGER DEFAULT 0,
            locked_group_name TEXT,
            locked_nicknames TEXT,
            lock_enabled INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN automation_running INTEGER DEFAULT 0')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN locked_group_name TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN locked_nicknames TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE user_configs ADD COLUMN lock_enabled INTEGER DEFAULT 0')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_cookies(cookies):
    """Encrypt cookies for secure storage"""
    if not cookies:
        return None
    return cipher_suite.encrypt(cookies.encode()).decode()

def decrypt_cookies(encrypted_cookies):
    """Decrypt cookies"""
    if not encrypted_cookies:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_cookies.encode()).decode()
    except:
        return ""

def create_user(username, password):
    """Create new user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      (username, password_hash))
        user_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, messages)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, '', '', 30, ''))
        
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    """Verify user credentials using SHA-256"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[1] == hash_password(password):
        return user[0]
    return None

def get_user_config(user_id):
    """Get user configuration"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT chat_id, name_prefix, delay, cookies_encrypted, messages, automation_running
        FROM user_configs WHERE user_id = ?
    ''', (user_id,))
    
    config = cursor.fetchone()
    conn.close()
    
    if config:
        return {
            'chat_id': config[0] or '',
            'name_prefix': config[1] or '',
            'delay': config[2] or 30,
            'cookies': decrypt_cookies(config[3]),
            'messages': config[4] or '',
            'automation_running': config[5] or 0
        }
    return None

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    """Update user configuration"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    encrypted_cookies = encrypt_cookies(cookies)
    
    cursor.execute('''
        UPDATE user_configs 
        SET chat_id = ?, name_prefix = ?, delay = ?, cookies_encrypted = ?, 
            messages = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (chat_id, name_prefix, delay, encrypted_cookies, messages, user_id))
    
    conn.commit()
    conn.close()

def get_username(user_id):
    """Get username by user ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return user[0] if user else None

def set_automation_running(user_id, is_running):
    """Set automation running state for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE user_configs 
        SET automation_running = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (1 if is_running else 0, user_id))
    
    conn.commit()
    conn.close()

def get_automation_running(user_id):
    """Get automation running state for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT automation_running FROM user_configs WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return bool(result[0]) if result else False

def get_lock_config(user_id):
    """Get lock configuration for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT chat_id, locked_group_name, locked_nicknames, lock_enabled, cookies_encrypted
        FROM user_configs WHERE user_id = ?
    ''', (user_id,))
    
    config = cursor.fetchone()
    conn.close()
    
    if config:
        import json
        try:
            nicknames = json.loads(config[2]) if config[2] else {}
        except:
            nicknames = {}
        
        return {
            'chat_id': config[0] or '',
            'locked_group_name': config[1] or '',
            'locked_nicknames': nicknames,
            'lock_enabled': bool(config[3]),
            'cookies': decrypt_cookies(config[4])
        }
    return None

def update_lock_config(user_id, chat_id, locked_group_name, locked_nicknames, cookies=None):
    """Update complete lock configuration including chat_id and cookies"""
    import json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    nicknames_json = json.dumps(locked_nicknames)
    
    if cookies is not None:
        encrypted_cookies = encrypt_cookies(cookies)
        cursor.execute('''
            UPDATE user_configs 
            SET chat_id = ?, locked_group_name = ?, locked_nicknames = ?, 
                cookies_encrypted = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (chat_id, locked_group_name, nicknames_json, encrypted_cookies, user_id))
    else:
        cursor.execute('''
            UPDATE user_configs 
            SET chat_id = ?, locked_group_name = ?, locked_nicknames = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (chat_id, locked_group_name, nicknames_json, user_id))
    
    conn.commit()
    conn.close()

def set_lock_enabled(user_id, enabled):
    """Enable or disable the lock system"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE user_configs 
        SET lock_enabled = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (1 if enabled else 0, user_id))
    
    conn.commit()
    conn.close()

def get_lock_enabled(user_id):
    """Check if lock is enabled for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT lock_enabled FROM user_configs WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return bool(result[0]) if result else False

init_db()

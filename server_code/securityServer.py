# # securityserver.py

# import anvil.server
# import sqlite3
# import hashlib
# import os
# import re
# import binascii
# from datetime import datetime

# DATABASE_FILE = 'userdatabase.db'

# def generate_salt():
#     """Generate a salt for password hashing."""
#     return hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

# def hash_password(password):
#     """Hash a password for storing using PBKDF2 HMAC with SHA-512."""
#     salt = generate_salt()
#     pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
#     return (salt + binascii.hexlify(pwdhash)).decode('ascii')

# def verify_password(stored_password, provided_password):
#     """Verify a stored password against one provided by user."""
#     salt, stored_hash = stored_password[:64], stored_password[64:]
#     pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
#     return binascii.hexlify(pwdhash).decode('ascii') == stored_hash

# def is_valid_email(email):
#     """Check if email adheres to a simple regex pattern."""
#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     return re.match(pattern, email) is not None

# def is_secure_password(password):
#     """Check password for minimum security requirements."""
#     return all([
#         len(password) >= 8,
#         re.search(r'[a-z]', password),
#         re.search(r'[A-Z]', password),
#         re.search(r'\d', password),
#         re.search(r'[\W_]', password)
#     ])

# @anvil.server.callable
# def create_db():
#     """Initialize the database and create the 'users' table if not exists."""
#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             email TEXT UNIQUE NOT NULL,
#             enabled INTEGER NOT NULL DEFAULT 1,
#             last_login TEXT,
#             password_hash TEXT NOT NULL,
#             n_password_failures INTEGER NOT NULL DEFAULT 0,
#             signed_up TEXT NOT NULL
#         )
#         ''')
#         conn.commit()

# @anvil.server.callable
# def sign_up(email, password):
#     """Sign up a new user with email and password."""
#     if not is_valid_email(email) or not is_secure_password(password):
#         return "Invalid email or password does not meet security criteria."

#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         if username_exists(email, cursor):
#             return "Email already taken"

#         password_hash = hash_password(password)
#         signed_up = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         cursor.execute('''
#         INSERT INTO users (email, enabled, last_login, password_hash, n_password_failures, signed_up) 
#         VALUES (?, 1, NULL, ?, 0, ?)
#         ''', (email, password_hash, signed_up))
#         conn.commit()
#     return "User created successfully"

# @anvil.server.callable
# def login(email, password):
#     """Authenticate an existing user."""
#     user = get_user(email)
#     if user and verify_password(user[4], password):
#         update_login_success(email)
#         return "Login successful!"
#     else:
#         update_login_failure(email)
#         return "Login failed. Check your email and password."

# def username_exists(email, cursor):
#     """Check if the email already exists in the database."""
#     cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
#     return cursor.fetchone() is not None

# def get_user(email):
#     """Retrieve a user's information by their email."""
#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
#         return cursor.fetchone()

# def update_login_success(email):
#     """Update the last_login timestamp on successful login."""
#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('UPDATE users SET last_login = ?, n_password_failures = 0 WHERE email = ?', 
#                        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email))
#         conn.commit()

# def update_login_failure(email):
#     """Increment the n_password_failures counter on failed login attempt."""
#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute('UPDATE users SET n_password_failures = n_password_failures + 1 WHERE email = ?', (email,))
#         conn.commit()


import anvil.server
import sqlite3
import hashlib
import os
import re
import binascii
from datetime import datetime

DATABASE_FILE = 'userdatabase.db'

def generate_salt():
    return hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

def hash_password(password):
    salt = generate_salt()
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return (salt + binascii.hexlify(pwdhash)).decode('ascii')

def verify_password(stored_password, provided_password):
    salt, stored_hash = stored_password[:64], stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    return binascii.hexlify(pwdhash).decode('ascii') == stored_hash

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def is_secure_password(password):
    return len(password) >= 8 and re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[_@$!%*?&]", password)

@anvil.server.callable
def create_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            last_login TEXT,
            password_hash TEXT NOT NULL,
            n_password_failures INTEGER NOT NULL DEFAULT 0,
            signed_up TEXT NOT NULL
        )
        ''')
        conn.commit()

@anvil.server.callable
def sign_up(email, password):
    if not is_valid_email(email) or not is_secure_password(password):
        return "Invalid email format or password criteria not met."
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        if username_exists(email, cursor):
            return "Email already taken."
        password_hash = hash_password(password)
        signed_up = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO users (email, enabled, last_login, password_hash, n_password_failures, signed_up) VALUES (?, 1, NULL, ?, 0, ?)', (email, password_hash, signed_up))
        conn.commit()
    return "User created successfully."

@anvil.server.callable
def login(email, password):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user and verify_password(user[5], password):
            update_login_success(email, conn)
            return "Login successful."
        else:
            update_login_failure(email, conn)
            return "Login failed. Please check your email and password."

def username_exists(email, cursor):
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    return cursor.fetchone() is not None

def update_login_success(email, conn):
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET last_login = ?, n_password_failures = 0 WHERE email = ?', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email))
    conn.commit()

def update_login_failure(email, conn):
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET n_password_failures = n_password_failures + 1 WHERE email = ?', (email,))
    conn.commit()

anvil.server.wait_forever()
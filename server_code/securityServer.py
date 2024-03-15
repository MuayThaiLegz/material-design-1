# securityserver.py

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import sqlite3
import hashlib
import os
import re
import binascii
from datetime import datetime

# Database filename
DATABASE_FILE = 'userdatabase.db'

# Helper functions
def generate_salt():
    """Generate a salt for password hashing."""
    return hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

def hash_password(password):
    """Hash a password for storing using PBKDF2 HMAC with SHA-512."""
    salt = generate_salt()
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return (salt + binascii.hexlify(pwdhash)).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    salt, stored_hash = stored_password[:64], stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    return binascii.hexlify(pwdhash).decode('ascii') == stored_hash

def is_valid_email(email):
    """Check if email adheres to a simple regex pattern."""
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def is_secure_password(password):
    """Check password for minimum security requirements."""
    return all([
        len(password) >= 8,
        re.search(r'[a-z]', password),
        re.search(r'[A-Z]', password),
        re.search(r'\d', password),
        re.search(r'[\W_]', password)
    ])

# Database management functions
@anvil.server.callable
def create_db():
    """Initialize the database and create the 'users' table if not exists."""
    conn = sqlite3.connect(DATABASE_FILE)
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
    conn.close()

@anvil.server.callable
def sign_up(email, password):
    """Sign up a new user with all required attributes, allowing up to 3 attempts for valid input."""
    attempts = 0

    while attempts < 3:
        email = email
        if not is_valid_email(email):
            print("Invalid email format. Please try again.")
            attempts += 1
            continue

        password = password
        if not is_secure_password(password):
            print("Password does not meet security criteria. Please try again.")
            attempts += 1
            continue

        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        if username_exists(email, cursor):
            print("Email already taken")
            conn.close()
            return

        password_hash = hash_password(password)
        signed_up = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO users 
            (email, enabled, last_login, password_hash, n_password_failures, signed_up) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, 1, None, password_hash, 0, signed_up))
        conn.commit()
        conn.close()
        print("User created successfully")
        return

    print("Maximum attempts reached. Please try again later.")


@anvil.server.callable
def login(email, password):
    """Authenticate an existing user."""
    email = email
    password = password

    user = get_user(email)
    if user and verify_password(user[4], password):
        update_login_success(email)
        print("Login successful!")
    else:
        update_login_failure(email)
        print("Login failed. Check your email and password.")

# Utility database functions
def username_exists(email, cursor):
    """Check if the email already exists in the database."""
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    return cursor.fetchone() is not None

def get_user(email):
    """Retrieve a user's information by their email."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_login_success(email):
    """Update the last_login timestamp on successful login."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users SET last_login = ?, n_password_failures = 0 WHERE email = ?
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email))
    conn.commit()
    conn.close()

def update_login_failure(email):
    """Increment the n_password_failures counter on failed login attempt."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users SET n_password_failures = n_password_failures + 1 WHERE email = ?
    ''', (email,))
    conn.commit()
    conn.close()

# create_db()
# Uncomment the following lines to enable sign-up or login functionality
# sign_up()
# login()
                          
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

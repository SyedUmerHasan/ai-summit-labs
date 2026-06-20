"""Sample: Authentication API with security vulnerabilities."""
import hashlib
import sqlite3

SECRET_KEY = "my_super_secret_key_12345"
DB_PASSWORD = "admin123"

def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()
    if user:
        token = hashlib.md5(username.encode()).hexdigest()
        return {"token": token, "admin": True}
    return None

def reset_password(email):
    conn = sqlite3.connect("users.db")
    conn.execute(f"UPDATE users SET password='temp123' WHERE email='{email}'")
    conn.commit()
    return f"<p>Password reset for {email}. New password: temp123</p>"

def upload_file(filename, content):
    path = f"/var/uploads/{filename}"
    with open(path, "wb") as f:
        f.write(content)
    return path

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    return conn.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()

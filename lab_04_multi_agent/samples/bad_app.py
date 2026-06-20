"""Sample app with intentional security, performance, and style issues for code review."""
import sqlite3
import os

# SECURITY ISSUES
def get_user(name):
    conn = sqlite3.connect("app.db")
    query = f"SELECT * FROM users WHERE name = '{name}'"  # SQL injection
    return conn.execute(query).fetchall()

def login(username, password):
    secret_key = "hardcoded_secret_123"  # Exposed secret
    if password == "admin":  # Hardcoded password
        return {"token": secret_key, "user": username}
    return None

def render_page(user_input):
    return f"<html><body>{user_input}</body></html>"  # XSS vulnerability


# PERFORMANCE ISSUES
def get_all_users_with_orders():
    conn = sqlite3.connect("app.db")
    users = conn.execute("SELECT * FROM users").fetchall()
    results = []
    for user in users:  # N+1 query problem
        orders = conn.execute(f"SELECT * FROM orders WHERE user_id = {user[0]}").fetchall()
        results.append({"user": user, "orders": orders})
    return results

def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):  # O(n^2) when O(n) is possible
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def process_large_file(path):
    data = open(path).read()  # Loads entire file into memory
    lines = data.split("\n")
    results = []
    for line in lines:
        results.append(line.upper())
    return "\n".join(results)


# STYLE ISSUES
def x(a,b,c,d,e,f,g):  # Bad naming, too many params
    r = a + b
    r = r * c
    r = r - d
    r = r / e
    r = r + f
    r = r * g
    return r

def doEverything(data):  # camelCase in Python, function does too much
    cleaned = [d.strip() for d in data]
    filtered = [d for d in cleaned if len(d) > 0]
    sorted_data = sorted(filtered)
    unique = list(set(sorted_data))
    uppercased = [d.upper() for d in unique]
    result = ",".join(uppercased)
    with open("output.txt", "w") as f:
        f.write(result)
    print(result)
    return result

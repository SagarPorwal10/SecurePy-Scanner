"""
INTENTIONALLY VULNERABLE TEST FILE
For security testing and learning purposes only.
"""

import os
import subprocess
import sqlite3
import pickle
import yaml
import hashlib
import base64
import requests
from flask import Flask, request

app = Flask(__name__)

# ==============================
# 🔴 CRITICAL VULNERABILITIES
# ==============================

# 1. Hardcoded Secret Key
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"

# 2. Hardcoded Database Credentials
DB_PASSWORD = "SuperSecret123"

# 3. Insecure Deserialization
def unsafe_pickle(data):
    return pickle.loads(data)


# ==============================
# 🟠 HIGH SEVERITY
# ==============================

# 4. Remote Code Execution (eval)
def execute_user_code(code):
    return eval(code)

# 5. Command Injection
def list_files(user_input):
    subprocess.call("ls " + user_input, shell=True)

# 6. SQL Injection
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

# 7. Unsafe YAML Load
def unsafe_yaml(yaml_data):
    return yaml.load(yaml_data, Loader=yaml.Loader)


# ==============================
# 🟡 MEDIUM SEVERITY
# ==============================

# 8. Weak Hashing (MD5)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# 9. Path Traversal
def read_file(filename):
    with open("uploads/" + filename, "r") as f:
        return f.read()

# 10. Open Redirect
@app.route("/redirect")
def redirect_user():
    url = request.args.get("url")
    return f"<meta http-equiv='refresh' content='0; url={url}' />"

# 11. Server-Side Request Forgery (SSRF)
def fetch_url(url):
    return requests.get(url).text


# ==============================
# 🟢 LOW SEVERITY
# ==============================

# 12. Debug Mode Enabled
app.debug = True

# 13. Information Disclosure
@app.route("/env")
def show_env():
    return str(os.environ)

# 14. Base64 "Encryption"
def encode_secret(secret):
    return base64.b64encode(secret.encode()).decode()


# ==============================
# EXTRA MIXED VULNERABILITIES
# ==============================

# 15. Insecure Random Token
import random
def generate_token():
    return str(random.random())

# 16. Unvalidated File Upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save("uploads/" + file.filename)
    return "File uploaded"

# 17. Cross-Site Scripting (XSS)
@app.route("/greet")
def greet():
    name = request.args.get("name")
    return f"<h1>Hello {name}</h1>"


if __name__ == "__main__":
    app.run()

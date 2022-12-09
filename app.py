from flask import Flask, render_template, request
import sqlite3
from hashlib import pbkdf2_hmac
import requests
import json

app = Flask(__name__)


@app.route("/create")
def hello_world():
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    try:
        cur.execute("""
        CREATE TABLE Users(
        Username VARCHAR(20) NOT NULL PRIMARY KEY,
	Password VARCHAR(20) NOT NULL)
        """)
    except sqlite3.OperationalError as e:
        return str(e)
    return "table created"


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def signup():

    con = sqlite3.connect('login.db')

    encrypted_password = pbkdf2_hmac(
        'sha256', bytearray(request.form['loginPassword'], encoding='utf-8'), bytearray(request.form['loginUser'], encoding='utf-8'), 50)
    cur = con.cursor()
    cur.execute("INSERT INTO Users (Username, Password) VALUES (?,?)",
                (request.form['loginUser'], encrypted_password))
    con.commit()
    return render_template('signup_success.html'), {"Refresh": "2; url=/ "}


@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect('login.db')
    encrypted_password = pbkdf2_hmac(
        'sha256', bytearray(request.form['loginPassword'], encoding='utf-8'), bytearray(request.form['loginUser'], encoding='utf-8'), 50)
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
                (request.form['loginUser'], encrypted_password))
    match = len(cur.fetchall())
    if match == 0:
        return "Wrong username and password"
    else:
        res = requests.get("https://finnhub.io/api/v1/quote?symbol=AAPL&token=ce93rq2ad3i49a9hkpkgce93rq2ad3i49a9hkpl0")
        dict = json.loads(res.text)
        print(res)
        print(dict['c'])
        return render_template('index.html', apple_price=dict['c'])


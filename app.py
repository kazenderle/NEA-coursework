from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/create')
def create():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute(	"""	CREATE TABLE Users(
					Username VARCHAR(20) NOT NULL PRIMARY KEY,
					Password VARCHAR(20) NOT NULL
						  )
			""")
	con.commit()
	return 'CREATE'

@app.route('/')
def home():
        return render_template('login.html')

@app.route('/register')
def register():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("INSERT INTO Users (Username, Password) VALUES (?,?)",
                    (request.form['un'],request.form['pw']))
    con.commit()
    return request.form['un'] + ' added'

@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
                    (request.form['un'],request.form['pw']))
    match = len(cur.fetchall())
    if match == 0:
        return "Wrong username and password"
    else:
        return "Welcome " + request.form['un']

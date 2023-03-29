from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'tomaszogrodnikjestgruby'

mysql = mysql.connector.connect(
    host="34.159.139.65",
    user='kuba',
    password='zabki62a',
    db = 'twitter',
)

@app.route('/')
def directtologin():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
            

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    else:
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            account = cursor.fetchone()
            # account = str(account)
            if account:
                session['loggedin'] = True
                # session["id"] = account['id']
                session["username"] = username
                session["password"] = password
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect username/password!'
        return render_template('index.html', msg=msg)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    else:
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
                mysql.commit()
                msg = 'You have successfully registered!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('register.html', msg=msg)

@app.route('/home/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/profile/')
def profile():
    if 'loggedin' in session:
        username=session['username']
        password=session['password']
        cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT email FROM accounts WHERE username = %s and password = %s', (username,password,))
        email = cursor.fetchall()
        for x in range(2):
            email = email[-1]
        return render_template('profile.html', username=username, password=password, email=email,)
    else:
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session['loggedin'] = False
    session.clear()
    return redirect(url_for('login'))
# from mailbox import Message
import os
from mailjet_rest import Client
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import time

app = Flask(__name__)

app.secret_key = 'tomaszogrodnikjestgruby'
mail = Mail(app)

mysql = mysql.connector.connect(
    host="34.159.139.65",
    user='kuba',
    password='zabki62a',
    db = 'twitter',
)

mailjet = Client(auth=('d4a0e56cd58e2eb358753e75b3152d38', '0c6be36828e9b20a85888c19f17c1101'))

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
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s AND verification = 1', (username, password,))
            account = cursor.fetchone()
            # account = str(account)
            if account:
                session['loggedin'] = True
                # session["id"] = account['id']
                session["username"] = username
                session["password"] = password
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect username/password or check inbox to verification account'
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
                session["email"] = email
                session["confirmemail"] = True
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, 0)', (username, password, email,))
                mysql.commit()
                msg = 'You have successfully registered, now only confirm your email in inbox'
                data = {
                'FromEmail': 'twitter.technischools@gmail.com',
                'FromName': 'Twitter Technischools',
                'Subject': 'Twitter Technischools verification!',
                'Text-part': 'Hello, Thank you for register, confirm your account clicking link down!',
                'Html-part': '127.0.0.1:5000/confirm',
                'Recipients': [{'Email':(email)}]
                    }
            result = mailjet.send.create(data=data)
            return "Mail with verification link has sent, check your inbox"
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('register.html', msg=msg)
    
@app.route('/confirm/')
def confirm():
    if 'confirmemail' in session:
        mail = session["email"]
        mail = str(mail)
        cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET verification = 1 where email = %s', (mail,))
        mysql.commit()
        session.clear()
        return render_template('verification-confirm.html')
    else:
        return "You not have active session to confirm mail"


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
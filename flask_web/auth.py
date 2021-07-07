from flask import render_template, request, redirect, url_for
from flask_web import app, session, webserver
import re

@app.route('/')
@app.route('/login',methods=['GET', 'POST'])
def login():
    msg=""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = webserver.conn()
        cursor = conn.cursor()
        cursor.execute("select * from users where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            session['username'] = username
            session['id'] = data[0]
            return redirect(url_for("index"))
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = webserver.conn()
        cursor = conn.cursor()
        cursor.execute("select * from users where username='"+username+"' and password='" + password+"'")
        data = cursor.fetchone()
        if data:  
            msg = 'Username already exists'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers'
        
        elif not username or not password:
            msg = 'Fill out the form'
       
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password,))
            conn.commit()
            msg = 'You have successfully registered !'  
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)
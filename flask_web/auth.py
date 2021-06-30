from flask import session, Flask, render_template,request,flash,redirect,url_for
from flaskext.mysql import MySQL
from flask_web import app


@app.route('/')
@app.route('/login',methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connect().cursor()
        cursor.execute("select * from user where username='"+username+"' and password='" + password+"'")
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            session['username'] = data[0]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from user where username='"+username+"' and password='" + password+"'")
        data = cursor.fetchone()
        if data:  
            msg = 'Username already exists'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers'
        
        elif not username or not password:
            msg = 'Fill out the form'
       
        else:
            cursor.execute('INSERT INTO user VALUES (%s, %s)', (username, password,))
            conn.commit()
            msg = 'You have successfully registered !'  
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)


if __name__ == '__main__':
    app.run()

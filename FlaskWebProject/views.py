"""
Routes and views for the flask application.
"""
from flask import render_template, request, url_for, redirect, flash, session
from dbconnect import connection
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from FlaskWebProject import app

@app.route('/')
def main():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    gc.collect()
    flash("You have been logged out")
    return redirect(url_for('main'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("""SELECT * FROM users WHERE username = (%s)""", (thwart(request.form['username']),))
            
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error)  

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

@app.route('/register', methods=['GET','POST'])
def register():
    #try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("""SELECT * FROM users WHERE username = %s""",
                          (thwart(username),))

            if int(x) > 0:
                flash("The username is already taken, please choose another username")
                return render_template('register.html', form=form)

            else:
                c.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s)""",
                          (thwart(username), thwart(password), thwart(email)))
                
                conn.commit()
                flash("Thank you for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    # except Exception as e:
    #     return(str(e))
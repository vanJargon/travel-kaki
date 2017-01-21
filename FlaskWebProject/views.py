"""
Routes and views for the flask application.
"""
from flask import render_template, request, url_for, redirect, flash
from FlaskWebProject import app

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    try:
        if request.method == "POST":
		
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try again."

        return render_template("login.html", error = error)

    except Exception as e:
        return render_template("login.html", error = error)

@app.route('/register', methods=['GET','POST'])
def register():
    try:
        c, conn = connection()
        return("okay")
    except Exception as e:
        return(str(e))

    
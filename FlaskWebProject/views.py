"""
Routes and views for the flask application.
"""
from flask import render_template
from FlaskWebProject import app

@app.route('/')
def main():
    return render_template('index.html')
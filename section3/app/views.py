from flask import render_template
from app import app

@app.route('/')
def index():
    user = {'name': 'Homer Simpson'}
    return render_template('index.html', title='Simple template example', user=user)

@app.route('/fruit')
def displayFruit():
    fruits = ["Apple", "Banana", "Orange", "Kiwi"]
    return render_template("fruit_with_inheritance.html",fruits=fruits)
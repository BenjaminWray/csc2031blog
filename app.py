from flask import Flask
from config import app
from flask import render_template


@app.route('/')
def index():
    return render_template('home/index.html')


@app.route('/registration')
def registration():
    return render_template('accounts/registration.html')


if __name__ == '__main__':
    app.run()

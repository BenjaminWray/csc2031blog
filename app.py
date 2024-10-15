from flask import render_template
from config import app

@app.route('/')
def index():
    return render_template('home/index.html')

@app.errorhandler(429)
def ratelimit(e):
    return render_template("errors/error.html"), 429


if __name__ == '__main__':
    app.run()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<p>Homepage!<p>"

@app.route('/portfolios')
def about():
    return "<p>Portfolios</p>"

@app.route('/market')
def about():
    return "<p>Market!</p>"

@app.route('/about')
def about():
    return "<p>About!</p>"
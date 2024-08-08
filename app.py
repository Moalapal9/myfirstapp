from flask import Flask, render_template

app = Flask(__name__)

# index route with jinja template
@app.route('/')
def index():
    foods = ['pizza', 'burger', 'french fries']
    return render_template('index.html', foods=foods)

# user route with params
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

# error handler 404
@app.errorhandler(404)
def error_page(e):
    return render_template('error_404.html'), 404
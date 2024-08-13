from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
    
app.config['SECRET_KEY'] = 'anonymous'


# ROUTES
@app.route('/')
def index():
	users = Users.query.order_by(Users.date_added)
	return render_template('index.html', users=users)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.errorhandler(404)
def error_page(e):
    return render_template('error_404.html'), 404

@app.route('/name', methods=['GET', 'POST'])
def add_name():
	form = NamerForm()
	name = None
	address = None
	if form.validate_on_submit():
		name = form.name.data
		address = form.address.data
	flash('Add successfully!')
	return render_template('add_name.html', name=name, address=address, form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	email = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
			flash("User Added Successfully!")
		name = form.name.data
		name = form.email.data
		
	form.name.data = ''
	form.email.data = ''
	users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html", form=form, email=email, name=name, users=users)

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
	user = Users.query.get_or_404(id)
	form = UserForm()
	if request.method=='POST':
		user.name = request.form['name']
		user.email = request.form['email']
		db.session.commit()
		return redirect(url_for('add_user'))
	elif request.method=='GET':
		return render_template('update_user.html', form=form, user=user)


@app.route('/user/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
	user = Users.query.get_or_404(id)

	db.session.delete(user)
	db.session.commit()
	flash("User successfully deleted!!")

	return redirect(url_for('add_user'))


# FORM
class NamerForm(FlaskForm):
	name = StringField("Enter your name?", validators=[DataRequired()])
	address = StringField("Enter your address!", validators=[DataRequired()])
	submit = SubmitField("Enter")

class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")


# MODEL
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

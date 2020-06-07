from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
db = SQLAlchemy(app) 

from models import User 

questions = [
{
	"id": "1",
	"question": "_____ they the first customers of the day?",
	"answers": ["a) Who", "b) Were", "c) Was", "d) What"],
	"correct": "b) Were"
},
{
	"id": "2",
	"question": "Thomas can't get out of bed because he _____ his leg.",
	"answers": ["a) breakable", "b) break", "c) broke", "d) broken"],
	"correct": "c) broke" 
},
{
	"id": "3",
	"question": "You can have ice cream _____ you finish your dinner.",
	"answers": ["a) when", "b) but", "c) and", "d) or"],
	"correct": "a) when"
},
{
	"id": "4",
	"question": "I have never _____ such a boring book!",
	"answers": ["a) saw", "b) read", "c) readed", "d) red"],
	"correct": "b) read" 
},
{
	"id": "5",
	"question": "Success in this examination depends _____ hard work alone.",
	"answers": ["a) at", "b) on", "c) for", "d) over"],
	"correct": "b) on" 
},
{
	"id": "6",
	"question": "Rohan and Rohit are twin brothers, but they do not look _____.",
	"answers": ["a) unique", "b) different", "c) alike", "d) likely"],
	"correct": "c) alike"
},
{
	"id": "7",
	"question": "The four sides of a room that hold up the ceiling.",
	"answers": ["a) land", "b) soil", "c) ribbon", "d) wall"],
	"correct": "d) wall"
},
{
	"id": "8",
	"question": "Discover:",
	"answers": ["a) To drive fast", "b) To find unexpectedly", "c) To dream", "d) To start something"],
	"correct": "b) To find unexpectedly"
},
{
	"id": "9",
	"question": "In which of the following places do people 'deposit' money?",
	"answers": ["a) with a friend", "b) at a store", "c) at work", "d) at a bank"],
	"correct": "d) at a bank"
},
{
	"id": "10",
	"question": "Which of the following best describes a 'wealthy' person?",
	"answers": ["a) an accountant", "b) a millionaire", "c) a teacher", "d) a cashier"],
	"correct": "b) a millionaire"
} 
]


@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'khushibarjatia@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home')) 
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/quiz", methods=['POST', 'GET']) 
def quiz():
	if request.method == 'GET':
		return render_template('quiz.html', data=questions, title='Quiz') 
	else:
		result = 0
		total = 0
		for question in questions:
			if request.form[question.get('id')] == question.get('correct'):
				result += 1
			total += 1
		return render_template('quiz_results.html', total=total, result=result, title='Quiz')


    

if __name__ == '__main__':
    app.run(debug=True)
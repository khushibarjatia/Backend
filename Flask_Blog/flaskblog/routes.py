import os
import secrets
from PIL import Image 
from flask import render_template, request, url_for, flash, redirect
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            RequestResetForm, ResetPasswordForm) 
from flaskblog.models import User 
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

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


questions_1 = [ 
{
    "id_1": "1",
    "question_1": "Select the antonym for the word 'Light':",
    "answers_1": ["a) Dark", "b) Hard", "c) Bright", "d) Shine"],
    "correct_1": "a) Dark"
},
{
    "id_1": "2",
    "question_1": "Rhyming word of 'try':",
    "answers_1": ["a) tree", "b) grey", "c) fry", "d) wheel"],
    "correct_1": "c) fry"
},
{
    "id_1": "3",
    "question_1": "Where are you going?",
    "answers_1": ["a) I am going to Johns house.", "b) I going at work.", "c) I are going to the store.", "d) I am going to the store."],
    "correct_1": "d) I am going to the store."
},
{
    "id_1": "4",
    "question_1": "He was invited, ____ he did not come.",
    "answers_1": ["a) if", "b) when", "c) but", "d) while"],
    "correct_1": "c) but"
},
{
    "id_1": "5",
    "question_1": "Paul can't touch the ceiling because he is too _____",
    "answers_1": ["a) shortening", "b) shortness", "c) shortly", "d) short"],
    "correct_1": "d) short"
},
{
    "id_1": "6",
    "question_1": "They ______ the pyramids when they went to Egypt.",
    "answers_1": ["a) didn't see", "b) seed", "c) did not saw", "d) not see"],
    "correct_1": "a) didn't see"
},
{
    "id_1": "7",
    "question_1": "Did you ____ to that restaurant?",
    "answers_1": ["a) been", "b) go", "c) going", "d) ate"],
    "correct_1": "b) go"
},
{
    "id_1": "8",
    "question_1": "I will talk ____ Susan when I see her.",
    "answers_1": ["a) in", "b) at", "c) to", "d) with"],
    "correct_1": "c) to"
},
{
    "id_1": "9",
    "question_1": "Edward has always _____ things very quickly and efficiently.",
    "answers_1": ["a) does", "b) done", "c) did", "d) do"],
    "correct_1": "b) done"
},
{
    "id_1": "10",
    "question_1": "This shirt ____ mine.",
    "answers_1": ["a) is", "b) are", "c) of", "d) wear"],
    "correct_1": "a) is"
},
{
    "id_1": "11",
    "question_1": "Never look directly ____ the sun. It is bad for your eyes.",
    "answers_1": ["a) under", "b) to", "c) through", "d) at"],
    "correct_1": "d) at"
},
{
    "id_1": "12",
    "question_1": "She _____ a dress to the party last night.",
    "answers_1": ["a) worn", "b) wear", "c) wore", "d) weared"],
    "correct_1": "c) wore"
},
{
    "id_1": "13",
    "question_1": "_____ he understand what you were talking about?",
    "answers_1": ["a) Would", "b) Did", "c) Was", "d) Were"],
    "correct_1": "b) Did"
},
{
    "id_1": "14",
    "question_1": "My sister ____ play tennis now.",
    "answers_1": ["a) can", "b) is", "c) was", "d) to"],
    "correct_1": "a) can"
},
{
    "id_1": "15",
    "question_1": "Plural form of knife:",
    "answers_1": ["a) knifes", "b) knives", "c) knive", "d) knifess"],
    "correct_1": "b) knives"
}

]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() 
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login')) 
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/quiz", methods=['POST', 'GET'])
@login_required 
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


@app.route("/features", methods=['GET', 'POST'])
@login_required
def features():
    return render_template('features.html')


@app.route("/analyze_yourself", methods=['GET', 'POST'])
@login_required
def analyze_yourself():
    if request.method == 'GET':
        return render_template('analyze_yourself.html', data_1=questions_1, title='Analyze Yorself')
    else:
        result_1 = 0
        total_1 = 0
        for question_1 in questions_1:
            if request.form[question_1.get('id_1')] == question_1.get('correct_1'):
                result_1 += 1
            total_1 += 1 
        return render_template('analyze_yourself_results.html', total_1=total_1, result_1=result_1, title='Analyze Yorself')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home')) 


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size) 
    i.save(picture_path) 

    return picture_fn


@app.route("/account", methods=['GET', 'POST']) 
@login_required 
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) 
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() 
        flash('Your account has been updated!', 'success') 
        return redirect(url_for('account')) 
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form) 


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
        sender='khushibarjatia@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)} 

If you did not make this request, then simply ignore this email and no changes will be made.
''' 
    mail.send(msg) 



@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login')) 
    return render_template('reset_request.html', title='Reset Password', form=form)



@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token) 
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request')) 
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit() 
        flash('Your password has been updated! You are now able to log in!', 'success')
        return redirect(url_for('login')) 
    return render_template('reset_token.html', title='Reset Password', form=form)






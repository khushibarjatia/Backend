import os
import secrets
from PIL import Image 
from flask import render_template, request, url_for, flash, redirect, jsonify
from flaskblog import app, db, bcrypt
from flaskblog.models import User 
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
#from operator import itemgetter 

questions = [
{
    "id": "1",
    "question": "_____ they the first customers of the day?",
    "answers": ["Who", "Were", "Was", "What"],
    "correct": "Were" 
},
{
    "id": "2",
    "question": "Thomas can't get out of bed because he _____ his leg.",
    "answers": ["breakable", "break", "broke", "broken"],
    "correct": "broke" 
},
{
    "id": "3",
    "question": "You can have ice cream _____ you finish your dinner.",
    "answers": ["when", "but", "and", "or"],
    "correct": "when"
},
{
    "id": "4",
    "question": "I have never _____ such a boring book!",
    "answers": ["saw", "read", "readed", "red"],
    "correct": "read" 
},
{
    "id": "5",
    "question": "Success in this examination depends _____ hard work alone.",
    "answers": ["at", "on", "for", "over"],
    "correct": "on" 
},
{
    "id": "6",
    "question": "Rohan and Rohit are twin brothers, but they do not look _____.",
    "answers": ["unique", "different", "alike", "likely"],
    "correct": "alike"
},
{
    "id": "7",
    "question": "The four sides of a room that hold up the ceiling.",
    "answers": ["land", "soil", "ribbon", "wall"],
    "correct": "wall"
},
{
    "id": "8",
    "question": "Discover:",
    "answers": ["To drive fast", "To find unexpectedly", "To dream", "To start something"],
    "correct": "To find unexpectedly"
},
{
    "id": "9",
    "question": "In which of the following places do people 'deposit' money?",
    "answers": ["with a friend", "at a store", "at work", "at a bank"],
    "correct": "at a bank"
},
{
    "id": "10",
    "question": "Which of the following best describes a 'wealthy' person?",
    "answers": ["an accountant", "a millionaire", "a teacher", "a cashier"],
    "correct": "a millionaire"
} 
]


questions_1 = [ 
{
    "id_1": "1",
    "question_1": "Select the antonym for the word 'Light':",
    "answers_1": ["Dark", "Hard", "Bright", "Shine"],
    "correct_1": "Dark"
},
{
    "id_1": "2",
    "question_1": "Rhyming word of 'try':",
    "answers_1": ["tree", "grey", "fry", "wheel"],
    "correct_1": "fry"
},
{
    "id_1": "3",
    "question_1": "Where are you going?",
    "answers_1": ["I am going to Johns house.", "I going at work.", "I are going to the store.", "I am going to the store."],
    "correct_1": "I am going to the store."
},
{
    "id_1": "4",
    "question_1": "He was invited, ____ he did not come.",
    "answers_1": ["if", "when", "but", "while"],
    "correct_1": "but"
},
{
    "id_1": "5",
    "question_1": "Paul can't touch the ceiling because he is too _____",
    "answers_1": ["shortening", "shortness", "shortly", "short"],
    "correct_1": "short"
},
{
    "id_1": "6",
    "question_1": "They ______ the pyramids when they went to Egypt.",
    "answers_1": ["didn't see", "seed", "did not saw", "not see"],
    "correct_1": "didn't see"
},
{
    "id_1": "7",
    "question_1": "Did you ____ to that restaurant?",
    "answers_1": ["been", "go", "going", "ate"],
    "correct_1": "go"
},
{
    "id_1": "8",
    "question_1": "I will talk ____ Susan when I see her.",
    "answers_1": ["in", "at", "to", "with"],
    "correct_1": "to"
},
{
    "id_1": "9",
    "question_1": "Edward has always _____ things very quickly and efficiently.",
    "answers_1": ["does", "done", "did", "do"],
    "correct_1": "done"
},
{
    "id_1": "10",
    "question_1": "This shirt ____ mine.",
    "answers_1": ["is", "are", "of", "wear"],
    "correct_1": "is"
},
{
    "id_1": "11",
    "question_1": "Never look directly ____ the sun. It is bad for your eyes.",
    "answers_1": ["under", "to", "through", "at"],
    "correct_1": "at"
},
{
    "id_1": "12",
    "question_1": "She _____ a dress to the party last night.",
    "answers_1": ["worn", "wear", "wore", "weared"],
    "correct_1": "wore"
},
{
    "id_1": "13",
    "question_1": "_____ he understand what you were talking about?",
    "answers_1": ["Would", "Did", "Was", "Were"],
    "correct_1": "Did"
},
{
    "id_1": "14",
    "question_1": "My sister ____ play tennis now.",
    "answers_1": ["can", "is", "was", "to"],
    "correct_1": "can"
},
{
    "id_1": "15",
    "question_1": "Plural form of knife:",
    "answers_1": ["knifes", "knives", "knive", "knifess"],
    "correct_1": "knives"
}
]

words = [
{
    "word_id": "1",
    "word": "NONPLUSSED:",
    "meaning": "Filled with bewilderment"
},
{
    "word_id": "2",
    "word": "INCHOATE:",
    "meaning": "Only partly in existence; imperfectly formed"
},
{
    "word_id": "3",
    "word": "MARTINET:",
    "meaning": "Someone who demands complete obedience; a strict disciplinarian."
},
{
    "word_id": "4",
    "word": "HOI POLLOI:",
    "meaning": "Common people"
},
{
    "word_id": "5",
    "word": "ABJECT:",
    "meaning": "Completely without pride or dignity."
},
{
    "word_id": "6",
    "word": "ABERRATION:",
    "meaning": "A state or condition markedly different from the norm."
},
{
    "word_id": "7",
    "word": "ABJURE:",
    "meaning": "Formally reject a formerly held belief."
},
{
    "word_id": "8",
    "word": "ABROGATE:",
    "meaning": "revoke formally"
},
{
    "word_id": "9",
    "word": "ABSCOND:",
    "meaning": "Run away; often taking something or somebody along"
},
{
    "word_id": "10",
    "word": "ABSTRUSE:",
    "meaning": "Difficult to understand"
},
{
    "word_id": "11",
    "word": "ALACRITY:",
    "meaning": "Liveliness and eagerness"
},
{
    "word_id": "12",
    "word": "ALIAS:",
    "meaning": "A name that has been assumed temporarily."
},
{
    "word_id": "13",
    "word": "ANACHRONISTIC:",
    "meaning": "Chronologically misplaced"
},
{
    "word_id": "14",
    "word": "ANATHEMA:",
    "meaning": "A formal eccelesiastical curse accompanied by excommunication."
},
{
    "word_id": "15",
    "word": "ANNEX:",
    "meaning": "Attach to"
},
{
    "word_id": "16",
    "word": "ANTEDILUVIUM:",
    "meaning": "Of or relating to the period before the biblical flood."
},
{
    "word_id": "17",
    "word": "APATHETIC:",
    "meaning": "Showing little or no emotion"
},
{
    "word_id": "18",
    "word": "ANTITHESIS:",
    "meaning": "Exact opposite"
},
{
    "word_id": "19",
    "word": "APOCRYPHAL:",
    "meaning": "Of doubtful authenticity"
},
{
    "word_id": "20",
    "word": "CACHET AND PANACHE:",
    "meaning": "An indication of approved or superior status; distinctive and stylish respectively, CACHET is more about prestige and PANACHE is more about style."
},
{
    "word_id": "21",
    "word": "INDEFATIGABLE:",
    "meaning": "Showing sustained enthusiastic action with unflagging vitality."
},
{
    "word_id": "22",
    "word": "UNCANNY:",
    "meaning": "Surpassing the ordinary or normal."
},
{
    "word_id": "23",
    "word": "UNABASHED:",
    "meaning": "Not embarrased"
},
{
    "word_id": "24",
    "word": "DILATORY:",
    "meaning": "Wasting time"
},
{
    "word_id": "25",
    "word": "ACCOST:",
    "meaning": "Approach and speak to someone aggressively"
},
{
    "word_id": "26",
    "word": "ACCRETION:",
    "meaning": "An increase by natural growth or addition"
},
{
    "word_id": "27",
    "word": "ACUMEN:",
    "meaning": "Shrewdness shown by keen insight"
},
{
    "word_id": "28",
    "word": "ADAMANT:",
    "meaning": "very sure; refusing to change one's mind"
},
{
    "word_id": "29",
    "word": "ADMONISH:",
    "meaning": "Scold or reprimand; take to task"
},
{
    "word_id": "30",
    "word": "ADUMBRATE:",
    "meaning": "Describe roughly or give the main points or summary"
},
{
    "word_id": "31",
    "word": "AFFLUENT:",
    "meaning": "Having an abundant supply of money or possessions of value."
},
{
    "word_id": "32",
    "word": "AGGRANDIZE:",
    "meaning": "Increase the scope, power or importance of"
},
{
    "word_id": "33",
    "word": "AMBIVALENT:",
    "meaning": "Uncertain or unable to decide about what course to follow."
},
{
    "word_id": "34",
    "word": "AMENABLE:",
    "meaning": "Disposed or willing to comply"
},
{
    "word_id": "35",
    "word": "ARROGATE:",
    "meaning": "Seize and take control without authority."
},
{
    "word_id": "36",
    "word": "ASCETIC:",
    "meaning": "Someone who practices self denial as a spiritual discipline."
}
]

basic = [
{
    "basic_id": "1", 
    "basic_link": "https://perfectlyspoken.com/"
},
{
    "basic_id": "2",
    "basic_link": "https://alison.com/course/speaking-and-writing-english-effectively"
},
{
    "basic_id": "3",
    "basic_link": "https://www.talkenglish.com/"
},
{
    "basic_id": "4",
    "basic_link": "https://www.oxfordonlineenglish.com/free-spoken-english-lessons"
}
]


advanced = [
{
    "advanced_id": "1",
    "advanced_link": "https://www.britishcouncil.in/english/online/classes/myenglish"
},
{
    "advanced_id": "2",
    "advanced_link": "https://www.edx.org/learn/english" 
},
{
    "advanced_id": "3",
    "advanced_link": "https://perfectlyspoken.com/english-courses/c1/"
}
]

books =[
{
    "book_id": "1",
    "book_link": "https://www.learnenglishteam.com/great-books-to-improve-your-english/"
},
{
    "book_id": "2",
    "book_link": "https://www.learnenglishteam.com/formal-and-informal-english/"
},
{
    "book_id": "3",
    "book_link": "https://www.bloomsbury-international.com/student-ezone/e-book/"
},
{
    "book_id": "4",
    "book_link": "https://www.pdfdrive.com/english-books.html"
},
{
    "book_id": "5",
    "book_link": "https://www.easypacelearning.com/english-books/english-books-for-download-pdf"
}
]


@app.route("/register", methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email') 
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password') 
    msg = ""
    if not username or not password or not email:
        msg = {"status": {"type": "failure", "message": "Missing Data!"}} 
        return jsonify(msg)

    if confirm_password != password:
        msg ={"status": {"type": "failure", "message": "Please make sure your passwords match."}}
        return jsonify(msg) 

    if User.query.filter_by(username=username).count() == 1:
        msg = {"status": {"type": "failure", "message": "Username already taken!"}}
        return jsonify(msg)

    if User.query.filter_by(email=email).count() == 1:
        msg = {"status": {"type": "failure", "message": "Email already taken!"}}
        return jsonify(msg) 

    u = User()
    u.username = username
    u.email = email
    u.set_password(password)
    db.session.add(u)
    db.session.commit(u)

    msg = {"status": {"type": "success", "message": "You have registered successfully!"}}
    return jsonify(msg) 


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    msg = ""
    if not username or not password:
        msg = {"status": {"type": "failure", "message": "Missing Data!"}} 
        return jsonify(msg) 

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_passsword(password):
        msg = {"status": {"type": "failure", "message": "Username or password incorrect!"}} 
    else:
        msg = {"status": {"type": "success", "message": "Logged in Successfully!"},
               "data": {"user": user.getJsonData()} 
        } 
    return jsonify(msg) 


@app.route("/quiz", methods=['POST', 'GET'])
def quiz():
    a = {d['question']: d['answers'] for d in questions} 
    return jsonify(a) 


@app.route("/quiz_results", methods=['POST', 'GET']) 
def quiz_results():
    result = []  
    request_data = request.get_json()
    question = request_data['question'] 
    for question in questions:
        if request.form[question.get('question')] == question.get('correct'):
            result.append(id) 
            
    return jsonify(len(result)) 


@app.route("/analyze_yourself", methods=['GET', 'POST'])
def analyze_yourself():
    b = {d['question_1']: d['answers_1'] for d in questions_1} 
    return jsonify(b) 

    
@app.route("/analyze_yourself_results", methods=['GET', 'POST'])
def analyze_yourself_results():
    result_1 = []
    request_data = request.get_json()
    id_1 = request_data['id_1']  
    for question_1 in questions_1:
        if request.form[question_1.get('id_1')] == question_1.get('correct_1'):
            result_1.append(id_1)
    return jsonify(result_1)  

 

#@app.route("/word", methods=['GET', 'POST'])
#def word_of_the_day():
 #   c = {i['word']: i['meaning'] for i in words}
  #  for key, value in c.items():
   #     return f'''Word: {key}
    #    Meaning: {value} 
#''' 
        


    #return jsonify(words)   

#@app.route("/test", methods=['GET', 'POST'])
#scheduler.start() 
#def testing():
 #   return "Hi" 
#job = scheduler.add_job(testing, 'interval', seconds=2) 
 
@app.route("/test1", methods=['GET', 'POST'])
def testing1():
    return jsonify(words[2]) 



@app.route("/test", methods=['GET', 'POST'])
def testing():
    i = 0
    while i<=35:
        return jsonify(words[i]) 
        i = i + 1
    



@app.route("/basic", methods=['GET', 'POST'])
def display_basic():
    b = {d['basic_id']: d['basic_link'] for d in basic} 
    return jsonify(b)


@app.route("/advanced", methods=['GET', 'POST'])
def display_adv():
    b = {d['advanced_id']: d['advanced_link'] for d in advanced} 
    return jsonify(b)


@app.route("/book", methods=['GET', 'POST'])
def display():
    b = {d['book_id']: d['book_link'] for d in books} 
    return jsonify(b) 


@app.route("/logout")
@login_required
def logout():
    logout_user()
 


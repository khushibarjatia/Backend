import os
import secrets
from PIL import Image 
from flask import render_template, request, url_for, flash, redirect, jsonify
from flaskblog import app, db, bcrypt
from flaskblog.models import User 
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

questions = [
{
    "id": "1",
    "question": "_____ they the first customers of the day?",
    "answers": ["a) Who", "b) Were", "c) Was", "d) What"],
    "correct": "Were" 
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
    "advanced_link": "https://www.talkenglish.com/" 
},
{
    "advanced_id": "3",
    "advanced_link": "https://perfectlyspoken.com/"
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
    return jsonify(questions)    


@app.route("/quiz_results", methods=['POST', 'GET'])
@login_required 
def quiz_results():
    result = []  
    request_data = request.get_json()
    id = request_data['id'] 
    for question in questions:
        if request.form[question.get('id')] == question.get('correct'):
            result.append(id)  
    return jsonify(result)  


@app.route("/analyze_yourself", methods=['GET', 'POST'])
@login_required
def analyze_yourself():
    return jsonify({'questions_1': questions_1}) 


@app.route("/analyze_yourself_results", methods=['GET', 'POST'])
@login_required
def analyze_yourself_results():
    result_1 = []
    request_data = request.get_json()
    id_1 = request_data['id_1']  
    for question_1 in questions_1:
        if request.form[question_1.get('id_1')] == question_1.get('correct_1'):
            result_1.append(id_1)
    return jsonify(result_1)  


@app.route("/word", methods=['GET', 'POST'])
@login_required
def word_of_the_day():
    return jsonify({'words': words})   


@app.route("/basic", methods=['GET', 'POST'])
@login_required
def basic():
    return jsonify({'basic': basic})


@app.route("/advanced", methods=['GET', 'POST'])
@login_required
def advanced():
    return jsonify({'advanced': advanced})


@app.route("/books", methods=['GET', 'POST'])
def books():
    return jsonify({'books': books}) 


@app.route("/logout")
@login_required
def logout():
    logout_user()
 


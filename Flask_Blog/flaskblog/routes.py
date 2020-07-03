import os
import secrets
from PIL import Image 
from flask import render_template, request, url_for, flash, redirect, jsonify
from flaskblog import app, db, bcrypt, sched
from flaskblog.models import User 
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
#from operator import itemgetter 
import time
import random


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
    "basic_desc": "300 free video lessons from professional teachers! Free quizzes included!",
    "basic_link": "https://perfectlyspoken.com/"
},
{
    "basic_desc": "Duration: 2-3 hours, Ratings: 3.8, Enrolled students: Over 3.3 Lakh, Certification and Assessment included!",
    "basic_link": "https://alison.com/course/speaking-and-writing-english-effectively"
},
{
    "basic_desc": "The lessons here are structured to give you practice in reading, speaking and listening at the same time!",
    "basic_link": "https://www.talkenglish.com/"
},
{
    "basic_desc": "Learn to speak English with confidence in this lesson. Do you feel shy or nervous speaking English? Learn to sound and feel more confident in your English!",
    "basic_link": "https://www.oxfordonlineenglish.com/free-spoken-english-lessons"
}
]


advanced = [
{
    "advanced_desc": "This course has videos, mobile apps, games, stories, listening activities and grammar exercises for adults, teenagers and children! ",
    "advanced_link": "https://www.britishcouncil.me/en/english/learn-online"
},
{
    "advanced_desc": "Learn effective English communication skills with online classes and courses from Tsinghua, ASU, HKPolyU and other top schools!",
    "advanced_link": "https://www.edx.org/learn/english" 
},
{
    "advanced_desc": "Develop your English language skills so you can communicate fluently, flexibly and effectively and build a vocabulary of about 8,000 words. This course is designed to take your English skills to the next level with high quality video lessons and more!",
    "advanced_link": "https://perfectlyspoken.com/english-courses/c1/"
}
]

more_about_english =[
{
    "more_desc": "This includes five English Grammar books. If you are a beginner or advanced level English learner, these books will help you improve your English better than ever!",
    "more_link": "https://www.learnenglishteam.com/great-books-to-improve-your-english/"
},
{
    "more_desc": "Best way to start your initiative towards learning English! Includes examples of Formal and Informal English!",
    "more_link": "https://www.learnenglishteam.com/formal-and-informal-english/"
},
{
    "more_desc": "This offers a fantastic selection of free book downloads to help improve your English reading, grammar and vocabulary. Their printable books also include fun quizzes!",
    "more_link": "https://www.bloomsbury-international.com/student-ezone/e-book/"
},
{
    "more_desc": "This is your search engine for PDF files. As of today, they have 8 Crore eBooks for you to download for free. No annoying ads, no download limits, enjoy it now!",
    "more_link": "https://www.pdfdrive.com/english-books.html"
},
{
    "more_desc": "This includes a huge variety of books ranging from Phrasal verbs to English grammar to Voice and Accent Training and a lot more!",
    "more_link": "https://www.easypacelearning.com/english-books/english-books-for-download-pdf"
}
]


books = [
{
    "book_desc": "Young Readers Books",
    "book_link": "https://manybooks.net/search-book?field_genre%5B14%5D=14"
},
{
    "book_desc": "Action and Adventure Books",
    "book_link": "https://manybooks.net/search-book?field_genre%5B10%5D=10"
},
{
    "book_desc": "Mystery and Thriller Books",
    "book_link": "https://manybooks.net/search-book?field_genre%5B19%5D=19&field_genre%5B66%5D=66"
},
{
    "book_desc": "Science Fiction Books",
    "book_link": "https://manybooks.net/search-book?field_genre%5B26%5D=26"
},
{
    "book_desc": "Horror Books",
    "book_link": "https://manybooks.net/search-book?field_genre%5B18%5D=18"
},
{
    "book_desc": "Biographies and History Books",
    "book_link": "https://manybooks.net/search-book?field_genre%5B32%5D=32&field_genre%5B12%5D=12"
}
]




@app.route("/register", methods=['GET', 'POST']) 
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email'] 
        password = request.form['password']
        confirm_password = request.form['confirm_password']  
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
    if request.method == "POST":
        username = request.form('username')
        password = request.form('password')
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
            result.append(question)  
    return jsonify(result)  


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
 
@app.route("/test1", methods=['GET'])
def testing1():
    return "hi" 
sched.add_job(testing1, trigger='interval', seconds=3)
sched.start() 


@app.route("/test", methods=['GET', 'POST'])
def testing():
    chosen = random.choice(words)
    return jsonify(chosen) 


@app.route("/basic", methods=['GET', 'POST'])
def display_basic():
    b = {d['basic_link']: d['basic_desc'] for d in basic} 
    return jsonify(b)


@app.route("/advanced", methods=['GET', 'POST'])
def display_adv():
    b = {d['advanced_link']: d['advanced_desc'] for d in advanced} 
    return jsonify(b)


@app.route("/book", methods=['GET', 'POST'])
def display_books():
    b = {d['book_link']: d['book_desc'] for d in books} 
    return jsonify(b) 



@app.route("/more", methods=['GET', 'POST'])
def display_more():
    b = {d['more_link']: d['more_desc'] for d in more_about_english} 
    return jsonify(b) 



@app.route("/logout")
@login_required
def logout():
    logout_user()
 


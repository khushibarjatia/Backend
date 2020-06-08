from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
db = SQLAlchemy(app) 

from models import User 

q1 = """ Select the antonym for word light:
   a.Heavy
   b.hard
   c.tendy
   d.brighter"""
q2 = """Rhyming word for try:
   a.tree
   b.grey
   c.fry
   d.whee"""
q3 = """ Were there any beers in the refrigerator?
   a.Yes,there will be a few.
   b.Thereare a little.
   c.There was not even one.
   d.There have been some.
   e.There were a little."""
q4 = """Where are my car keys?
      They are _ _ _ _your hands!
   a.on
   b.to
   c.of
   d.in"""
q5 = """Whose keys are these?
      _ _ _ _are mine.
   a.They
   b.These 
   c.It
   d.whose
   e.keys"""
q6 = """_ _ _ the war ,most Italians were farmers.
   a.To
   b.From
   c.While
   d.Before
   e.When"""
q7 ="""who is your mother's sister's daughter?
      _ _ _ _ .
   a.She is my wife.
   b.She is my mother's nephew.
   c.She  my cousin.
   d.Is my mother's niece.
   e.My mother's sister's daughter is my cousin."""
q8 ="""Paul can't touch ceiling because he is too _ _ _.
   a.shortening
   b.shortness
   c.shorten
   d.shortly
   e.short."""
q9 =""" Is there a doctor in the house?
    _ _ _ _.
   a.Yes,is there.
   b.No,isn't.
   c.Yes,there is.
   d.No,they isn't
   e.No ,theirs not."""
q10 =""" We must _ _ _ _ the train at the next stop.
   a.get off
   b.get over
   c.get on
   d.get down
   e.get up"""
q11 = """Put your arms _ _ _ _ me and kiss me you fool!
   a.beyond
   b.around
   c.to
   d.onto
   e.on"""
q12 = """English grammmer is the worst grammmer of  any language.
       No,it isn't.German grammer _ _ _ .
   a.worse is.
   b.is worst.
   c.is bladder.
   d.is worse."""
q13 = """ Is that boy Mary's son? _ _ _.
   a.Yes,name is Robert.
   b.Yes,he is.
   c.No,he is Marys nephew.
   d.Yes,he are."""
q14 = """ Where are you going?
   a.I am going to Johns house.
   b.I going at work.
   c.I are going the store.
   d.I am going to my mother's house."""
q15 = """ He was invited_ _ _ _ he did not come.
   a.if
   b.when
   c.or
   d.but
   e.while."""
q16 = """ They _ _ _ _ the pyramids when went to Egypt.
   a.didn't see.
   b.seed
   c.did not saw
   d.not see
   e.not seen"""
q17 = """ Have you ever _ _ _ in that restaurant?
   a.eat
   b.going
   c.ate 
   d.went
   e.eaten."""
q18 =""" I will speak _ _ _ Suzanne when I see her.
   a. in
   b.to
   c.around
   d.at
   e.toward"""
q19 = """ Edward has always _ _ _ things very quickly and efficiently.
   a.does
   b.done 
   c..did
   d.do"""
q20 = """Neha been working there _ _ _  only eight months.
   a.in
   b.by
   c.for
   d.since
   e.from."""
q21 =""" The police went_ _ _ _ all of Karl's things, but they didn't find any guns.
   a.under
   b.past
   c.through
   d.in
   e.across."""
q22 = """These pants _ _ _ mine;that jackets is yours.
   a.of
   b.are wearing
   c.are
   d.is wearing
   e.is."""
q23 =""" Never look directly _ _ _ the sun.It is bad for your eyes
   a.to
   b.for
   c.through
   d.of
   e.at"""
q24 ="""You can use my car _ _ _  tomorrow.
   a.yet
   b.since
   c.until
   d.around
   e.in"""
q25 ="""She _ _ _ blue velvet to the party last night.
   a.worn
   b.war
   c.weared
   d.wear
   e.wore"""
q26 = """_ _  _he understand what you were talking about?
   a.could
   b.cans
   c.can't
   d.does"""
q27 ="""My sister _ _ _play tennis now.
   a.can to
   b.can
   c.will can"""
q28 = """I _ _ _ walk when I was less than a year old.
   a.can
   b.could
   c.have can"""
q29 = """(polite)_ _ _ you tell me what time it is ,please?
   a.could
   b.can
   c.will"""
questions ={q1:"a",q2:"c",q3:"e",q4:"d",q5:"a",q6:"d",q7:"e",q8:"e",q9:"c",q10:"a",q11:"b",q12:"d",q13:"b",q14:"d",q15:"d",q16:"a",
            q17:"e",q18:"b",q19:"b",q20:"c",q21:"c",q22:"c",q23:"e",q24:"c",q25:"e",q26:"a",q27:"b",q28:"b",q29:"c"
            }

score = 0
for i in questions:
    print(i)
    flag1 =input("Do you want to skip this question? Y/N")
    if flag1=="Y":
       continue
    ans = input("Enter the answer:")
    if ans==questions[i]:
        print("correct answer,you got 1 point")
        score = score+1
    else:
        print("wrong answer,you lost 1 point")
        score =score-1
    flag2 =input("Do you want to quit ? Y/N")
    if flag2 =="y":
       break
print("Final score is:" ,score)

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

from flask import Flask, render_template, session, request
import random
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class ScoreBoard(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ign = db.Column(db.String(5), nullable=False)
	sc = db.Column(db.Integer, nullable=False, default=0)

	def __repr__(self):
		return 'ScoreBoard: ' + str(self.id)

words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'donec', 'tempus', 'commodo', 'nisl', 'eget', 'pellentesque', 'sed', 'nec', 'nunc', 'eget', 'leo', 'iaculis', 'malesuada', 'pellentesque', 'interdum', 'convallis', 'suscipit', 'morbi', 'vitae', 'ullamcorper', 'purus', 'eget', 'interdum', 'odio', 'ut', 'suscipit', 'felis', 'scelerisque', 'faucibus', 'aliquam', 'dui', 'nunc', 'suscipit', 'risus', 'nec', 'tincidunt', 'dui', 'nibh', 'quis', 'est', 'vestibulum', 'laoreet', 'quis', 'urna', 'nec', 'tempor', 'sed', 'maximus', 'interdum', 'risus', 'nec', 'facilisis']

def calc(og_text, td_text, ign):
    count = 0
    td_list = td_text.split(" ")
    for n in range(len(td_list)):
        if og_text[n] == td_list[n]:
            count += 1
    
    calc1 = (count/15) * 60
    if calc1 != 0:
        new_post = ScoreBoard(ign=ign, sc=calc1)
        db.session.add(new_post)
        db.session.commit()
    str1 = '<strong>Score:</strong> ' + str(calc1) + ' <strong>Right:</strong> ' + str(count) + ' <strong>Wrong:</strong> ' + str(len(td_list) - count)
    return str1

class NameForm(Form):
	i1 = StringField('Enter your ID:', [DataRequired(message="Enter Your Name Please"), Length(min=4, max=5)])

class TypeForm(Form):
	t1 = StringField('Typed Text:', [DataRequired(message="Start Typing"), Length(min=0, max=415)])

def set_vars():
    session['set_word'] = sorted(words, key=lambda k: random.random())
    session['set_state'] = 0
    session['set_ign'] = ''
    session['set_typed'] = ''

@app.route('/', methods=['GET', 'POST'])
def hi():
    name_form = NameForm(request.form)
    type_form = TypeForm(request.form)
    if request.method == 'GET' and session.get('set_state') == None:
        set_vars()
        return render_template('mm.html', name_form=name_form)
    
    elif request.method == 'POST' and session.get('set_state') == 0:
        session['set_state'] = 1
        session['set_ign'] = request.form['i1']
        return render_template('mm.html', type_form=type_form)
    
    elif request.method == 'POST' and session.get('set_state') == 1 and request.form['t1'] != None:
        session['set_state'] = 2
        session['set_typed'] = request.form['t1']
        cr_count = calc(session['set_word'], session['set_typed'], session['set_ign'])
        all_scores = ScoreBoard.query.order_by(desc(ScoreBoard.sc)).limit(10)
        return render_template('mm.html', cr_count=cr_count, scores=all_scores)

    else:
        set_vars()
        return render_template('mm.html', value=session['set_word'], name_form=name_form)

@app.errorhandler(400)
def page_not_found(e):
    name_form = NameForm(request.form)
    set_vars()
    return render_template('mm.html', value=session['set_word'], name_form=name_form)

@app.errorhandler(404)
def page_not_found(e):
    name_form = NameForm(request.form)
    set_vars()
    return render_template('mm.html', value=session['set_word'], name_form=name_form)

@app.errorhandler(500)
def page_not_found(e):
    name_form = NameForm(request.form)
    set_vars()
    return render_template('mm.html', value=session['set_word'], name_form=name_form)

if __name__ == "__main__":
    app.secret_key = 'giant'
    app.run(debug=True)
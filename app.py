from flask import Flask, render_template, session, request
import random
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'donec', 'tempus', 'commodo', 'nisl', 'eget', 'pellentesque', 'sed', 'nec', 'nunc', 'eget', 'leo', 'iaculis', 'malesuada', 'pellentesque', 'interdum', 'convallis', 'suscipit', 'morbi', 'vitae', 'ullamcorper', 'purus', 'eget', 'interdum', 'odio', 'ut', 'suscipit', 'felis', 'scelerisque', 'faucibus', 'aliquam', 'dui', 'nunc', 'suscipit', 'risus', 'nec', 'tincidunt', 'dui', 'nibh', 'quis', 'est', 'vestibulum', 'laoreet', 'quis', 'urna', 'nec', 'tempor', 'sed', 'maximus', 'interdum', 'risus', 'nec', 'facilisis']

class NameForm(Form):
	i1 = StringField('Enter your ID:', [DataRequired(message="Enter Your Name Please"), Length(min=4, max=5)])

class TypeForm(Form):
	t1 = StringField('Typed Text:', [DataRequired(message="Start Typing"), Length(min=0, max=415)])

def set_vars():
    session['set_word'] = sorted(words, key=lambda k: random.random())
    session['set_state'] = 0
    session['set_ign'] = ''

@app.route('/', methods=['GET', 'POST'])
def hi():
    name_form = NameForm(request.form)
    type_form = TypeForm(request.form)
    if request.method == 'GET' and session.get('set_state') == None:
        set_vars()
        return render_template('mm.html', value=session['set_word'], name_form=name_form)
    
    elif request.method == 'POST' and session.get('set_state') == 0:
        session['set_state'] = 1
        session['set_ign'] = request.form['i1']
        return render_template('mm.html', value=session['set_word'], type_form=type_form)


if __name__ == "__main__":
    app.secret_key = 'giant'
    app.run(debug=True)
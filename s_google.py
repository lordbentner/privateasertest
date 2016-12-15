from flask import Flask
from flask import request
from flask import render_template
from wtforms import Form, BooleanField, TextField, validators
app = Flask(__name__)

class RegistrationForm(Form):
    username     = TextField('Username', [validators.Length(min=4, max=25)])
    email        = TextField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.Required()])

@app.route('/', methods=['POST'])
def my_form_post():

    processed_text = request.form['text']
    return render_template('index.html', resultat=processed_text)

@app.route('/')
def hello():
    return render_template('index.html')

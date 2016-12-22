from flask import Flask
from flask import request,url_for
import requests 
from flask import render_template
from html.parser import HTMLParser
from wtforms import Form, BooleanField, TextField, validators, TextAreaField
app = Flask(__name__)

class RegistrationForm(Form):
    url    = TextField('url')
    motscles = TextAreaField('motscles',render_kw={"rows": 11, "cols": 20})
    position = TextField('position')
    page_max = TextField('page_max')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.data = []
        self.position = 0
        self.countLanguages = 0
        self.lasttag = None
        self.lastname = None
        self.lastvalue = None
        self.form = RegistrationForm(request.form)

    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'cite':
            for name, value in attrs:
                if name == 'class' and value == '_Rm':
                    self.inLink = True
                    self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == "cite":
            self.inlink = False

    def handle_data(self, data):
        if self.lasttag == 'cite' and data.find(self.form.url.data) != -1:
            self.data.append(data)
            self.position = self.getpos()[0] - 1
            print (data)
            print(self.getpos()[0] - 1)


@app.route('/', methods=['POST'])
def my_form_post():
    form = RegistrationForm(request.form)
    processed_text = "https://www.google.fr/search?hl=fr&q="+form.motscles.data[0]+"&start=0"
    parse = MyHTMLParser()
    r = requests.get(processed_text)
    res = parse.feed(r.text)


    return render_template('index.html', form=form, resultat=parse.data, position=parse.position)

@app.route('/')

def hello():
    form = RegistrationForm(request.form)
    return render_template('index.html',form=form)

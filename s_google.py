from flask import Flask
from flask import request,url_for
import requests 
from flask import render_template
from html.parser import HTMLParser
from wtforms import Form, BooleanField, TextField, validators, TextAreaField , FieldList, IntegerField
app = Flask(__name__)

class RegistrationForm(Form):
    url    = TextField('Site web')
    motscles = TextAreaField('Mots-clés',render_kw={"rows": 11, "cols": 40})
    position = TextField('position')
    page_max = TextField('Descendre jusqu\'a la page')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.data = 'n/a'
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
            self.data = data
            self.position = self.getpos()[0]


@app.route('/', methods=['POST'])
def my_form_post():
    form = RegistrationForm(request.form)
    page  = form.page_max.data
    i = 0;
    donne_final = '<table class="tableau" style=" border : solid 1px black;text-align: center;"><tr><td><b>Mot-clé</b></td><td><b>URL</b></td><td><b>Position</b></td></tr>'
    form.motscles.data.split("\n")
    for l in form.motscles.data.split("\n"):
        while i < (int(page)*10):
            processed_text = "https://www.google.fr/search?hl=fr&q="+l+"&start="+str(i)
            parse = MyHTMLParser()
            r = requests.get(processed_text)
            res = parse.feed(r.text)
            if parse.data  != 'n/a' or (i+10)  >= (int(page)*10):
                donne_final = donne_final+"<tr><td>"
                donne_final = donne_final+l
                donne_final = donne_final+"</td><td>"
                donne_final = donne_final+parse.data
                donne_final = donne_final+"</td><td>"
                if parse.data  != 'n/a':
                    donne_final = donne_final+str(parse.position+i)
                else:
                    donne_final = donne_final+'n/a'
                donne_final = donne_final+"</td></tr>"
                break
            i = i+10
    donne_final  = donne_final+"</table>"

    return render_template('index.html', form=form, resultat=donne_final, position=parse.position)

@app.route('/')

def hello():
    form = RegistrationForm(request.form)
    form.page_max.default = "1"
    form.process()
    return render_template('index.html',form=form)

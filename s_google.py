from flask import Flask
from flask import request,url_for
import requests
from flask import render_template
from html.parser import HTMLParser
from wtforms import Form, TextField, validators, ValidationError, TextAreaField
app = Flask(__name__)

class RegistrationForm(Form):
    url = TextField('Site web')
    keyword = TextAreaField('Mots-clés',render_kw={"rows": 11, "cols": 40})
    page_max = TextField('Descendre jusqu\'a la page')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.data = 'n/a'
        self.position = 0
        self.lasttag = None
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
    parse = MyHTMLParser()
    page  = parse.form.page_max.data
    try:
        int(parse.form.page_max.data)
    except ValueError:     
        return render_template('index.html', form=parse.form,error="Veuillez insérer un nombre")
    i = 0
    j = 0
    array_data = []
    parse.form.keyword.data.split("\n")
    for l in parse.form.keyword.data.split("\n"):
        while i < (int(page)*10):
            processed_text = "https://www.google.fr/search?hl=fr&q="+l+"&start="+str(i)
            r = requests.get(processed_text)
            res = parse.feed(r.text)
            if parse.data  != 'n/a' or (i+10)  >= (int(page)*10):
                array_data.append([])
                array_data[j].append(l)
                array_data[j].append(parse.data)
                if parse.data  != 'n/a':
                    array_data[j].append(str(parse.position+i))
                else:
                    array_data[j].append('n/a')
                break
            i = i+10
        j = j+1

    return render_template('index.html', form=form,result = array_data)

@app.route('/')

def hello():
    form = RegistrationForm(request.form)
    form.page_max.default = "1"
    form.process()
    return render_template('index.html',form=form)

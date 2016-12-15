from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route('/', methods=['POST'])
def my_form_post():

    processed_text = request.form['text'].upper()
    return render_template('index.html')

@app.route('/')
def hello():
    return render_template('index.html')


# -*-coding:Latin-1 -*


import os # On importe le module os qui dispose de variables 
          # et de fonctions utiles pour dialoguer avec votre 
          # système d'exploitation

# Programme testant si une année, saisie par l'utilisateur, est bissextile ou non

# On met le programme en pause pour éviter qu'il ne se referme (Windows)
os.system("pause")
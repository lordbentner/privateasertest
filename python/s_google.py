from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

# -*-coding:Latin-1 -*

import os # On importe le module os qui dispose de variables 
          # et de fonctions utiles pour dialoguer avec votre 
          # système d'exploitation

# Programme testant si une année, saisie par l'utilisateur, est bissextile ou non

# On met le programme en pause pour éviter qu'il ne se referme (Windows)
os.system("pause")
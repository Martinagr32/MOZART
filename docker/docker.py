'''
    Creating our image
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

# PROBANDO CON UN HOLAMUNDO
from flask import Flask

app = Flask(__name__)

@app.route('/') 
def hello_world():     
    return 'Hello World' 

@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name

if __name__ == "__main__":
    app.run()


from flask import Flask, render_template
import time
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Round1/')
def Round1():
    return render_template('Round1.html')

@app.route('/Round2/')
def Round2():
    return render_template('Round2.html')

@app.route('/Round3/')
def Round3():
    return render_template('Round3.html')

@app.route('/Round4/')
def Round4():
    return render_template('Round4.html')

@app.route('/Round5/')
def Round5():
    return render_template('Round5.html')

@app.route('/Round6/')
def Round6():
    return render_template('Round6.html')

if __name__ == '__main__':
    app.run()
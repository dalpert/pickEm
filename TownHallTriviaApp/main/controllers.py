from flask import Blueprint, render_template


main = Blueprint("main", __name__, template_folder="templates")

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/Round1/')
def Round1():
    return render_template('Round1.html')

@main.route('/Round2/')
def Round2():
    return render_template('Round2.html')

@main.route('/Round3/')
def Round3():
    return render_template('Round3.html')

@main.route('/Round4/')
def Round4():
    return render_template('Round4.html')

@main.route('/Round5/')
def Round5():
    return render_template('Round5.html')

@main.route('/Round6/')
def Round6():
    return render_template('Round6.html')
from flask import Blueprint, render_template


main = Blueprint("main", __name__, template_folder="templates")

@main.route('/')
def home():
    return render_template('main/home.html')

@main.route('/Round1/')
def Round1():
    return render_template('main/Round1.html')

@main.route('/Round2/')
def Round2():
    return render_template('main/Round2.html')

@main.route('/Round3/')
def Round3():
    return render_template('main/Round3.html')

@main.route('/Round4/')
def Round4():
    return render_template('main/Round4.html')

@main.route('/Round5/')
def Round5():
    return render_template('main/Round5.html')

@main.route('/Round6/')
def Round6():
    return render_template('main/Round6.html')
from flask import Blueprint, render_template, session, url_for, redirect, request


main = Blueprint("main", __name__, template_folder="templates")

@main.route('/')  
def home():
    if "teamName" in session:
        return redirect(url_for("main.Round1")) 
    return render_template("main/home.html") 
 
@main.route('/login')  
def login():  
    return render_template("main/login.html")
 
@main.route('/success', methods = ["POST"])  
def success():  
    if request.method == "POST":  
        session['teamName']=request.form['teamName']  
        return render_template('main/success.html', teamName=session['teamName'])
    return redirect(url_for("main.home")) 
 
@main.route('/logout')  
def logout():  
    if 'teamName' in session:  
        session.pop('teamName',None)  
        return render_template('main/logout.html');
    else:  
        return redirect(url_for("main.home"))

@main.route('/Round1/')
def Round1():
    return render_template('main/Round1.html', teamName=session['teamName'])

@main.route('/Round2/')
def Round2():
    return render_template('main/Round2.html', teamName=session['teamName'])

@main.route('/Round3/')
def Round3():
    return render_template('main/Round3.html', teamName=session['teamName'])

@main.route('/Round4/')
def Round4():
    return render_template('main/Round4.html', teamName=session['teamName'])

@main.route('/Round5/')
def Round5():
    return render_template('main/Round5.html', teamName=session['teamName'])

@main.route('/Round6/')
def Round6():
    return render_template('main/Round6.html', teamName=session['teamName'])
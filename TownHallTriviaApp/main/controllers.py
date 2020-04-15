from flask import Blueprint, render_template, session, url_for, redirect, request
import redisCacheManager
import flaskSessionManager

main = Blueprint("main", __name__, template_folder="templates")
teamName = "teamName"
teamId = "teamId"
roundNumber = "roundNumber"
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@main.route('/')  
def home():
    if teamName in session:
        return redirect(url_for("main.Round1"))
    sessionManager.setSessionId("1")
    return render_template("main/home.html") 
 
@main.route('/login')  
def login():
    return render_template("main/login.html")
 
@main.route('/success', methods = ["POST"])  
def success():  
    if request.method == "POST":
        sessionManager.setTeamName(request.form[teamName])
        sessionManager.setTeamId()
        redisManager.registerTeam()
        return render_template('main/success.html', teamName=sessionManager.getTeamName())
    return redirect(url_for("main.home")) 
 
@main.route('/logout')  
def logout():  
    if teamName in session:  
        session.pop(teamName, None)
        return render_template('main/logout.html');
    else:  
        return redirect(url_for("main.home"))

@main.route('/Round1/')
def Round1():
    if teamName in session:
        session[roundNumber] = 1
        return render_template('main/Round.html', teamName=session[teamName], roundNumber=session[roundNumber])
    else:
        return redirect(url_for("main.home"))

@main.route('/Round2/')
def Round2():
    if teamName in session and roundNumber in session:
        session[roundNumber] = 2
        return render_template('main/Round.html', teamName=session[teamName], roundNumber=session[roundNumber])
    else:
        return redirect(url_for("main.home"))

@main.route('/Round3/')
def Round3():
    if teamName in session and roundNumber in session:
        session[roundNumber] = 3
        return render_template('main/Round.html', teamName=session[teamName], roundNumber=session[roundNumber])
    else:
        return redirect(url_for("main.home"))

@main.route('/Round4/')
def Round4():
    if teamName in session and roundNumber in session:
        session[roundNumber] = 4
        return render_template('main/Round.html', teamName=session[teamName], roundNumber=session[roundNumber])
    else:
        return redirect(url_for("main.home"))

@main.route('/Round5/')
def Round5():
    if teamName in session and roundNumber in session:
        session[roundNumber] = 5
        return render_template('main/Round.html', teamName=session[teamName], roundNumber=session[roundNumber])
    else:
        return redirect(url_for("main.home"))

@main.route('/Round6/')
def Round6():
    if teamName in session and roundNumber in session:
        session[roundNumber] = 6
        return render_template('main/Round.html', teamName=session[teamName], roundNumber=session[roundNumber])
    else:
        return redirect(url_for("main.home"))

@main.route('/Round7/')
def Round7():
    if teamName in session and roundNumber in session:
        session[roundNumber] = 7
        return redirect(url_for("main.logout"))
    else:
        return redirect(url_for("main.home"))

@main.route('/SubmitRoundAnswers/', methods = ["POST"])
def WriteToCache():
    if request.method == "POST":  
        redisManager.writeFormAnswers(request.form)
        currentroundNumber = request.form[roundNumber]
        sessionManager.incrementRoundNumber()
        pageName = "main.Round" + str(sessionManager.getRoundNumber())
        return redirect(url_for(pageName))
    return redirect(url_for("main.home")) 

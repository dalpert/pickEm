from flask import Blueprint, render_template, session, url_for, redirect, request
import redisCacheManager
import flaskSessionManager

admin = Blueprint("admin", __name__, template_folder="templates")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@admin.route('/')
def Home():
    sessionManager.setSessionId("1")
    return render_template('admin/home.html', session=session)

@admin.route('/getInfo/')
def getInfo():
    if sessionManager.doesSessionIdExist():
        return render_template('admin/getInfo.html', session=session, info=redisManager.getAllTeams())
    else:
        return redirect(url_for("admin.Home"))

@admin.route('/teamAnswers', methods = ["POST"])  
def teamAnswers():  
    if request.method == "POST":
        return render_template('admin/teamAnswers.html', teamAnswers=redisManager.readFormAnswers(request.form["teamId"], request.form["roundNumber"]))
    return redirect(url_for("admin.Home")) 
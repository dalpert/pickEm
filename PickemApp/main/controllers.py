from flask import Blueprint, render_template, session, url_for, redirect, request
import json
import redisCacheManager
import flaskSessionManager

main = Blueprint("main", __name__, template_folder="templates")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@main.route('/')
def homePage():
    sessionManager.logOutUser()
    return render_template('main/home.html')

@main.route('/loginUser')
def loginUser():
    sessionManager.logOutUser()
    sessionManager.loginUser(request.form["userName"])
    return render_template('main/enterGameId.html')
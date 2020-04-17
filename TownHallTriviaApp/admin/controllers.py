from flask import Blueprint, render_template, session, url_for, redirect, request
import redisCacheManager
import flaskSessionManager

admin = Blueprint("admin", __name__, template_folder="templates")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@admin.route('/')
def Index():
    return render_template('admin/index.html')

def checkGameId():
    if request.form["submit"] == "Create":
        if not redisManager.doesGameExist(request.form["gameId"]):
            redisManager.createGame(request.form["gameId"])
            sessionManager.setAdminGameId(request.form["gameId"])
            return redirect(url_for('admin.controlPanel'))
        else:
            return redirect(url_for("admin.gameIdError", message="Game ID already exists, choose another :)"))
    elif request.form["submit"] == "Find":
        if redisManager.doesGameExist(request.form["gameId"]):
            sessionManager.setAdminGameId(request.form["gameId"])
            return redirect(url_for('admin.controlPanel'))
        else:
            return redirect(url_for("admin.gameIdError", message="Game ID doesn't exists, fix spelling or create a new game."))

@admin.route('/gameIdError/')
def gameIdError():
    render_template('admin/gameIdError.html', gameId=sessionManager.getAdminGameId(), message=request.args.get('message'))

@admin.route('/controlPanel/')
def controlPanel():
    return render_template(
        'admin/controlPanel.html',
        gameId=sessionManager.getAdminGameId(),
        isGameEnabled=redisManager.isGameEnabled(sessionManager.getAdminGameId()),
        enabledRounds=redisManager.getEnabledRounds(sessionManager.getAdminGameId()))

@admin.route('/toggleGame/')
def toggleGame():
    if request.method == "POST":
        request.form["toggleGame"] == "enableGame":
            redisManager.enableGame(sessionManager.getAdminGameId())
        request.form["toggleGame"] == "disableGame":
            redisManager.disableGame(sessionManager.getAdminGameId())
    return redirect(url_for('admin.controlPanel'))

@admin.route('/toggleRound/', methods=["POST"])
def toggleRound():
    if request.method == "POST":
        request.form["submit"] == "disableRound":
            redisManager.disableRound(request.form["roundId"])
        request.form["submit"] == "enableRound":
            redisManager.enableRound(request.form["roundId"])
    return redirect(url_for('admin.controlPanel'))

@admin.route('/getRoundResults/', methods=["POST"])
def toggleRound():
    if request.method == "POST":
        roundAnswers = redisManager.getRoundAnswers(sessionManager.getAdminGameId(), request.form["roundId"])
        # Download Files
    return redirect(url_for('admin.controlPanel'))





    
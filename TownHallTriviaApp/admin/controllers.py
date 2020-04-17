from flask import Blueprint, render_template, session, url_for, redirect, request
import redisCacheManager
import flaskSessionManager

admin = Blueprint("admin", __name__, template_folder="templates")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/checkGameId', methods=["POST"])
def checkGameId():
    print(request.form)
    print(request.form["gameId"])
    if request.form["operation"] == "Create":
        if not redisManager.doesGameExist(request.form["gameId"]):
            redisManager.createGame(request.form["gameId"])
            sessionManager.setAdminGameId(request.form["gameId"])
            return redirect(url_for('admin.controlPanel', message="Game Created!"))
        else:
            return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Game ID already exists, choose another :)"))
    elif request.form["operation"] == "Find":
        if redisManager.doesGameExist(request.form["gameId"]):
            sessionManager.setAdminGameId(request.form["gameId"])
            return redirect(url_for('admin.controlPanel', message="Game Found!"))
        else:
            return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Game ID doesn't exists, fix spelling or create a new game."))

@admin.route('/gameIdError')
def gameIdError():
    return render_template('admin/gameIdError.html', gameId=request.args.get('gameId'), message=request.args.get('message'))

@admin.route('/controlPanel')
def controlPanel():
    return render_template(
        'admin/controlPanel.html',
        message=request.args.get('message'),
        gameId=sessionManager.getAdminGameId(),
        isGameEnabled=redisManager.isGameEnabled(sessionManager.getAdminGameId()),
        enabledRounds=redisManager.getEnabledRounds(sessionManager.getAdminGameId()))

@admin.route('/toggleGame', methods=["POST"])
def toggleGame():
    if request.method == "POST":
        if request.form["toggleGame"] == "Game Enabled":
            redisManager.enableGame(sessionManager.getAdminGameId())
        elif request.form["toggleGame"] == "Game Disabled":
            redisManager.disableGame(sessionManager.getAdminGameId())
        else:
            return redirect(url_for("admin.gameIdError", gameId=sessionManager.getAdminGameId(), message="Expected: Game Enabled/Game Disabled Actual: " + request.form["toggleGame"]))
    return redirect(url_for('admin.controlPanel', message=request.form["toggleGame"]))

@admin.route('/toggleRound', methods=["POST"])
def toggleRound():
    if request.method == "POST":
        if request.form["submit"] == "Enabled":
            redisManager.enableRound(request.form["roundId"])
        elif request.form["submit"] == "Disabled":
            redisManager.disableRound(request.form["roundId"])
        else:
            return redirect(url_for("admin.gameIdError", gameId=sessionManager.getAdminGameId(), message="Expected: Enabled/Disabled" + request.form["submit"]))
    return redirect(url_for('admin.controlPanel', message=request.form["submit"] + " " + request.form["roundId"]))

@admin.route('/getRoundResults', methods=["POST"])
def getRoundResults():
    if request.method == "POST":
        roundAnswers = redisManager.getRoundAnswers(sessionManager.getAdminGameId(), request.form["roundId"])
        # Download Files
    return redirect(url_for('admin.controlPanel', message="Downloaded Files For " + request.form["roundId"]))






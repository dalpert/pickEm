from flask import Blueprint, render_template, session, url_for, redirect, request
import redisCacheManager
import flaskSessionManager
import automaticGrading.autoGrader as autoGrader
import os, csv

admin = Blueprint("admin", __name__, template_folder="templates")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@admin.route('/')
def adminLogin():
    sessionManager.toggleAdminLoggedInState(False)
    return render_template('admin/adminLogin.html')

@admin.route('/adminLoginValidation', methods=["POST"])
def adminLoginValidation():
    if request.method == "POST":
        if request.form["adminPassword"] == os.environ['CUSTOMCONNSTR_ADMIN_PASSWORD']:
            sessionManager.toggleAdminLoggedInState(True)
            return redirect(url_for("admin.home"))
        else:
            return redirect(url_for("admin.adminLogin"))

@admin.route('/home')
def home():
    if sessionManager.isAdminLoggedIn():
        return render_template('admin/home.html')
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/checkGameId', methods=["POST"])
def checkGameId():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            if request.form["operation"] == "Create":
                if not redisManager.doesGameExist(request.form["gameId"]):
                    # Game doesn't exist, so we create a new one
                    if redisManager.createGame(request.form["gameId"]):
                        sessionManager.setAdminGameId(request.form["gameId"])
                        return redirect(url_for('admin.controlPanel', message="Game "+ request.form["gameId"] + " created!"))
                    else:
                        return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Failed to initialize Game ID, please try again."))
                else:
                    # Game already exists
                    return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Game ID already exists, choose another :)"))
            elif request.form["operation"] == "Find":
                if redisManager.doesGameExist(request.form["gameId"]):
                    sessionManager.setAdminGameId(request.form["gameId"])
                    return redirect(url_for('admin.controlPanel', message="Game Found!"))
                else:
                    return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Game ID doesn't exists, fix spelling or create a new game."))
    else:
        redirect(url_for("admin.adminLogin"))

@admin.route('/gameIdError')
def gameIdError():
    if sessionManager.isAdminLoggedIn():
        return render_template('admin/gameIdError.html', gameId=request.args.get('gameId'), message=request.args.get('message'))
    else:
        redirect(url_for("admin.adminLogin"))
@admin.route('/controlPanel')
def controlPanel():
    if sessionManager.isAdminLoggedIn():
        return render_template(
            'admin/controlPanel.html',
            message=request.args.get('message'),
            gameId=sessionManager.getAdminGameId(),
            isGameEnabled=redisManager.isGameEnabled(sessionManager.getAdminGameId()),
            enabledRounds=redisManager.getEnabledRounds(sessionManager.getAdminGameId()))
    else:
        redirect(url_for("admin.adminLogin"))

@admin.route('/toggleGame', methods=["POST"])
def toggleGame():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            if request.form["toggleGame"] == "Game Enabled":
                redisManager.enableGame(sessionManager.getAdminGameId())
            elif request.form["toggleGame"] == "Game Disabled":
                redisManager.disableGame(sessionManager.getAdminGameId())
            else:
                return redirect(url_for("admin.gameIdError", gameId=sessionManager.getAdminGameId(), message="Expected: Game Enabled/Game Disabled Actual: " + request.form["toggleGame"]))
        return redirect(url_for('admin.controlPanel', message=request.form["toggleGame"]))
    else:
        redirect(url_for("admin.adminLogin"))

@admin.route('/toggleRound', methods=["POST"])
def toggleRound():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            if request.form["submit"] == "Enabled":
                redisManager.enableRound(sessionManager.getAdminGameId(), request.form["roundId"])
            elif request.form["submit"] == "Disabled":
                redisManager.disableRound(sessionManager.getAdminGameId(), request.form["roundId"])
            else:
                return redirect(url_for("admin.gameIdError", gameId=sessionManager.getAdminGameId(), message="Expected: Enabled/Disabled" + request.form["submit"]))
        return redirect(url_for('admin.controlPanel', message=request.form["submit"] + " " + request.form["roundId"]))
    else:
        redirect(url_for("admin.adminLogin"))

@admin.route('/getRoundResults', methods=["POST"])
def getRoundResults():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            roundAnswers = redisManager.getRoundAnswers(sessionManager.getAdminGameId(), request.form["roundId"])
            answerKey = redisManager.get
            print("In ADMIN CONTROLLER.PY")
            print(roundAnswers)
            with open("results/rawAnswers.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(roundAnswers)



            # THIS IS WHERE WE INVOKE AUTOMATIC GRADING



        return redirect(url_for('admin.controlPanel', message="Downloaded Files For " + request.form["roundId"]))
    else:
        redirect(url_for("admin.adminLogin"))

@admin.route('/answerKey')
def answerKey():
    if sessionManager.isAdminLoggedIn():
        return render_template("admin/answerKey.html")

@admin.route('/submitAnswerKey', methods=["POST"])
def submitAnswerKeySuccess():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            answers =
            [request.form['Question1'],
            request.form['Question2'],
            request.form['Question3'],
            request.form['Question4'],
            request.form['Question5'],
            request.form['Question6']]
            pointValues = 
            [request.form['Question1_ExpectedPoints'],
            request.form['Question2_ExpectedPoints'],
            request.form['Question3_ExpectedPoints'],
            request.form['Question4_ExpectedPoints'],
            request.form['Question5_ExpectedPoints'],
            request.form['Question6_ExpectedPoints']]
            redisManager.submitAnswerKey(sessionManager.getAdminGameId(), request.form["roundId"], answers, pointValues)
            return redirect(url_for("admin.controlPanel"))

@admin.route('/flushDb', methods=["POST"])
def flushDb():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            roundAnswers = redisManager.flushDb()
            return redirect(url_for("admin.home"))
    else:
        redirect(url_for("admin.adminLogin"))





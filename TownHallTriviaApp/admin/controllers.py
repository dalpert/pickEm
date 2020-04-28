from flask import Blueprint, render_template, session, url_for, redirect, request, send_file, send_from_directory
import redisCacheManager
import flaskSessionManager
import autoGrader as autoGraderClass
import os, csv
import json

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()
autoGrader = autoGraderClass.autoGraderClass()

@admin.route('/')
def adminLogin():
    sessionManager.toggleAdminLoggedInState(False)
    sessionManager.removeAdminGame()
    return render_template('admin/adminLogin.html')

@admin.route('/adminLoginValidation', methods=["POST"])
def adminLoginValidation():
    if request.method == "POST":
        if request.form["adminPassword"] == os.environ['CUSTOMCONNSTR_ADMIN_PASSWORD']:
            sessionManager.toggleAdminLoggedInState(True)
            return redirect(url_for("admin.getGameId"))
        else:
            return redirect(url_for("admin.adminLogin"))

@admin.route('/getGameId')
def getGameId():
    if sessionManager.isAdminLoggedIn():
        return render_template('admin/getGameId.html')
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
                        sessionManager.setMessage("Game "+ request.form["gameId"] + " created!")
                        return redirect(url_for('admin.controlPanel'))
                    else:
                        return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Failed to initialize Game ID, please try again."))
                else:
                    # Game already exists
                    return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Game ID already exists, choose another :)"))
            elif request.form["operation"] == "Find":
                if redisManager.doesGameExist(request.form["gameId"]):
                    sessionManager.setAdminGameId(request.form["gameId"])
                    sessionManager.setMessage("Game Found!")
                    return redirect(url_for('admin.controlPanel'))
                else:
                    return redirect(url_for("admin.gameIdError", gameId=request.form["gameId"], message="Game ID doesn't exists, fix spelling or create a new game."))
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/gameIdError')
def gameIdError():
    if sessionManager.isAdminLoggedIn():
        return render_template('admin/gameIdError.html', gameId=request.args.get('gameId'), message=request.args.get('message'))
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/controlPanel')
def controlPanel():
    if sessionManager.isAdminLoggedIn():
        return render_template(
            'admin/controlPanel.html',
            message=sessionManager.getMessage(),
            gameId=sessionManager.getAdminGameId(),
            isGameEnabled=redisManager.isGameEnabled(sessionManager.getAdminGameId()),
            enabledRounds=redisManager.getEnabledRounds(sessionManager.getAdminGameId()))
    else:
        return redirect(url_for("admin.adminLogin"))

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
        sessionManager.setMessage(request.form["toggleGame"])
        return redirect(url_for('admin.controlPanel'))
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/toggleRound', methods=["POST"])
def toggleRound():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            print(request.form)
            print(request.form.get("submit"))
            if request.form.get("submit") == "Enabled":
                redisManager.enableRound(sessionManager.getAdminGameId(), request.form["roundId"])
            elif request.form["submit"] == "Disabled":
                redisManager.disableRound(sessionManager.getAdminGameId(), request.form["roundId"])
            else:
                return redirect(url_for("admin.gameIdError", gameId=sessionManager.getAdminGameId(), message="Expected: Enabled/Disabled" + request.form["submit"]))
        sessionManager.setMessage(request.form["submit"] + " " + request.form["roundId"])
        return redirect(url_for('admin.controlPanel'))
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/getRoundEndTime', methods=["POST"])
def getRoundEndTime():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            enabled, endTime = redisManager.getCountdownClockInfo(sessionManager.getAdminGameId())
            print(" in py. getRoundEntime")
            print(request.form)
            sessionManager.setMessage("Auto-Disable has been enabled for " + request.form["roundId"])
            info = {"endTime" : endTime}
            # Convert dict to string
            info = json.dumps(info)
            print(info)
            return info
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/setCountdownClockInfo', methods=["POST"])
def setCountdownClockInfo():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            remainingSeconds = 0
            try:
                remainingSeconds = int(request.form["remainingSeconds"])
            except ValueError:
                print(request.form["remainingSeconds"] + " Can't be converted to an INT")
                sessionManager.setMessage("\"" + request.form["remainingSeconds"] + "\" is not a valid value for the countdownClock")
                return redirect(url_for('admin.controlPanel'))
            success, endtime = redisManager.setCountdownClockInfo(sessionManager.getAdminGameId(), remainingSeconds)
            sessionManager.setMessage("Enabled countDown Clock with " + request.form["remainingSeconds"] + " seconds remaining. Auto Submissions at: " + endtime)
        return redirect(url_for('admin.controlPanel'))
    else:
        return redirect(url_for("admin.adminLogin"))


@admin.route('/getRoundResults', methods=["POST"])
def getRoundResults():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            roundAnswers = redisManager.getRoundAnswers(sessionManager.getAdminGameId(), request.form["roundId"])
            answerKey = redisManager.getAnswerKey(sessionManager.getAdminGameId(), request.form["roundId"])
            # THIS IS WHERE WE INVOKE AUTOMATIC GRADING
            if len(answerKey) == 0:
                sessionManager.setMessage("Someone didnt submit an answer key for " + request.form["roundId"])
                return redirect(url_for("admin.controlPanel"))
            print("answerKey")

            print(answerKey)
            print("controller.py:: Running Auto Grader:")
            print(os.listdir())
            pathToResultsFolder = os.path.join(admin.static_folder, "roundResults")
            filelist = [ f for f in os.listdir(pathToResultsFolder) ]
            for file in filelist:
                print("FILE: " + file)
                os.remove(os.path.join(pathToResultsFolder, file))
            autoGrader.gradeAndWriteFiles(roundAnswers, answerKey, request.form["roundId"])
            # Empty Results Folder
            zipFileName = autoGrader.createZipFile()
            # print(admin.static_folder)
            # print(os.path.join(admin.static_folder, "roundResults", zipFileName))
            # root_dir = os.path.dirname(os.getcwd())
            # print("root_dir")
            # print(root_dir)
            # return send_from_directory(os.path.join(root_dir, 'TownHallTrivia', "TownHallTriviaApp", 'roundResults'), zipFileName)
            # return admin.send_static_file(os.path.join(admin.static_folder, "roundResults", zipFileName))
            return send_file(os.path.join(pathToResultsFolder, zipFileName), attachment_filename=zipFileName, as_attachment = False, cache_timeout=0)
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/answerKey')
def answerKey():
    if sessionManager.isAdminLoggedIn():
        if sessionManager.isAdminGameIdSet():
            return render_template("admin/answerKey.html", gameId=sessionManager.getAdminGameId())
        else:
            return redirect(url_for("admin.getGameId"))


@admin.route('/submitAnswerKey', methods=["POST"])
def submitAnswerKeySuccess():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            answers = [request.form['Answer1'],
            request.form['Answer2'],
            request.form['Answer3'],
            request.form['Answer4'],
            request.form['Answer5'],
            request.form['Answer6']]
            pointValues = [request.form['Question1_ExpectedPoints'],
            request.form['Question2_ExpectedPoints'],
            request.form['Question3_ExpectedPoints'],
            request.form['Question4_ExpectedPoints'],
            request.form['Question5_ExpectedPoints'],
            request.form['Question6_ExpectedPoints']]
            redisManager.submitAnswerKey(sessionManager.getAdminGameId(), request.form["roundId"], answers, pointValues)
            sessionManager.setMessage("Answer Key Submission Successful for " + request.form["roundId"])
            return redirect(url_for("admin.controlPanel"))

@admin.route('/getAllTeams')
def getAllTeams():
    if sessionManager.isAdminLoggedIn():
        teamNames = redisManager.getAllTeams(sessionManager.getAdminGameId())
        teamsCount = len(teamNames)
        teamNameString = ",  ".join(teamNames)
        return render_template("admin/getAllTeams.html", teamsList=teamNameString, teamsCount=teamsCount)

@admin.route('/getTeamsForNextWeek')
def getTeamsForNextWeek():
    if sessionManager.isAdminLoggedIn():
        teamNames = redisManager.getTeamsForNextWeek(sessionManager.getAdminGameId())
        teamsCount = len(teamNames)
        teamNameString = ",  ".join(teamNames)
        return render_template("admin/getAllTeams.html", teamsList=teamNameString, teamsCount=teamsCount)

@admin.route('/getTeamResponseCount', methods=["POST"])
def getTeamResponseCount():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            teamsThatHaveAnswered, totalTeamCount = redisManager.getTeamResponseCount(sessionManager.getAdminGameId(), request.form["roundId"])
            sessionManager.setMessage(str(teamsThatHaveAnswered) + "/" + str(totalTeamCount) + " have responded")
            return redirect(url_for("admin.controlPanel"))
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/flushDb', methods=["POST"])
def flushDb():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            sessionManager.removeAdminGame()
            roundAnswers = redisManager.flushDb()
            return redirect(url_for("admin.getGameId"))
    else:
        return redirect(url_for("admin.adminLogin"))





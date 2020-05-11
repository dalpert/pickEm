from flask import Blueprint, render_template, session, url_for, redirect, request, send_file, send_from_directory
import redisCacheManager
import flaskSessionManager
import TownHallTriviaApp.admin.autoGrader as autoGraderClass
from TownHallTriviaApp.admin.zipFileManagement import zipFileManagement
import os, csv
import json
from datetime import datetime, timedelta

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()
autoGrader = autoGraderClass.autoGraderClass(admin.static_folder)

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

@admin.route('/downloadNextWeeksTeams', methods=["POST"])
def downloadNextWeeksTeams():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            nextWeekTeams = redisManager.getTeamsForNextWeek(request.form["date"])
            nextWeekTeams.insert(0, ["First Name", "Last Name", "Team Name", "Email"])
            zipFileClass = zipFileManagement("RegisteredTeams.zip", admin.static_folder)
            zipFileClass.emptyOutputFolder()
            autoGrader.writeRowsToCsvFile(request.form["date"] + ".csv", nextWeekTeams)
            zipFileClass.createZipFileFromOutputFolder()
            return send_file(zipFileClass.getZipFilePath(), attachment_filename=zipFileClass.getZipFileName(), as_attachment = False, cache_timeout=0)

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
            
            # lock the round 2 seconds after the client's forced form submission
            endTimeObject = datetime.strptime(endTime, "%B %d %Y %H:%M:%S")
            print("in getRoundEndTime::::")
            endTimeObject = endTimeObject + timedelta(0, 10)
            endTime = endTimeObject.strftime("%B %d %Y %H:%M:%S")
            print(" in py. getRoundEntime")
            print(endTime)
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
            if len(answerKey) == 0:
                sessionManager.setMessage("Someone didnt submit an answer key for " + request.form["roundId"])
                return redirect(url_for("admin.controlPanel"))
            zipFileClass = zipFileManagement("Results.zip", admin.static_folder)
            zipFileClass.emptyOutputFolder()
            autoGrader.gradeAndWriteFiles(roundAnswers, answerKey, request.form["roundId"])
            zipFileClass.createZipFileFromOutputFolder()
            return send_file(zipFileClass.getZipFilePath(), attachment_filename=zipFileClass.getZipFileName(), as_attachment = False, cache_timeout=0)
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

@admin.route('/teamsRegistrationView')
def teamsRegistrationView():
    if sessionManager.isAdminLoggedIn():
        thisWeekTeams = redisManager.getAllTeams(sessionManager.getAdminGameId())
        thisWeekTeamsCount = len(thisWeekTeams)
        thisWeekTeamString = ",  ".join(thisWeekTeams)
        return render_template("admin/currentTeams.html",
            thisWeekList=thisWeekTeamString,
            thisWeekCount=thisWeekTeamsCount)

@admin.route('/getTeamResponseCount', methods=["POST"])
def getTeamResponseCount():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            teamsThatHaveAnswered, totalTeamCount = redisManager.getTeamResponseCount(sessionManager.getAdminGameId(), request.form["roundId"])
            sessionManager.setMessage(str(teamsThatHaveAnswered) + "/" + str(totalTeamCount) + " have responded")
            return redirect(url_for("admin.controlPanel"))
    else:
        return redirect(url_for("admin.adminLogin"))

@admin.route('/getGameAnswerKeys', methods=["POST"])
def getGameAnswerKeys():
    if sessionManager.isAdminLoggedIn():
        if request.method == "POST":
            zipFileClass = zipFileManagement("AnswerKeys.zip", admin.static_folder)
            zipFileClass.emptyOutputFolder()
            roundIds = ["Round_1", "Round_2", "Round_3", "Round_4", "Round_5", "Round_6"]
            for roundId in roundIds:
                answerKey = redisManager.getAnswerKey(request.form["gameId"], roundId)
                if len(answerKey) == 0:
                    continue
                # NNED TO ADD ROUND ID TO THIS FUNCTIN HEADER
                autoGrader.writeAnswerKeyToTextFile(answerKey, roundId)
            zipFileClass.createZipFileFromOutputFolder()
            return send_file(zipFileClass.getZipFilePath(), attachment_filename=zipFileClass.getZipFileName(), as_attachment = False, cache_timeout=0)
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





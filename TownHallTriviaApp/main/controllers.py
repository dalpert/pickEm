from flask import Blueprint, render_template, session, url_for, redirect, request
import json
import redisCacheManager
import flaskSessionManager

main = Blueprint("main", __name__, template_folder="templates")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()

@main.route('/')
def homePage():
    sessionManager.removePlayerGame()
    sessionManager.unregisterTeam()
    # shouldPresentSignUpPage, date = redisManager.presentSignUpFormOnHomePage()
    if False:
        return render_template("main/signUpForNextWeek.html")
    else:
        return render_template('main/enterGameId.html')

@main.route('/validateGameId', methods = ["POST", "GET"])
def validateGameId():
    if request.method == "POST":
        sessionManager.setPlayerGameId(request.form["gameId"])
        if not redisManager.doesGameExist(request.form["gameId"]):
            sessionManager.setMessage("That game id isn't valid")
            return redirect(url_for("main.error", ))
        if redisManager.isGameEnabled(request.form["gameId"]):
            sessionManager.setMessage("Let's get ready to rumble!")
            return redirect(url_for("main.registerTeam"))
        else:
            return redirect(url_for("main.gameWaitingRoom"))
    else:
        return redirect(url_for("main.homePage"))

@main.route('/gameWaitingRoom')
def gameWaitingRoom():
    if not sessionManager.isPlayerGameIdSet():
        sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
        return redirect(url_for("main.error"))
    if redisManager.isGameEnabled(sessionManager.getPlayerGameId()):
        sessionManager.setMessage("Thanks for your patience. Now let's get your team registered!")
        return redirect(url_for("main.registerTeam"))
    else:
        return render_template("main/gameWaitingRoom.html", gameId=sessionManager.getPlayerGameId(), message=sessionManager.getMessage())

@main.route('/registerTeam')
def registerTeam():
    if not sessionManager.isPlayerGameIdSet():
        # Don't have a valid gameId set
        sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
        return redirect(url_for("main.error"))
    if redisManager.isGameEnabled(sessionManager.getPlayerGameId()):
        return render_template("main/registerTeam.html", gameId=sessionManager.getPlayerGameId(), message=sessionManager.getMessage())
    else:
        return render_template("main/gameWaitingRoom.html", gameId=sessionManager.getPlayerGameId())

@main.route('/error')
def error():
    return render_template("main/error.html", gameId=sessionManager.getPlayerGameId(), message=sessionManager.getMessage())

@main.route('/teamRegisterSuccess', methods = ["POST", "GET"])
def teamRegisterSuccess():
    if request.method == "POST":
        if sessionManager.isTeamRegistered():
            sessionManager.unregisterTeam()
        sessionManager.setTeamName(request.form["teamName"])
        if redisManager.addTeamToGame(sessionManager.getPlayerGameId(), request.form["teamName"]):
            # Allow team to login as existing team
            sessionManager.setMessage("Succesfull registration!")
            return redirect(url_for("main.gamePlayRoom"))
        else:
            return redirect(url_for("main.loginAsExistingTeam"))
    else:
        sessionManager.setMessage("Stick to clicking buttons, entering url's directly wont get you anywhere. Let's start over.")
        return redirect(url_for("main.error"))

@main.route('/loginAsExistingTeam')
def loginAsExistingTeam():
    if not sessionManager.isPlayerGameIdSet():
        sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
        return redirect(url_for("main.error"))
    if not sessionManager.isTeamRegistered():
        sessionManager.setMessage("You have to register a team before playing!")
        return redirect(url_for("main.registerTeam"))
    return render_template('main/loginAsExistingTeam.html', teamName=sessionManager.getTeamName())

@main.route('/confirmation')
def confirmation():
    if not sessionManager.isPlayerGameIdSet():
        sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
        return redirect(url_for("main.error"))
    if not sessionManager.isTeamRegistered():
        sessionManager.setMessage("You have to register a team before playing!")
        return redirect(url_for("main.registerTeam"))
    return render_template("main/confirmation.html", gameId=sessionManager.getPlayerGameId(), teamName=sessionManager.getTeamName(), message=sessionManager.getMessage())

@main.route('/gamePlayRoom')
def gamePlayRoom():
    if not sessionManager.isPlayerGameIdSet():
        sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
        return redirect(url_for("main.error"))
    if not sessionManager.isTeamRegistered():
        sessionManager.setMessage("You have to register a team before playing!")
        return redirect(url_for("main.registerTeam", gameId=sessionManager.getPlayerGameId()))
    return render_template("main/gamePlayRoom.html", gameId=sessionManager.getPlayerGameId(), teamName=sessionManager.getTeamName())

@main.route('/playRound', methods = ["POST", "GET"])
def playRound():
    if request.method == "POST":
        if not sessionManager.isPlayerGameIdSet():
            sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
            return redirect(url_for("main.error"))
        if not sessionManager.isTeamRegistered():
            sessionManager.setMessage("You have to register a team before playing!")
            return redirect(url_for("main.registerTeam", gameId=sessionManager.getPlayerGameId()))
        if not redisManager.isGameEnabled(sessionManager.getPlayerGameId()):
            sessionManager.setMessage("Trivia Game \"" + sessionManager.getPlayerGameId() + "\" is no longer Enabled")
            return redirect(url_for("main.gameWaitingRoom"))
        sessionManager.setRoundId(request.form["roundId"])
        sessionManager.toggleCountdownClockEnabled(False)
        redisManager.disableCountdownClock(sessionManager.getPlayerGameId())
        if redisManager.isRoundEnabled(sessionManager.getPlayerGameId(), sessionManager.getRoundId()):
            return render_template("main/round.html", teamName=sessionManager.getTeamName(), gameId=sessionManager.getPlayerGameId(), roundId=sessionManager.getRoundId())
        return redirect(url_for("main.gamePlayRoom", message="Woah there... " + request.form["roundId"] + " isn't enabled yet, hold your horses!"))
    else:
        sessionManager.setMessage("Stick to clicking buttons, entering url's directly wont get you anywhere. Let's start over.")
        return redirect(url_for("main.error"))

@main.route("/checkCountdownClock")
def checkCountdownClock():
    # enabled, endTime = redisManager.getCountdownClockInfo(sessionManager.getPlayerGameId())
    info = {"AdminEnabled" : enabled, "EndTime" : endTime, "ClientEnabled" : sessionManager.getCountdownClockEnabled()}
    # Convert dict to string
    info = json.dumps(info)
    if enabled:
        sessionManager.toggleCountdownClockEnabled(True)
    return info

@main.route('/submitTeamAnswers', methods = ["POST", "GET"])
def submitTeamAnswers():
    if request.method == "POST":
        if not sessionManager.isPlayerGameIdSet():
            sessionManager.setMessage("We couldn't process your game id. You'll have to re-enter it to continue.")
            return redirect(url_for("main.error"))
        if not sessionManager.isTeamRegistered():
            sessionManager.setMessage("You have to register a team before playing!")
            return redirect(url_for("main.registerTeam", gameId=sessionManager.getPlayerGameId()))
        if redisManager.isRoundEnabled(sessionManager.getPlayerGameId(), sessionManager.getRoundId()):
            redisManager.submitTeamAnswers(sessionManager.getPlayerGameId(), sessionManager.getTeamName(), sessionManager.getRoundId(), request.form)
            sessionManager.setMessage(sessionManager.getRoundId() + " Answer Submission Confirmation")
            return redirect(url_for("main.confirmation"))
        else:
            sessionManager.setMessage("You unfortunately were not able to submit your form in time for " + sessionManager.getRoundId() + ". Try to submit earlier for the next round!")
            return redirect(url_for("main.confirmation"))
    else:
        sessionManager.setMessage("Stick to clicking buttons, entering url's directly wont get you anywhere. Let's start over.")
        return redirect(url_for("main.error"))

@main.route('/endGame')
def endGame():
    sessionManager.unregisterTeam()
    return render_template("main/endGame.html")

@main.route('/registerTeamForNextWeek', methods = ["POST"])
def registerTeamForNextWeek():
    if request.method == "POST":
        if not redisManager.registerTeamForNextWeek(sessionManager.getPlayerGameId(), request.form["teamName"], request.form["emailContact"]):
            return redirect(url_for("main.endGame"))
        return redirect(url_for("main.homePage"))
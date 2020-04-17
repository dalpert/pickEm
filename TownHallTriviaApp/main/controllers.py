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
def index():
    return render_template('main/index.html')

@main.route('/validateGameId', methods = ["POST"])
def validateGameId():
    if redisManager.doesGameExist(request.form["gameId"]):
        sessionManager.setPlayerGameId(request.form["gameId"])
        if redisManager.isGameEnabled(request.form["gameId"]):
            return redirect(url_for("main.registerTeam", message="Let's get ready to rumble!"))
        else:
            return redirect(url_for("main.gameWaitingRoom"))
    else:
        return redirect(url_for("main.error", gameId=request.form["gameId"], message="Your Game Id isn't valid"))

@main.route('/gameWaitingRoom')
def gameWaitingRoom():
    if redisManager.isGameEnabled(sessionManager.getPlayerGameId()):
        return redirect(url_for("main.registerTeam"))
    else:
        return render_template("main/gameWaitingRoom.html", gameId=sessionManager.getPlayerGameId())

@main.route('/registerTeam')
def registerTeam():
    return render_template("main/registerTeam.html", gameId=sessionManager.getPlayerGameId(), message=request.args.get('message'))

@main.route('/error')
def error():
    return render_template("main/error.html", gameId=request.args.get('gameId'), message=request.args.get('message'))

@main.route('/teamRegisterSuccess', methods = ["POST"])
def teamRegisterSuccess():
    if request.method == "POST":
        if sessionManager.isTeamRegistered():
            session.pop(teamName, None)
        if not redisManager.addTeamToGame(sessionManager.getPlayerGameId(), request.form["teamName"]):
            return redirect(url_for("main.registerTeam", message="Team Name: " + request.form["teamName"] + " has already been taken, please choose another name."))
        sessionManager.setTeamName(request.form["teamName"])
        return redirect(url_for("main.confirmation", message="Succesfull registration!"))

@main.route('/confirmation')
def confirmation():
    return render_template("main/confirmation.html", gameId=sessionManager.getPlayerGameId(), teamName=sessionManager.getTeamName(), message=request.args.get('message'))

@main.route('/gamePlayRoom')
def gamePlayRoom():
    return render_template("main/gamePlayRoom.html", gameId=sessionManager.getPlayerGameId(), teamName=sessionManager.getTeamName())

@main.route('/startRound', methods = ["POST"])
def startRound():
    if request.method == "POST":
        roundId = request.form["roundId"]
        if redisManager.isRoundEnabled(sessionManager.getPlayerGameId(), roundId):
            return redirect(url_for("main.round", roundId=roundId))
        return redirect(url_for("main.gamePlayRoom"))

@main.route('/round')
def round():
    return render_template("main/round.html", teamName=sessionManager.getTeamName(), roundId=request.args.get('roundId'))

@main.route('/submitTeamAnswers', methods = ["POST"])
def submitTeamAnswers():
    if request.method == "POST":
        redisManager.submitTeamAnswers(sessionManager.getPlayerGameId(), sessionManager.getTeamName(), request.form)
        return redirect(url_for("main.confirmation", message=request.form["roundId"] + " Answer Submission Confirmation"))






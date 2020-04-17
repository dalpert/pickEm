import redis, os
from flask import session
import flaskSessionManager as flaskManager

QuestionNames = ["Question1", "Question2", "Question3", "Question4", "Question5", "Question6"]

# Define a class
class RedisClass:
    def __init__(self):
        myHostname = os.environ['CUSTOMCONNSTR_REDIS_CACHE_HOSTNAME']
        myPassword = os.environ['CUSTOMCONNSTR_REDIS_CACHE_PRIMARY_KEY']
        port = 6380
        sslEnabledPort = True
        self.redisCxn = redis.StrictRedis(host=myHostname, port=port, password=myPassword, ssl=sslEnabledPort)
        self.flaskSessionManager = flaskManager.FlaskSessionManager()
        self.GameIdKey = "GameIds"
        self.EnabledRounds = "_EnabledRounds"
        self.RoundResults = "_RoundResults"
        self.teams = "_teams"

    ##########################
    ## Functions for Admins ##
    ##########################

    def doesGameExist(self, gameId):
        # Check GameIds Map
        key = self.GameIdKey
        return True

    def createGame(self, gameId):
        # Add gameId to GameIds map
        key = self.GameIdKey
        pass

    def isGameEnabled(self, gameId):
        # check value associated with gameId in GameIds table
        key = self.GameIdKey
        return True

    def getEnabledRounds(self, gameId):
        # Return list of round numbers
        key = gameId + self.EnabledRounds
        return ["Round_1", "Round_4"]

    def enableGame(self, gameId):
        # Set gameId value to True
        key = self.GameIdKey

    def disableGame(self, gameId):
        # set gameId value to False
        key = self.GameIdKey

    def enableRound(self, gameId):
        # Add round to the Enabled Rounds Table
        key = gameId + self.EnabledRounds

    def disableRound(self, gameId):
        # Remove round from Enabled Rounds Table
        key = gameId + self.EnabledRounds

    def getRoundAnswers(self, gameId, roundId):
        # return round Answers for all teams
        key = gameId + self.RoundResults


    def addTeamToGame(self, gameId, teamId):
        # Add team to Teams list
        # check to ensure team name is unique
        key = gameId + self.teams
        return True

    def submitTeamAnswers(self, gameId, teamId, answers):
        # Add round answers for the given team
        key = gameId + self.RoundResults
        subkey = teamId

    def isRoundEnabled(self, gameId, roundId):
        enabledRounds = self.getEnabledRounds(gameId)
        return roundId in enabledRounds









    def testConnection():
        isSuccess = r.ping()
        return isSuccess

    def readFormAnswers(self, teamId, roundNumber):
        formSubmission = ""
        for questionName in QuestionNames:
            key = str(teamId) + str(roundNumber) + questionName
            if self.redisCxn.exists(key):
                result = self.redisCxn.get(key)
                formSubmission += result.decode("utf-8") + "\t"
        return formSubmission

    def writeFormAnswers(self, form):
        teamId = self.flaskSessionManager.getTeamId()
        roundNumber = self.flaskSessionManager.getRoundNumber()
        for questionName in QuestionNames:
            key = str(teamId) + str(roundNumber) + questionName
            value = form[questionName]
            print("did cache write succeed? : " + str(self.redisCxn.set(key, value)))

    def registerTeam(self):
        key = "TeamList-" + self.flaskSessionManager.getSessionId()
        result = self.redisCxn.hset(key, self.flaskSessionManager.getTeamId(), self.flaskSessionManager.getTeamName())

    def getAllTeams(self):
        key = "TeamList-" + self.flaskSessionManager.getSessionId()
        if self.redisCxn.exists(key):
            return self.redisCxn.hgetall(key)
        return None

    def read(self, key):
        result = self.redisCxn.get(firstKey)
        return result.decode("utf-8")

    def getClientList(self):
        result = self.redisCxn.client_list()
        print("CLIENT LIST returned : ")
        for c in result:
            print("id : " + c['id'] + ", addr : " + c['addr'])






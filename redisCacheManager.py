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
        db=0
        self.redisCxn = redis.StrictRedis(host=myHostname, port=port, password=myPassword, db=db, ssl=sslEnabledPort, socket_timeout=None, decode_responses=True)
        self.flaskSessionManager = flaskManager.FlaskSessionManager()
        self.EnabledRounds = "_EnabledRounds"
        self.RoundResults = "_RoundResults"
        self.TeamsKey = "_teams"
        self.Enabled = "Enabled"
        self.Disabled = "Disabled"

# Game Level Functions
    def createGame(self, gameId):
        gameKey = gameId
        # print("in createGame")
        if self.redisCxn.exists(gameKey):
            # Game already Exists
            return False
        return self.redisCxn.set(gameKey, self.Disabled)

    def doesGameExist(self, gameId):
        # print("in doesGameExist")
        key = gameId
        return self.redisCxn.exists(key)

    def isGameEnabled(self, gameId):
        # print("in isGameEnabled")
        key = gameId
        return self.Enabled == self.redisCxn.get(key)

    def enableGame(self, gameId):
        key = gameId
        return self.redisCxn.set(key, self.Enabled)

    def disableGame(self, gameId):
        key = gameId
        return self.redisCxn.set(key, self.Disabled)

    def flushDb(self):
        self.redisCxn.flushdb()


# Team Operations
    def addTeamToGame(self, gameId, teamName):
        key = gameId + self.TeamsKey
        teamsListLength = self.redisCxn.llen(key)
        expectedLength = teamsListLength + 1
        existingTeams = self.redisCxn.lrange(key, 0, teamsListLength)
        if existingTeams == None:
            # appending the first Team
            return expectedLength == self.redisCxn.rpush(key, teamName)
        # print("existingTeams: ")
        # print(existingTeams)
        if teamName not in existingTeams:
            # print("adding team to list")
            # print("teamName: " + teamName)
            #  rpush returns the number of objects successfully appended
            return expectedLength == self.redisCxn.rpush(key, teamName)
        else:
            # Team already exists
            return False

# Round Operations
    def getEnabledRounds(self, gameId):
        key = gameId + self.EnabledRounds
        enabledRounds = []
        if self.redisCxn.exists(key):
            roundsListLength = self.redisCxn.llen(key)
            enabledRounds = self.redisCxn.lrange(key, 0, roundsListLength)
        return enabledRounds

    def enableRound(self, gameId, roundId):
        key = gameId + self.EnabledRounds
        expectedListLength = self.redisCxn.llen(key) + 1
        returnValue = self.redisCxn.rpush(key, roundId)
        # print("In ENABLEROUND")
        # print("expectedListLength: " + str(expectedListLength) + " returnValue: " + str(returnValue))
        return expectedListLength == returnValue

    def disableRound(self, gameId, roundId):
        key = gameId + self.EnabledRounds
        returnValue = self.redisCxn.lrem(key, 0, roundId)
        # print("IN DISABLEROUND")
        # print("expectedListLength: " + str(1) + " returnValue: " + str(returnValue))
        return 1 == returnValue

    def isRoundEnabled(self, gameId, roundId):
        enabledRounds = self.getEnabledRounds(gameId)
        return roundId in enabledRounds

# Round Answer Operations
    def submitTeamAnswers(self, gameId, teamName, roundId, form):
        key = gameId + '_' + roundId
        header = ','.join(map(str, form.keys()))
        answers = ','.join(map(str, form.values()))
        finalCsv = '\n'.join([header, answers])
        # print(finalCsv)
        self.redisCxn.hset(key, teamName, finalCsv)

    # Get all all answers
    def getRoundAnswers(self, gameId, roundId):
        key = gameId + '_' + roundId
        returnValue = self.redisCxn.hgetall(key)
        print(returnValue)
        return returnValue

# General Redis Functions
    def testConnection():
        isSuccess = r.ping()
        return isSuccess

    def getClientList(self):
        result = self.redisCxn.client_list()
        print("CLIENT LIST returned : ")
        for c in result:
            print("id : " + c['id'] + ", addr : " + c['addr'])






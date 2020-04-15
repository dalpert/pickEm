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






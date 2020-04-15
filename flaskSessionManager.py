from flask import session
import uuid


# Define a class
class FlaskSessionManager:
    def __init__(self):
        self.teamName = "teamName"
        self.teamId = "teamId"
        self.roundNumber = "roundNumber"
        self.sessionId = "sessionId"
    
    def setTeamName(self, teamNameInput):
        session[self.teamName] = teamNameInput

    def setTeamId(self):
        session[self.teamId] = str(uuid.uuid4())

    def setRoundNumber(self, roundNumberInput):
        session[self.roundNumber] = roundNumberInput

    def incrementRoundNumber(self):
        session[self.roundNumber] += 1

    def setSessionId(self, sessionId):
        session[self.sessionId] = sessionId

    def doesSessionIdExist(self):
        return self.sessionId in session

    def getRoundNumber(self):
        return session[self.roundNumber]

    def getTeamName(self):
        return session[self.teamName]

    def getTeamId(self):
        return session[self.teamId]

    def getSessionId(self):
        return session[self.sessionId]
from flask import session
import uuid


# Define a class
class FlaskSessionManager:
    def __init__(self):
        self.teamName = "teamName"
        self.teamId = "teamId"
        self.roundId = "roundId"
        self.adminGameId = "adminGameId"
        self.playerGameId = "playerGameId"
        self.message = "message"
        self.adminLogin = "adminLogin"

    def toggleAdminLoggedInState(self, loggedIn):
        session[self.adminLogin] = loggedIn

    def isAdminLoggedIn(self):
        return session[self.adminLogin] == True
    
    def isTeamRegistered(self):
        return self.teamName in session

    def unregisterTeam(self):
        session.pop(self.teamName, None)

    def setTeamName(self, teamName):
        session[self.teamName] = teamName

    def setTeamId(self):
        session[self.teamId] = str(uuid.uuid4())

    def setRoundId(self, roundId):
        session[self.roundId] = roundId

    def setAdminGameId(self, gameId):
        session[self.adminGameId] = gameId

    def setPlayerGameId(self, gameId):
        session[self.playerGameId] = gameId

    def setMessage(self, message):
        session[self.message] = message

    def getMessage(self):
        return session[self.message]

    def getPlayerGameId(self):
        return session[self.playerGameId]

    def getAdminGameId(self):
        return session[self.adminGameId]

    def getRoundId(self):
        return session[self.roundId]

    def getTeamName(self):
        return session[self.teamName]

    def getTeamId(self):
        return session[self.teamId]
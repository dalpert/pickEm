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
        loggedIn = self.adminLogin in session
        if loggedIn:
            loggedIn = session[self.adminLogin] == True
        return loggedIn

    def isAdminGameIdSet(self):
        return self.adminGameId in session

    def removeAdminGame(self):
        if self.adminGameId in session:
            session.pop(self.adminGameId, None)
    
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
        if self.message in session:
            return session[self.message]
        else:
            return None

    def getPlayerGameId(self):
        if self.playerGameId in session:
            return session[self.playerGameId]
        return None

    def getAdminGameId(self):
        if self.adminGameId in session:
            return session[self.adminGameId]
        else:
            return None

    def getRoundId(self):
        if self.roundId in session:
            return session[self.roundId]
        else:
            return None

    def getTeamName(self):
        if self.teamName in session:
            return session[self.teamName]
        else:
            return None

    def getTeamId(self):
        if self.teamId in session:
            return session[self.teamId]
        else:
            return None
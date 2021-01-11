from flask import session

class FlaskSessionManager:
    def __init__(self):
        self.user = "user"
    
    def isUserLoggedIn(self):
        return self.user in session

    def logoutUser(self):
        session.pop(self.user, None)

    def loginUser(self, userName):
        session[self.user] = userName
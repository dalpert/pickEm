from flask import Flask
from TownHallTriviaApp.main.controllers import main
from TownHallTriviaApp.admin.controllers import admin

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
app.secret_key = "abc"

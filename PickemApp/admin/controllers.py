from flask import Blueprint, render_template, session, url_for, redirect, request, send_file, send_from_directory
import redisCacheManager
import flaskSessionManager
import TownHallTriviaApp.admin.autoGrader as autoGraderClass
from TownHallTriviaApp.admin.zipFileManagement import zipFileManagement
import os, csv
import json
from datetime import datetime, timedelta

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="")
redisManager = redisCacheManager.RedisClass()
sessionManager = flaskSessionManager.FlaskSessionManager()
autoGrader = autoGraderClass.autoGraderClass(admin.static_folder)

@admin.route('/')
def adminLogin():
    sessionManager.toggleAdminLoggedInState(False)
    sessionManager.removeAdminGame()
    return render_template('admin/adminLogin.html')

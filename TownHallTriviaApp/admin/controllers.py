from flask import Blueprint, render_template, session


admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route('/')
def home():
    return render_template('admin/home.html', session=session)

"""
Page Logic goes here

This is a blank path template
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

BLANK_path = Blueprint('BLANK_path', __name__)

"""
@BLANK_path.route('/BLANK')
@login_required
def BLANK():
    return render_template("BLANK.html", user=current_user)
"""

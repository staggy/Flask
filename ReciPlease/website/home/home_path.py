"""
This is the landing page
similar to a index.html or index.php

"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_path = Blueprint('home_path', __name__)


# since teh '/' is the route this makes this page the home page.
@home_path.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)
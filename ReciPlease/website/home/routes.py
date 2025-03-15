"""
This is the landing page
similar to an index.html or index.php

"""
from website.home import blueprint

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user


# since the '/' is the route this makes this page the home page.
@blueprint.route('/', methods=['GET'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_blueprint.login'))
    return render_template('home.html', user=current_user)
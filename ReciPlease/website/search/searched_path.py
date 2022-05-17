"""
Page Logic goes here

login_required
"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from website.models import Recipe, User

from website.sanitize import *
from website import db

searched_path = Blueprint('searched_path', __name__)


@searched_path.route('/searched', methods=['get', 'post'])
@login_required
def searched():

    recipes = Recipe.query.all()
    users = User.query.all()

    if request.method == 'POST':
        selected = request.form.getlist('favorite')
        for recipeID in selected:
            print(f"for id:{recipeID}")
            print(int(current_user.getid()))
            recipes[int(recipeID) - 1].favorited.append(users[current_user.getid() - 1])
            db.session.commit()

        print(f"cur: {current_user}")
        print(request.form.getlist('favorite'))
        print(f"selected: {selected}")

        return render_template('searchedfavorited.html', user=current_user)

    return render_template('searched.html', user=current_user, favorited=fav)
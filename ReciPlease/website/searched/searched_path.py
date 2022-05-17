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
    # Called after form is submitted passes the search results and displays
    # Check boxes on the page allow users to select their favorites
    
    # Not the best way to get a list of recipes and users
    # but quickest way to get ID in tables to verify against
    recipes = Recipe.query.all()
    users = User.query.all()
    
    if request.method == 'POST':
        selected = request.form.getlist('favorite')
        #print(selected)
        for recipeID in selected:
            recipes[int(recipeID)-1].favorited.append(users[current_user.getid()-1])
            
            db.session.commit()
        # add the chosen recipes to user_recipes table by calling this path to process
        return render_template('searchedfavorited.html', user=current_user)
    # if GET then just render the searched page
    return render_template('searched.html', user=current_user, favorited=fav)
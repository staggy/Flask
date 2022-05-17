"""
Page Logic goes here
login_required
"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from website.sanitize import *
from website import db

search_path = Blueprint('search_path', __name__)


@search_path.route('/search', methods=['post', 'get'])
@login_required
def search():
    error = ""
    if request.method == 'POST':

        searched_value = []
        search_ing_flag = False
        search_recipe_flag = False
        search_recipe = sanitize(request.form['searchName'])
        search_ing = sanitize(request.form['searchIng'])

        if search_ing == '' and search_recipe == '':
            error = "Please enter something"
        elif search_recipe != '' and search_ing != '':
            error = "Please only search one entry"
        if search_recipe != '':
            search_recipe_flag = True
        if search_ing != '':
            search_ing_flag = True
        if error != '':
            return render_template('search.html', message=error, user=current_user)

        # search Recipe
        if search_recipe_flag and len(search_recipe) <= 1:
            error = "Please enter a valid search entry"
            return render_template('search.html', message=error, user=current_user)
        elif search_recipe_flag:
            query = f"SELECT id, name, instructions FROM recipe WHERE name LIKE \'%{search_recipe}%\'"

            searched_value = []
            result = db.session.execute(query)
            for item in result:
                searched_value.append(item)

        # search ingredients
        if search_ing_flag and len(search_ing) <= 1:
            error = "Please enter a valid search entry 2"

            return render_template('search.html', message=error, user=current_user)
        elif search_ing_flag:
            query = f"SELECT name FROM ingredient WHERE name LIKE \'%{search_ing}%\'"

            searched_value = []
            result = db.session.execute(query)
            for item in result:
                searched_value.append(item)

        return render_template('searched.html', user=current_user, searched_value=searched_value)

    return render_template('search.html', message=error, user=current_user)
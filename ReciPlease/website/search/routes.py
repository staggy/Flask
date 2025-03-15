"""
Page Logic goes here
login_required
"""
from website.search import blueprint
from website.sanitize import *
from website import db
from website.models import Recipe, User
from sqlalchemy import text
from flask import render_template, request
from flask_login import login_required, current_user


@blueprint.route('/search', methods=['post', 'get'])
@login_required
def search():
    error = ""
    if request.method == 'POST':

        searched_value = []
        search_ing_flag = False
        search_recipe_flag = False
        search_recipe = sanitize(request.form['searchName'])
        search_ing = sanitize(request.form['searchIng'])
        
        # Verify a value was entered
        if search_ing == '' and search_recipe == '':
            error = "Please enter something"
        elif search_recipe != '' and search_ing != '':
            error = "Please only search one entry"
        if search_recipe != '':
            search_recipe_flag = True
        elif search_ing != '':
            search_ing_flag = True
        if error != '':
            return render_template('search.html', message=error, user=current_user)

        # search Recipe
        if search_recipe_flag and len(search_recipe) <= 1:
            error = "Please enter a valid search entry"
            return render_template('search.html', message=error, user=current_user)
        elif search_recipe_flag:
            query = text(f"SELECT id, name, instructions FROM recipe WHERE name LIKE \'%{search_recipe}%\'")

            searched_value = []
            result = db.session.execute(query)
            for item in result:
                searched_value.append(item)

        # search ingredients
        if search_ing_flag and len(search_ing) <= 1:
            error = "Please enter a valid search entry 2"

            return render_template('search.html', message=error, user=current_user)
        elif search_ing_flag:
            query = text(f"SELECT name FROM ingredient WHERE name LIKE \'%{search_ing}%\'")

            searched_value = []
            result = db.session.execute(query)
            for item in result:
                searched_value.append(item)

        return render_template('searched.html', user=current_user, searched_value=searched_value)

    return render_template('search.html', message=error, user=current_user)


@blueprint.route('/searched', methods=['get', 'post'])
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
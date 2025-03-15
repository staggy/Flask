"""
This page is for displaying the recipes that have been favorited

"""
from website.myrecipes import blueprint
from website.models import Recipe, User, recipe_user

from flask import render_template
from flask_login import login_required, current_user


@blueprint.route('/my-recipes')
@login_required
def my_recipes():
    recipe_list = []
    norecipes = False
    user = User.query.get(current_user.getid())
    recipes = user.favorites
    
    if len(recipes) == 0:
        norecipes = True
    else:
        for recipe in recipes:
            recipe_list.append(recipe)

    return render_template("myRecipes.html", user=current_user, recipe_list=recipe_list, norecipes=norecipes)

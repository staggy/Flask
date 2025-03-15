"""
template for recipes to be displayed.

uses the URL variables to query the database and display that recipe

E.g. http://127.0.0.1:5000/recipe?id=5
Will display the Candied Cashew Recipe

"""
from website.recipe import blueprint

from flask import render_template, request
from flask_login import login_required, current_user
from website.models import Recipe


@blueprint.route('/recipe')
@login_required
def recipe_template():
    """
    this needs to be passed a recipe's ID that's in the database.
    
    class Recipe(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200))  # unique=True cant do this
        instructions = db.Column(db.String(3000))
        ingredients = db.relationship('Ingredient', secondary=recipe_ingredient, backref='ingredients')
        favorited = db.relationship('User', secondary=recipe_user, backref='favorites')
    """
    # Recipe list that will hold the values inside the returned query
    recipe = []
    # get the Id from url parameter id
    id = request.args.get('id')
    
    # if there is no id variable passed this causes the server to have an internal error.
    if id != str:
        # id should always be a string as URL variable are strings
        # if its not a string class deliver the homepage.
        print(f'Error on /recipe URL given: {type(id)} : instead of a str class')
        return render_template('home.html', user=current_user)
    
    # query the recipe table for that id
    query = Recipe.query.get(id)
    # get the individual parts off the Recipe class and add them to a list that is passed to the html
    recipe.append(query.id)
    recipe.append(query.name)
    recipe.append(query.instructions)
    recipe.append(query.ingredients)
    
    return render_template('recipe.html', user=current_user, recipe=recipe)
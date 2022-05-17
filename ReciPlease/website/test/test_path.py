"""
Page Logic goes here
this is for testing
"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from flask_sqlalchemy import SQLAlchemy
from website.models import Recipe, Ingredient

from website.sanitize import *
from website import db




# db = SQLAlchemy()
testsearch_path = Blueprint('testsearch_path', __name__)


@testsearch_path.route('/testsearch', methods=['post', 'get'])
@login_required
def testsearch():
    #engine = create_engine('sqlite:///database.db')
    error = ""
    
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        # SANITIZE THIS SEARCH
        search_recipe = sanitize(request.form['searchName'])
        search_ing = sanitize(request.form['searchIng'])

        # Validate form data
        print()
        # if not search_recipe == '' and not search_ing == '':
        #     # input is empty
        #     error = "Please enter a valid search entry"
        if len(search_recipe) <= 1:
            # input is too short
            error = "Please enter a valid search entry"
        else:
            #connection = engine.connect()
            # print(search_recipe)
            query = f"SELECT name, instructions FROM recipe WHERE name LIKE \'%{search_recipe}%\'"

            searched_value = []
            result = db.session.execute(query)
            for item in result:
                searched_value.append(item)
                
            
            # print(searched_value)
            return testsearched(current_user, searched_value)
    return render_template('testsearch.html', message=error, user=current_user)


testsearched_path = Blueprint('testsearched_path', __name__)
@testsearched_path.route('/testsearched', methods=['get'])
@login_required
def testsearched(current_user, searched_value, enumerate=enumerate):
    return render_template('searched.html', user=current_user, searched_value=searched_value)



testrecipe_path = Blueprint('testrecipe_path', __name__)
@testrecipe_path.route('/recipe', methods=['get'])
@login_required
def testrecipe(current_user, recipeName, recipeInstructions):
    return render_template('recipe.html', user=current_user)







test_path = Blueprint('test_path', __name__)


@test_path.route('/test', methods=['post', 'get'])
@login_required
def test():
    """
        Manualy add items into Recipe database
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()

        """
    # new_recipe = Recipe(name='TestRecipe')
    # db.session.add(new_recipe)
    # db.session.commit()

    # q = session.query(Recipe)
    # user = User.query.filter_by(email=email).first()
    # recipes = Recipe.query.all()
    # https://www.youtube.com/watch?v=47i-jzrrIGQ 
    recipes = Recipe.query.all()
    ingredients = Ingredient.query.all()
    print(recipes[0])
    print(ingredients[0])
    recipes[0].ingredients.append(ingredients[0])
    # db.session.add(new_join)
    db.session.commit()


    search = ''

    if request.method == 'GET':
        recipes = Recipe.query.all()
        search = request.form.get('search')

    return render_template('test.html', user=current_user, recipes=recipes, search=search)
"""
Join table between users and recipes.

They will save their favorite recipes on this page.


"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os, hashlib

db = SQLAlchemy()
DB_NAME = "database.db"

# Variables for creating the recipe table
recipes_list = []
instructions_list = []
ingredients_list = []

abspath = os.path.abspath("./")

# Check for pathing of database creation
if os.name == 'mac' or os.name == 'posix':
    recpath = abspath + '/website/recipes/'
else:
    """
    Pathing Can cause issues. Depending on your folder structure edit this call.
    If you receive a 
    FileNotFoundError: [WinError 3] The system cannot find the path specified: 
    'C:\\Users\\Username\\.....\\Flask\\website\\recipes\\'
    
    Adjust the following pathing according to how your folder structure is setup.
    
    If you are still confused about what pathing python is giving by the abspath varaible
    uncomment the below print statments
    """
    # print(abspath)
    recpath = abspath + '\\ReciPlease\\website\\recipes\\'
    dbpath = f"{abspath}\\ReciPlease\\website\\{DB_NAME}"


def create_app():
    # IM FOR TESTING
    # uncomment bellow 4 lines to delete the database on startup
    # try:
    #     os.remove(dbpath)
    # except:
    #     pass
    # IM FOR TESTING
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Flask YOLO SECRET KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Takes defined database and initializes it.
    db.init_app(app)
    
    
    """
       Managing Pages:
    
            Add all paths to html pages here.
    """
    from .auth import auth
    from website.home.home_path import home_path
    from website.search.search_path import search_path
    from website.searched.searched_path import searched_path
    from website.myrecipes.myrecipes_path import myrecipes_path
    from website.recipe.recipe_path import recipe_path

    # from website.test.test_path import test_path, testsearch_path, testsearched_path, testrecipe_path
    # app.register_blueprint(test_path, url_prefix='/')
    # app.register_blueprint(testsearch_path, url_prefix='/')
    # app.register_blueprint(testsearched_path, url_prefix='/')
    # app.register_blueprint(testrecipe_path, url_prefix='/')

    #         Add all blueprint paths here.
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home_path, url_prefix='/')
    app.register_blueprint(search_path, url_prefix='/')
    app.register_blueprint(searched_path, url_prefix='/')
    app.register_blueprint(myrecipes_path, url_prefix='/')
    app.register_blueprint(recipe_path, url_prefix='/')
    ##############################################################

    # import the model and create the database
    from .models import User, Note, Recipe, recipe_ingredient

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # String=Folder name
    if not path.exists(dbpath):
        print(f"The fuq|{dbpath}")
        db.create_all(app=app)
        print('Created Database!\nCreating the recipes table. . .')

        # Create the Test user
        create_test_user(app)

        # import the file that has the statements already made
        create_recipe_table(app)
    return


def create_test_user(app):
    """
    Creates the Test user and adds them to the database.
    """
    from .models import User
    from werkzeug.security import generate_password_hash
    print('Adding Default User . . .')
    with app.app_context():
        password1 = 'Test01!'

        m = hashlib.sha256()  # creates sha256 digester
        m.update(password1.encode('utf-8'))  # encodes unicode into bits
        hashed_password = m.digest()
        salt = os.urandom(64)  # generate random bytes for salt
        m.update(salt)
        hashed_and_salted_password = m.digest()

        new_user = User(email='test1@test.com', first_name='test',
                        password=hashed_and_salted_password, salt=salt)
        db.session.add(new_user)
        db.session.commit()
    print('Added default user!')
    return

"""
These functions are for creating the recipe table.
"""


def create_recipe_table(app):
    from .models import Recipe, Ingredient

    print("Adding Recipe Table . . .")

    file_paths = get_paths(recpath)
    # span_files(file_paths)
    for file in file_paths:
        print(f"reading file: {file}")
        open_file(file)

    print(f"Number of Names:{len(recipes_list)}, instructions:{len(instructions_list)}")
    print("Creating the Recipe Table in the DB, This may take some time . . .")

    location = 0
    with app.app_context():
        for name in recipes_list:
            new_recipe = Recipe(name=name, instructions=instructions_list[location])
            db.session.add(new_recipe)
            location += 1

        for ingredient in ingredients_list:
            new_ingredient = Ingredient(name=ingredient)
            db.session.add(new_ingredient)
        db.session.commit()

    print("added Recipe Table!")

    return


def get_paths(directory):
    """
    Takes in the directory and returns a list of filepaths
    """
    files_path = []
    for file in os.listdir(directory):
        files_path.append(f"{recpath}{file}")
    return files_path


def open_file(recipe_file):
    count = 1
    recipe_location = 0

    with open(recipe_file, 'r') as file:
        lines = file.readlines()
        line_count = len(lines)
        # Boolean checks required for knowing when \n is actually the beginning of the instructions
        name_found = False
        ingredients_found = False
        inside_instructions = False
        instructions_skip = 0  # checks to make we are one line past the name.
        ingredients_location = 0

        instructions = ''  # Holds the instructions string

        for line in lines:
            # ----------------------------------------------------------------------------------------------|
            # Name is 2 lines from where the mastercook is
            if line == '* Exported from MasterCook *\n':
                recipe_location = count + 2
                instructions_skip = count + 3
                name_found = True

            if recipe_location == count:
                # strip all leading/trailing whitespace and \n, but we want \n so add it back
                striped = line.strip().replace('\"', '')
                striped = striped.replace('\'', '')
                striped = striped.replace(',', '')
                # add a check for last value here

                recipes_list.append(striped)
                recipe_location = 0
            # ----------------------------------------------------------------------------------------------|
            # Add the ingredients
            if line == '--------  ------------  --------------------------------\n' and instructions_skip < count:
                ingredients_location = count
                ingredients_found = True
            if ingredients_found and inside_instructions == False and count > ingredients_location and line != '\n':
                ingredient_line_list = line.strip()

                ingredient_line_list = ingredient_line_list.split('  ')
                ingredient_line_list = list(filter(('').__ne__, ingredient_line_list))

                # The ingredient_line_list doesnt always have 3 elements
                # sometimes there is no measurement like egg, its a single unit.
                if len(ingredient_line_list) == 2:
                    ingredient_line_list.insert(1, 'units')
                # sometimes there is no measurement or amount, either a comment or like frosting.
                if len(ingredient_line_list) == 1:
                    ingredient_line_list.insert(0, '')
                    ingredient_line_list.insert(0, '')
                
                # amount and measurement are not implemented
                amount = ingredient_line_list[0]
                measurement = ingredient_line_list[1]
                ingredient = ingredient_line_list[2]
                
                ingredients_list.append(ingredient)

            # ----------------------------------------------------------------------------------------------|
            # Add the instructions
            # Check if name and ingredients have been found, then this \n is the beginning of the instructions.
            if line == '\n' and name_found and ingredients_found:
                inside_instructions = True

            # once this is found instructions have ended.
            if '- - - - - - - - - - - - - - - - - - -' in line:
                instructions_list.append(instructions.strip())  # Add to list thats used in database creation.
                # reset for next recipe.
                instructions = ''
                name_found = False
                ingredients_found = False
                inside_instructions = False
                instructions_skip = 9999999999

            if inside_instructions:
                instructions += line
            count += 1
        file.close()
    # end
    return

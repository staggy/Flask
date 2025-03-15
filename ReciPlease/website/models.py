import hashlib
from base64 import b64decode, b64encode
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    salt = db.Column(db.String(150))
    notes = db.relationship('Note')
    
    def getid(self):
        return int(self.id)
    
    def authenticate(email: str, password: str):
        """
        Authenticate a user and password.

        :param username: a username
        :param password: a plaintext password
        :return: The User object if the username+password combination is found, None otherwise.
        """
        # This queries the DB and checks to see if the user has an account
        user = User.query.filter_by(email=email).first()
        # If a user exists
        if not user:
            return None
        else:
            msg = hashlib.sha256()
            msg.update(password.encode('utf-8'))
            msg.update(user.salt)
            hashed_salted_password = msg.digest()

            # Authentication failed
            if user.password != hashed_salted_password:
                return None

            return user

# Many to Many table between recipes and ingredients
recipe_ingredient = db.Table('recipe_ingredient',
                             db.Column('recipe_id', db.ForeignKey('recipe.id')),
                             db.Column('ingredient_id', db.ForeignKey('ingredient.id'))
                             )

# Many to Many table between User and Recipes
# This works as the table that they save thier favorites too
recipe_user = db.Table('recipe_user',
                             db.Column('recipe_id', db.ForeignKey('recipe.id')),
                             db.Column('user_id', db.ForeignKey('user.id'))
                             )


class Recipe(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))  # unique=True cant do this
    instructions = db.Column(db.String(3000))
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredient, backref='ingredients')
    favorited = db.relationship('User', secondary=recipe_user, backref='favorites')

    # there are multiples of same name

    def __repr__(self):
        return f"<Recipe: {self.name}>"


class Ingredient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), )  # unique=True cant do this

    # there are multiples of same name
    # recipe = db.relationship('Recipe', secondary=recipe_ingredient, backref='Recipes')

    def __repr__(self):
        return f"<Ingredient: {self.name}>"


class Shelf(db.Model):
    __tablename__ = 'Shelf'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'))

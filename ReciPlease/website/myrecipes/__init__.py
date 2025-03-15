from flask import Blueprint

blueprint = Blueprint(
    'myrecipes_blueprint',
    __name__,
    url_prefix=''
)
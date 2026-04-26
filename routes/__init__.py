from flask import Blueprint

from routes.account import admin_blueprint

mainBp = Blueprint("main", __name__)

# Loads all of the blueprints
def loadBlueprints(app):
    app.register_blueprint(admin_blueprint)

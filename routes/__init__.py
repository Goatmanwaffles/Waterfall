from flask import Blueprint

from routes.account import account_blueprint
from routes.student import student_blueprint
from routes.takes import takes_blueprint 
from routes.instructor import instructor_blueprint
from routes.classroom import classroom_blueprint
from routes.course import course_blueprint
from routes.section import section_blueprint
from routes.time_slot import time_slot_blueprint

mainBp = Blueprint("main", __name__)

# Loads all of the blueprints
def loadBlueprints(app):
    app.register_blueprint(account_blueprint)
    app.register_blueprint(student_blueprint)
    app.register_blueprint(takes_blueprint)
    app.register_blueprint(instructor_blueprint)
    app.register_blueprint(classroom_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(section_blueprint)

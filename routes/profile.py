from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

profile_blueprint = Blueprint("profile", __name__)

@profile_blueprint.route("/profile", methods=['POST', 'GET'])
def profile():
    return render_template(
        "profile.html",
        first_name="bob",
        last_name="LSbob"
    )

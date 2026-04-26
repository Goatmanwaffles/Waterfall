from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/dashboard")
def dash():
    #Get User auth level
    role = session.get("role")
    return render_template("dash.html", role=role)

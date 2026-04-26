from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

course_blueprint = Blueprint("course", __name__)


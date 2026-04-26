from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

instructor_blueprint = Blueprint("instructor", __name__)

@instructor_blueprint.route("/edit_prereqs", methods=['GET', 'POST'])
def edit_prereqs():
    if request.method =='GET':
        cursor = dbserver.cursor()
        instructor_ID = session.get("accountID")
        cursor.execute("""SELECT c.course_ID, c.title, pc.course_ID, pc.title
                       FROM course c 
                       JOIN teaches t ON t.course_ID = c.course_ID 
                       LEFT JOIN prereq p ON p.course_ID = c.course_ID
                       LEFT JOIN course pc ON p.course_ID = pc.course_ID 
                       WHERE t.instructor_ID = %s""", [instructor_ID])
        rows = cursor.fetchall()
        courses = []
        for course_ID, course_title, prereq_ID, prereq_title in rows:
            courses += {
                "course_ID": course_ID,
                "course_title": course_title,
                "prereq_ID": prereq_ID,
                "prereq_title": prereq_title
            }
        return render_template("prereqs.hmtl")

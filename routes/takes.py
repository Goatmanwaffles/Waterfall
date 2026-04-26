from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

takes_blueprint = Blueprint("takes", __name__)

#Okay so this works, besides for matching the ID and cleaning it up, in concept it works though
#It creates a row in takes with no grade
#TO DO:
#More precise filtering on what classes it shows (Shold probobaly only show like next 2 or 3 semesters IDK)
#Get User ID working so we can get actual users to use this and not whoever student ID 1 is
@takes_blueprint.route("/register", methods=['POST', 'GET'])
def register():
    student_ID = session.get("userID")
    
    if request.method == 'GET':
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, c.credits, s.semester, s.year, s.section_ID FROM section s JOIN course c on s.course_ID = c.course_ID WHERE s.year > 2025 AND NOT EXISTS (SELECT 1 FROM takes t WHERE t.section_ID = s.section_ID AND t.student_ID = %s)",[student_ID])
        sections = cursor.fetchall()
        cursor.close()
        return render_template("register.html", sections=sections)
    if request.method == 'POST':
        
        sec_ID = request.form['section_ID']
        cursor = dbserver.cursor()
        if sec_ID and student_ID:
            print("Executing")
            cursor.execute("INSERT INTO takes (student_ID, section_ID) VALUES (%s, %s)", [student_ID, sec_ID])
        cursor.close()
        dbserver.commit()

        #Gets Updated Courses List to filter out course just signed up for
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, c.credits, s.semester, s.year, s.section_ID FROM section s JOIN course c on s.course_ID = c.course_ID WHERE s.year > 2025 AND NOT EXISTS (SELECT 1 FROM takes t WHERE t.section_ID = s.section_ID AND t.student_ID = %s)",[student_ID])
        sections = cursor.fetchall()
        cursor.close()
        return render_template("register.html", sections=sections)

#Allows Dropping of classes
#Also works just need real user ID and some polish like better year
@takes_blueprint.route("/drop", methods=['POST', 'GET'])
def dropClass():
    student_ID = session.get("userID")
    
    if request.method == 'GET':
        #Gets all classes student is registered for
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, s.semester, s.year, s.section_ID FROM takes t JOIN section s on t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.year >= 2026",[student_ID])
        enrolled = cursor.fetchall()
        cursor.close()
        return render_template("drop.html", enrolled=enrolled)
    
    if request.method == 'POST':
        #Drops section entry from takes
        sec_ID = request.form['section_ID']
        cursor = dbserver.cursor()
        if sec_ID and student_ID:
            cursor.execute("DELETE FROM takes WHERE section_ID = %s and student_ID = %s",[sec_ID,student_ID])
            dbserver.commit()
        cursor.close()
        return redirect(url_for('dash'))

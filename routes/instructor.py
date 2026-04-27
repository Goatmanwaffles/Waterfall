from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from setup import dbserver

instructor_blueprint = Blueprint("instructor", __name__)

@instructor_blueprint.route("/edit_instructor", methods=["GET", "POST"])
def edit_instructor():
    # Keep this page restricted to administrators.
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        # handles all form actions
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            department_name = (request.form.get("department_name") or "").strip()
            salary = (request.form.get("salary") or "0").strip()

            cursor.execute("CALL create_instructor(%s, %s, %s, %s)",
                (first_name, last_name, department_name, salary))
            
            dbserver.commit()

        elif action == "update":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            department_name = (request.form.get("department_name") or "").strip()
            salary = (request.form.get("salary") or "0").strip()

            # update_student uses advisor_ID
            cursor.execute("CALL update_instructor(%s, %s, %s, %s, %s)",
                (instructor_id, first_name, last_name, department_name, salary))
            
            dbserver.commit()

        elif action == "delete":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            #CHECKS
            cursor.execute("SELECT COUNT(*) FROM teaches t WHERE t.instructor_ID = %s", [instructor_id])
            if cursor.fetchone()[0] > 0:
                flash("Cannot delete instructor - they still has active sections.", "error")
                return redirect(url_for("instructor.edit_instructor"))
            
            cursor.execute("CALL delete_instructor(%s)", (instructor_id,))
            dbserver.commit()

        # Redirect after POST to avoid duplicate form submissions on refresh
        cursor.close()
        return redirect(url_for("instructor.edit_instructor"))

    # Load current data for dropdowns/table rendering.
    cursor.execute(
        """
        SELECT i.instructor_ID, i.first_name, i.last_name, d.department_name, i.salary
        FROM instructor i
        LEFT JOIN department d ON d.department_ID = i.department_ID
        ORDER BY i.instructor_ID
        """
    )
    instructors = cursor.fetchall()

    cursor.execute(
        "SELECT department_ID, department_name FROM department ORDER BY department_name"
    )
    departments = cursor.fetchall()

    cursor.close()

    return render_template("edit_instructor.html", instructors=instructors, departments=departments)

#INSTRUCTOR STUFF
#--------------------------------------------------------------
#Instructor Grade Updating
@instructor_blueprint.route("/instructorGrades", methods=['POST', 'GET'])
def instructorGrades():
    Id = session.get("userID")
    if request.method == 'GET':
        #Pull all taught sections and grades
        cursor = dbserver.cursor()

        cursor.execute(
            """
            SELECT n.first_name, n.last_name, k.grades, c.title, s.semester, s.year, k.section_ID, k.student_ID
            FROM teaches t
            JOIN section s ON s.section_ID = t.section_ID
            JOIN course c ON s.course_ID = c.course_ID
            LEFT JOIN takes k ON k.section_ID = s.section_ID
            LEFT JOIN student n ON n.student_ID = k.student_ID
            WHERE t.instructor_ID = %s
            """
            , [Id])
        rows = cursor.fetchall()

        sections = {}

        #Formats Data nicely to pass to page
        for first, last, grade, title, semester, year, section_ID, student_ID in rows:
            if section_ID not in sections:
                sections[section_ID] = {
                    "section_ID": section_ID,
                    "course": title,
                    "semester": semester,
                    "year": year,
                    "students": []
                }

            sections[section_ID]["students"].append({
                "student_ID": student_ID,
                "first_name": first,
                "last_name": last,
                "grade": grade
            })
        cursor.close()
        return render_template("instructorGrades.html", sections=sections)

    if request.method =='POST':
        cursor = dbserver.cursor()
        section_ID = request.form['section_ID']
        student_ID = request.form['student_ID']
        newGrade = request.form['newGrade']

        cursor.execute("""
            UPDATE takes t 
            SET t.grades = %s 
            WHERE t.student_ID = %s AND t.section_ID = %s 
""",[newGrade, student_ID, section_ID])
        dbserver.commit()
        cursor.close()
        return redirect(url_for('instructor.instructorGrades'))

#EDIT PREREQS -------------------------------------------------
@instructor_blueprint.route("/edit_prereqs", methods=['GET', 'POST'])
def edit_prereqs():
    if request.method =='GET':
        cursor = dbserver.cursor()
        instructor_ID = session.get("userID")

        cursor.execute("""SELECT c.course_ID, c.title, pc.course_ID, pc.title
                       FROM course c
                       JOIN section s ON c.course_ID = s.course_ID 
                       JOIN teaches t ON t.section_ID = s.section_ID AND t.instructor_ID = %s
                       LEFT JOIN prereq p ON p.base_course_ID = c.course_ID
                       LEFT JOIN course pc ON p.requires_course_ID = pc.course_ID
                       """, [instructor_ID])
        rows = cursor.fetchall()
        courses = {}
        for course_ID, course_title, prereq_ID, prereq_title in rows:
            if course_ID not in courses:
                courses[course_ID] = {
                    "ID": course_ID,
                    "title": course_title,
                    "prereqs": []
                }

            if prereq_ID:
                courses[course_ID]["prereqs"].append({
                    "prereq_ID": prereq_ID,
                    "prereq_title": prereq_title
                })

        #Fetch all courses for updating prereqs
        cursor.execute("""SELECT c.title, c.course_ID
                        FROM course c
        """)
        rows = cursor.fetchall()
        listCourses = {}
        for title, cID in rows:
            listCourses[cID]= {
                "title": title,
                "ID": cID
            }
        cursor.close()
        return render_template("prereqs.html", courses=courses, listCourses=listCourses)
    
    if request.method == 'POST':
        #Currently only works for 1 prereq
        courseID = request.form['courseID']
        newPrereq = request.form['newPrereq']
        cursor=dbserver.cursor()
        cursor.execute("UPDATE prereq SET requires_course_ID = %s WHERE base_course_ID = %s",[newPrereq, courseID])
        dbserver.commit()
        cursor.close()
        return redirect(url_for("instructor.edit_prereqs"))
    
#VIEW AND EDIT CLASS ROSTERS
@instructor_blueprint.route("/classRosters", methods=['GET', 'POST'])
def editRosters():
    instructor_ID = session.get("userID")
    if request.method == 'GET':
        cursor = dbserver.cursor()
        cursor.execute(""" SELECT s.first_name, s.last_name, t.grades, sc.semester, sc.year, c.title, sc.section_ID, s.student_ID
                       FROM student s
                       JOIN takes t ON t.student_ID = s.student_ID
                       JOIN section sc ON sc.section_ID = t.section_ID
                       JOIN course c ON sc.course_ID = c.course_ID
                       JOIN teaches te ON te.section_ID = sc.section_ID AND te.instructor_ID = %s
                       
        """, [instructor_ID])
        rows = cursor.fetchall()
        rosters = {}
        for first, last, grade, semester, year, title, sec_ID, stu_ID in rows:
            if sec_ID not in rosters:
                rosters[sec_ID] ={
                    "section_ID": sec_ID,
                    "class_title": title,
                    "semester": semester,
                    "year": year,
                    "students": []
                }
            
            rosters[sec_ID]["students"].append({
                "ID": stu_ID,
                "name": f"{first} {last}",
                "grade": grade
            })

        cursor.close()
        return render_template("rosters.html", rosters=rosters)
    
    if request.method == 'POST':
        action=request.form['action']
        if action == "remove":
            cursor = dbserver.cursor()
            student = request.form['student_ID']
            section = request.form['section_ID']
            cursor.execute("DELETE FROM takes WHERE student_ID = %s AND section_ID = %s", [student, section])
            dbserver.commit()
            cursor.close()
            return redirect(url_for("instructor.editRosters"))
        
        elif action == "filter":
            semester = request.form.get('filterSemester')
            year = request.form['filterYear']
            
            cursor = dbserver.cursor()
            query = """ SELECT s.first_name, s.last_name, t.grades, sc.semester, sc.year, c.title, sc.section_ID, s.student_ID
                       FROM student s
                       JOIN takes t ON t.student_ID = s.student_ID
                       JOIN section sc ON sc.section_ID = t.section_ID
                       JOIN course c ON sc.course_ID = c.course_ID
                       JOIN teaches te ON te.section_ID = sc.section_ID AND te.instructor_ID = %s
                       WHERE 1=1
                    """
            params = [instructor_ID]

            if semester:
                query += "AND sc.semester = %s"
                params.append(semester)

            if year:
                query += "AND sc.year = %s"
                params.append(year)

            print("Query: " + query)
            print("Params: " + str(params))
            cursor.execute(query, params)
            rows = cursor.fetchall()

            rosters = {}
            for first, last, grade, semester, year, title, sec_ID, stu_ID in rows:
                if sec_ID not in rosters:
                    rosters[sec_ID] ={
                        "section_ID": sec_ID,
                        "class_title": title,
                        "semester": semester,
                        "year": year,
                        "students": []
                    }
                
                rosters[sec_ID]["students"].append({
                    "ID": stu_ID,
                    "name": f"{first} {last}",
                    "grade": grade
                })

        cursor.close()
        return render_template("rosters.html", rosters=rosters)
    
#Check Sections Teaching Based on Semster
@instructor_blueprint.route("/assignedClasses", methods=['GET'])
def assignedClasses():
    instructor_ID = session.get("userID")
    cursor = dbserver.cursor()
    cursor.execute("""
                   SELECT s.section_ID, c.title, s.semester, s.year, b.building_name, ti.day, ti.start_hr, ti.start_min, ti.end_hr, ti.end_min
                   FROM teaches t
                   JOIN section s ON s.section_ID = t.section_ID
                   JOIN course c ON s.course_ID = c.course_ID
                   JOIN time_slot ti ON ti.time_slot_ID = s.time_slot_ID
                   JOIN building b ON b.building_ID = s.building_ID
                   WHERE t.instructor_ID = %s
                   ORDER BY s.year DESC, s.semester, ti.day, ti.start_hr, ti.start_min
    """,[instructor_ID])
    rows = cursor.fetchall()

    classes = {}

    for section_ID, title, semester, year, building, day, sthr, stmn, endhr, endmin in rows:
        classes[section_ID]={
            "class": title,
            "semester": semester,
            "year": year,
            "building": building,
            "timeslot": f"{day} - {sthr}:{stmn} - {endhr}:{endmin}" 
        }
    return render_template("assignedClasses.html", classes=classes)
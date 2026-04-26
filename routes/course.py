from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

course_blueprint = Blueprint("course", __name__)

@course_blueprint.route("/edit_course", methods=["GET", "POST"])
def edit_course():
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            title = (request.form.get("title") or "").strip()
            department_id = (request.form.get("department_id") or "").strip()
            credits = (request.form.get("credits") or "0").strip()

            cursor.execute(
                "INSERT INTO course (title, department_ID, credits) VALUES (%s, %s, %s)",
                (title, department_id, credits),
            )
            dbserver.commit()

        elif action == "update":
            course_id = (request.form.get("course_id") or "").strip()
            title = (request.form.get("title") or "").strip()
            department_id = (request.form.get("department_id") or "").strip()
            credits = (request.form.get("credits") or "0").strip()

            cursor.execute(
                """
                UPDATE course
                SET title = %s,
                    department_ID = %s,
                    credits = %s
                WHERE course_ID = %s
                """,
                (title, department_id, credits, course_id),
            )
            dbserver.commit()

        elif action == "delete":
            course_id = (request.form.get("course_id") or "").strip()
            cursor.execute("DELETE FROM course WHERE course_ID = %s", (course_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("course.edit_course"))

    cursor.execute(
        """
        SELECT
            c.course_ID,
            c.title,
            d.department_name,
            c.credits
        FROM course c
        LEFT JOIN department d ON d.department_ID = c.department_ID
        ORDER BY c.course_ID
        """
    )
    courses = cursor.fetchall()

    cursor.execute(
        "SELECT department_ID, department_name FROM department ORDER BY department_name"
    )
    departments = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_course.html",
        courses=courses,
        departments=departments,
    )

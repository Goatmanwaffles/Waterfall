from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

teaches_blueprint = Blueprint("teaches", __name__)

@teaches_blueprint.route("/edit_teaches", methods=["GET", "POST"])
def edit_teaches():
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            section_id = (request.form.get("section_id") or "").strip()

            cursor.execute(
                "INSERT INTO teaches (instructor_ID, section_ID) VALUES (%s, %s)",
                (instructor_id, section_id),
            )
            dbserver.commit()

        elif action == "update":
            old_instructor_id = (request.form.get("old_instructor_id") or "").strip()
            old_section_id = (request.form.get("old_section_id") or "").strip()
            instructor_id = (request.form.get("instructor_id") or "").strip()
            section_id = (request.form.get("section_id") or "").strip()

            cursor.execute(
                """
                UPDATE teaches
                SET instructor_ID = %s,
                    section_ID = %s
                WHERE instructor_ID = %s
                    AND section_ID = %s
                """,
                (instructor_id, section_id, old_instructor_id, old_section_id),
            )
            dbserver.commit()

        elif action == "delete":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            section_id = (request.form.get("section_id") or "").strip()

            cursor.execute(
                "DELETE FROM teaches WHERE instructor_ID = %s AND section_ID = %s",
                (instructor_id, section_id),
            )
            dbserver.commit()

        cursor.close()
        return redirect(url_for("teaches.edit_teaches"))

    cursor.execute(
        """
        SELECT
            t.instructor_ID,
            i.first_name,
            i.last_name,
            t.section_ID,
            s.course_ID,
            c.title,
            s.semester,
            s.year
        FROM teaches t
        LEFT JOIN instructor i ON i.instructor_ID = t.instructor_ID
        LEFT JOIN section s ON s.section_ID = t.section_ID
        LEFT JOIN course c ON c.course_ID = s.course_ID
        ORDER BY t.instructor_ID, t.section_ID
        """
    )
    teaches_rows = cursor.fetchall()

    cursor.execute(
        """
        SELECT instructor_ID, first_name, last_name
        FROM instructor
        ORDER BY instructor_ID
        """
    )
    instructors = cursor.fetchall()

    cursor.execute(
        """
        SELECT s.section_ID, s.course_ID, c.title, s.semester, s.year
        FROM section s
        LEFT JOIN course c ON c.course_ID = s.course_ID
        ORDER BY s.section_ID
        """
    )
    sections = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_teaches.html",
        teaches_rows=teaches_rows,
        instructors=instructors,
        sections=sections,
    )

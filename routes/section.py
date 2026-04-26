from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

section_blueprint = Blueprint("section", __name__)

@section_blueprint.route("/edit_section", methods=["GET", "POST"])
def edit_section():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            course_id = (request.form.get("course_id") or "").strip()
            semester = (request.form.get("semester") or "").strip()
            year = (request.form.get("year") or "0").strip()
            building_id = (request.form.get("building_id") or "").strip()
            time_slot_id = (request.form.get("time_slot_id") or "").strip()

            cursor.execute(
                "CALL create_section(%s, %s, %s, %s, %s)",
                (course_id, semester, year, building_id, time_slot_id),
            )
            dbserver.commit()

        elif action == "update":
            section_id = (request.form.get("section_id") or "").strip()
            course_id = (request.form.get("course_id") or "").strip()
            semester = (request.form.get("semester") or "").strip()
            year = (request.form.get("year") or "0").strip()
            building_id = (request.form.get("building_id") or "").strip()
            time_slot_id = (request.form.get("time_slot_id") or "").strip()

            cursor.execute(
                "CALL update_section(%s, %s, %s, %s, %s, %s)",
                (section_id, course_id, semester, year, building_id, time_slot_id),
            )
            dbserver.commit()

        elif action == "delete":
            section_id = (request.form.get("section_id") or "").strip()
            course_id = (request.form.get("course_id") or "").strip()
            semester = (request.form.get("semester") or "").strip()
            year = (request.form.get("year") or "0").strip()

            cursor.execute(
                "CALL delete_section(%s, %s, %s, %s)",
                (course_id, section_id, semester, year),
            )
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_section"))

    cursor.execute(
        """
        SELECT
            s.section_ID,
            s.course_ID,
            c.title,
            s.semester,
            s.year,
            s.building_ID,
            b.building_name,
            s.time_slot_ID
        FROM section s
        LEFT JOIN course c ON c.course_ID = s.course_ID
        LEFT JOIN building b ON b.building_ID = s.building_ID
        ORDER BY s.section_ID
        """
    )
    sections = cursor.fetchall()

    cursor.execute("SELECT course_ID, title FROM course ORDER BY course_ID")
    courses = cursor.fetchall()

    cursor.execute("SELECT building_ID, building_name FROM building ORDER BY building_ID")
    buildings = cursor.fetchall()

    cursor.execute(
        """
        SELECT time_slot_ID, day, start_hr, start_min, end_hr, end_min
        FROM time_slot
        ORDER BY time_slot_ID
        """
    )
    time_slots = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_section.html",
        sections=sections,
        courses=courses,
        buildings=buildings,
        time_slots=time_slots,
    )


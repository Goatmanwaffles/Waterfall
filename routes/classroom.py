from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

classroom_blueprint = Blueprint("classroom", __name__)

@classroom_blueprint.route("/edit_classroom", methods=["GET", "POST"])
def edit_classroom():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            building_id = (request.form.get("building_id") or "").strip()
            room_number = (request.form.get("room_number") or "0").strip()
            capacity = (request.form.get("capacity") or "0").strip()

            cursor.execute(
                "INSERT INTO classroom (building_ID, room_number, capacity) VALUES (%s, %s, %s)",
                (building_id, room_number, capacity),
            )
            dbserver.commit()

        elif action == "update":
            classroom_id = (request.form.get("classroom_id") or "").strip()
            building_id = (request.form.get("building_id") or "").strip()
            room_number = (request.form.get("room_number") or "0").strip()
            capacity = (request.form.get("capacity") or "0").strip()

            cursor.execute(
                """
                UPDATE classroom
                SET building_ID = %s,
                    room_number = %s,
                    capacity = %s
                WHERE classroom_ID = %s
                """,
                (building_id, room_number, capacity, classroom_id),
            )
            dbserver.commit()

        elif action == "delete":
            classroom_id = (request.form.get("classroom_id") or "").strip()
            cursor.execute("DELETE FROM classroom WHERE classroom_ID = %s", (classroom_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_classroom"))

    cursor.execute(
        """
        SELECT
            c.classroom_ID,
            c.building_ID,
            b.building_name,
            c.room_number,
            c.capacity
        FROM classroom c
        LEFT JOIN building b ON b.building_ID = c.building_ID
        ORDER BY c.classroom_ID
        """
    )
    classrooms = cursor.fetchall()

    cursor.execute("SELECT building_ID, building_name FROM building ORDER BY building_ID")
    buildings = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_classroom.html",
        classrooms=classrooms,
        buildings=buildings,
    )

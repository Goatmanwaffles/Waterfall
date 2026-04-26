from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

time_slot_blueprint = Blueprint("time_slot", __name__)

@time_slot_blueprint.route("/edit_time_slot", methods=["GET", "POST"])
def edit_time_slot():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            day = (request.form.get("day") or "").strip()
            start_hr = (request.form.get("start_hr") or "0").strip()
            start_min = (request.form.get("start_min") or "0").strip()
            end_hr = (request.form.get("end_hr") or "0").strip()
            end_min = (request.form.get("end_min") or "0").strip()

            cursor.execute(
                """
                INSERT INTO time_slot (day, start_hr, start_min, end_hr, end_min)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (day, start_hr, start_min, end_hr, end_min),
            )
            dbserver.commit()

        elif action == "update":
            time_slot_id = (request.form.get("time_slot_id") or "").strip()
            day = (request.form.get("day") or "").strip()
            start_hr = (request.form.get("start_hr") or "0").strip()
            start_min = (request.form.get("start_min") or "0").strip()
            end_hr = (request.form.get("end_hr") or "0").strip()
            end_min = (request.form.get("end_min") or "0").strip()

            cursor.execute(
                """
                UPDATE time_slot
                SET day = %s,
                    start_hr = %s,
                    start_min = %s,
                    end_hr = %s,
                    end_min = %s
                WHERE time_slot_ID = %s
                """,
                (day, start_hr, start_min, end_hr, end_min, time_slot_id),
            )
            dbserver.commit()

        elif action == "delete":
            time_slot_id = (request.form.get("time_slot_id") or "").strip()
            cursor.execute("DELETE FROM time_slot WHERE time_slot_ID = %s", (time_slot_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_time_slot"))

    cursor.execute(
        """
        SELECT
            time_slot_ID,
            day,
            start_hr,
            start_min,
            end_hr,
            end_min
        FROM time_slot
        ORDER BY time_slot_ID
        """
    )
    time_slots = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_time_slot.html",
        time_slots=time_slots,
    )


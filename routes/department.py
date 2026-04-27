from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from setup import dbserver

department_blueprint = Blueprint("department", __name__)

@department_blueprint.route("/edit_department", methods=["GET", "POST"])
def edit_department():
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            department_name = (request.form.get("department_name") or "").strip()
            building_id = (request.form.get("building_id") or "").strip()
            budget = (request.form.get("budget") or "0").strip()

            building_id_value = int(building_id) if building_id else None

            cursor.execute(
                "INSERT INTO department (department_name, building_ID, budget) VALUES (%s, %s, %s)",
                (department_name, building_id_value, budget),
            )
            dbserver.commit()

        elif action == "update":
            department_id = (request.form.get("department_id") or "").strip()
            department_name = (request.form.get("department_name") or "").strip()
            building_id = (request.form.get("building_id") or "").strip()
            budget = (request.form.get("budget") or "0").strip()

            building_id_value = int(building_id) if building_id else None

            cursor.execute(
                """
                UPDATE department
                SET department_name = %s, building_ID = %s, budget = %s
                WHERE department_ID = %s
                """,
                (department_name, building_id_value, budget, department_id),
            )
            dbserver.commit()

        elif action == "delete":
            department_id = (request.form.get("department_id") or "").strip()

            cursor.execute("SELECT COUNT(*) FROM instructor s WHERE s.department_ID = %s", [department_id])
            if cursor.fetchone()[0] > 0:
                flash("Cannot delete department - it still has active instructors.", "error")
                return redirect(url_for("department.edit_department"))
            
            cursor.execute("SELECT COUNT(*) FROM student s WHERE s.department_ID = %s", [department_id])
            if cursor.fetchone()[0] > 0:
                flash("Cannot delete department - it still has active students.", "error")
                return redirect(url_for("department.edit_department"))
            
            cursor.execute("SELECT COUNT(*) FROM course s WHERE s.department_ID = %s", [department_id])
            if cursor.fetchone()[0] > 0:
                flash("Cannot delete department - it still has active courses.", "error")
                return redirect(url_for("department.edit_department"))
            
            cursor.execute("DELETE FROM department WHERE department_ID = %s", (department_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("department.edit_department"))

    cursor.execute(
        """
        SELECT d.department_ID, d.department_name, d.building_ID, b.building_name, d.budget
        FROM department d
        LEFT JOIN building b ON b.building_ID = d.building_ID
        ORDER BY d.department_ID
        """
    )
    departments = cursor.fetchall()

    cursor.execute("SELECT building_ID, building_name FROM building ORDER BY building_ID")
    buildings = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_department.html",
        departments=departments,
        buildings=buildings,
    )

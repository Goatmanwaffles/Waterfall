from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

advisor_blueprint = Blueprint("advisor", __name__)

#STUDENT CHECK ADVISOR
@advisor_blueprint.route("/advisorInfo", methods=['GET'])
def getAdvisorInfo():
    student_ID = session.get("userID")
    print(student_ID)
    cursor = dbserver.cursor()
    cursor.execute("SELECT a2.first_name, a2.last_name, d.department_name FROM advises a JOIN advisor a2 ON a.advisor_ID = a2.advisor_ID JOIN department d ON d.department_ID = a2.department_ID WHERE a.student_ID = %s",[student_ID])
    advisor = cursor.fetchone()
    cursor.close()
    return render_template("studentAdvisor.html", advisor=advisor)

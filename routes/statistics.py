from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

statistics_blueprint = Blueprint("statistics", __name__)


GRADE_POINTS_SQL = """
CASE t.grades
    WHEN 'A+' THEN 4.0
    WHEN 'A' THEN 4.0
    WHEN 'A-' THEN 3.7
    WHEN 'B+' THEN 3.3
    WHEN 'B' THEN 3.0
    WHEN 'B-' THEN 2.7
    WHEN 'C+' THEN 2.3
    WHEN 'C' THEN 2.0
    WHEN 'C-' THEN 1.7
    WHEN 'D+' THEN 1.3
    WHEN 'D' THEN 1.0
    WHEN 'D-' THEN 0.7
    WHEN 'F' THEN 0.0
    ELSE NULL
END
"""


SECTION_TERM_ORDER_SQL = """
CASE s.semester
    WHEN 'Winter' THEN 1
    WHEN 'Spring' THEN 2
    WHEN 'Summer' THEN 3
    WHEN 'Fall' THEN 4
END
"""


@statistics_blueprint.route("/statistics", methods=['POST', 'GET'])
def statistics():
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()
    
    #####
    # PAST AND CURRENT STUDENTS
    #####

    # Gets department name and the number of students in the department
    cursor.execute("""
    SELECT department_name,
        (
            SELECT COUNT(*)
            FROM student
            WHERE student.department_ID = department.department_ID
        ) AS student_count
    FROM department;
    """)
    student_count = cursor.fetchall()

    # Gets lists of classes with and without students
    has_students = []
    no_students  = []
    for student in student_count:
        if student[1] != 0:
            has_students.append([student[0], student[1]])
        else:
            no_students.append(student[0])

    #####
    # CURRENT STUDENTS
    #####

    # Gets department name and the number of students in the department
    cursor.execute("""
    SELECT department.department_name,
    (
        SELECT COUNT(DISTINCT st.student_ID)
        FROM student st
        JOIN takes t ON st.student_ID = t.student_ID
        JOIN section sec ON t.section_ID = sec.section_ID
        WHERE sec.semester = "Spring"
            AND sec.year = 2026
            AND st.department_ID = department.department_ID
    ) AS student_count
    FROM department;
    """)
    current_student_count = cursor.fetchall()

    # Gets lists of classes with and without students
    current_has_students = []
    current_no_students  = []
    for student in current_student_count:
        if student[1] != 0:
            current_has_students.append([student[0], student[1]])
        else:
            current_no_students.append(student[0])

    #####
    # GRADE STATISTICS
    #####

    # Gets average grade points for each department.
    cursor.execute(
        f"""
        SELECT
            d.department_ID,
            d.department_name,
            ROUND(AVG({GRADE_POINTS_SQL}), 2) AS avg_grade
        FROM department d
        LEFT JOIN student st ON st.department_ID = d.department_ID
        LEFT JOIN takes t ON t.student_ID = st.student_ID
        GROUP BY d.department_ID, d.department_name
        ORDER BY d.department_name
        """
    )
    department_grade_stats = cursor.fetchall()

    # Gets courses used in the class-range selector.
    cursor.execute(
        """
        SELECT course_ID, title
        FROM course
        ORDER BY course_ID
        """
    )
    courses = cursor.fetchall()

    selected_course_id = (request.form.get("course_id") or "").strip()
    start_semester = (request.form.get("start_semester") or "Spring").strip()
    start_year = (request.form.get("start_year") or "2025").strip()
    end_semester = (request.form.get("end_semester") or "Spring").strip()
    end_year = (request.form.get("end_year") or "2026").strip()
    selected_semester = (request.form.get("selected_semester") or "Spring").strip()
    selected_year = (request.form.get("selected_year") or "2026").strip()

    if request.method == "GET" and courses:
        selected_course_id = str(courses[0][0])

    class_range_results = []
    best_classes = []
    worst_classes = []

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "class_range":
            cursor.execute(
                f"""
                SELECT c.course_ID, c.title, ROUND(AVG({GRADE_POINTS_SQL}), 2) AS avg_grade, COUNT(*) AS graded_count
                FROM takes t
                JOIN section s ON s.section_ID = t.section_ID
                JOIN course c ON c.course_ID = s.course_ID
                WHERE c.course_ID = %s
                    AND (s.year * 10 + {SECTION_TERM_ORDER_SQL}) BETWEEN
                        (%s * 10 + CASE %s
                            WHEN 'Winter' THEN 1
                            WHEN 'Spring' THEN 2
                            WHEN 'Summer' THEN 3
                            WHEN 'Fall' THEN 4
                        END)
                        AND
                        (%s * 10 + CASE %s
                            WHEN 'Winter' THEN 1
                            WHEN 'Spring' THEN 2
                            WHEN 'Summer' THEN 3
                            WHEN 'Fall' THEN 4
                        END)
                    AND {GRADE_POINTS_SQL} IS NOT NULL
                GROUP BY c.course_ID, c.title
                """,
                (selected_course_id, start_year, start_semester, end_year, end_semester)
            )
            class_range_results = cursor.fetchall()

        elif action == "best_worst":
            cursor.execute(
                f"""
                SELECT c.course_ID, c.title, ROUND(AVG({GRADE_POINTS_SQL}), 2) AS avg_grade, COUNT(*) AS graded_count
                FROM takes t
                JOIN section s ON s.section_ID = t.section_ID
                JOIN course c ON c.course_ID = s.course_ID
                WHERE s.semester = %s
                    AND s.year = %s
                    AND {GRADE_POINTS_SQL} IS NOT NULL
                GROUP BY c.course_ID, c.title
                ORDER BY avg_grade DESC, graded_count DESC
                LIMIT 3
                """,
                (selected_semester, selected_year),
            )
            best_classes = cursor.fetchall()

            cursor.execute(
                f"""
                SELECT
                    c.course_ID,
                    c.title,
                    ROUND(AVG({GRADE_POINTS_SQL}), 2) AS avg_grade,
                    COUNT(*) AS graded_count
                FROM takes t
                JOIN section s ON s.section_ID = t.section_ID
                JOIN course c ON c.course_ID = s.course_ID
                WHERE s.semester = %s
                    AND s.year = %s
                    AND {GRADE_POINTS_SQL} IS NOT NULL
                GROUP BY c.course_ID, c.title
                ORDER BY avg_grade ASC, graded_count DESC
                LIMIT 3
                """,
                (selected_semester, selected_year),
            )
            worst_classes = cursor.fetchall()

    cursor.close()
    return render_template(
            'statistics.html',
            student_count=student_count,
            has_students=has_students,
            no_students=no_students,
            current_has_students=current_has_students,
            current_no_students=current_no_students,
            department_grade_stats=department_grade_stats,
            courses=courses,
            selected_course_id=selected_course_id,
            start_semester=start_semester,
            start_year=start_year,
            end_semester=end_semester,
            end_year=end_year,
            selected_semester=selected_semester,
            selected_year=selected_year,
            class_range_results=class_range_results,
            best_classes=best_classes,
            worst_classes=worst_classes
            )

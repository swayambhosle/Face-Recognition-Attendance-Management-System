from flask import Flask, render_template, request, redirect, url_for, session as flask_session, send_file
from datetime import datetime
import os
import pandas as pd
from io import BytesIO

from models import db, User, Student, AttendanceSession, AttendanceRecord
from face_utils import register_face_for_student, run_attendance_for_session


app = Flask(__name__)
app.secret_key = "change_this_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "attendance.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

db.init_app(app)


def setup_database():
    """Create tables and default admin user."""
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password="admin", role="admin")
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: username=admin, password=admin")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("username", "").strip()
        pwd = request.form.get("password", "").strip()
        print("Login POST:", uname, pwd)

        user = User.query.filter_by(username=uname, password=pwd).first()

        if user:
            flask_session["user_id"] = user.id
            flask_session["role"] = user.role
            flask_session["username"] = user.username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect(url_for("login"))


def login_required():
    return "user_id" in flask_session


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/students", methods=["GET", "POST"])
def students():
    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        class_name = request.form.get("class_name", "").strip()

        if roll_no and name and class_name:
            existing = Student.query.filter_by(roll_no=roll_no).first()
            if not existing:
                s = Student(roll_no=roll_no, name=name, class_name=class_name)
                db.session.add(s)
                db.session.commit()
        return redirect(url_for("students"))

    all_students = Student.query.all()
    return render_template("students.html", students=all_students)


@app.route("/register_face/<int:student_id>")
def register_face(student_id):
    if not login_required():
        return redirect(url_for("login"))

    register_face_for_student(student_id)
    return redirect(url_for("students"))


@app.route("/start_session", methods=["GET", "POST"])
def start_session():
    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        class_name = request.form.get("class_name", "").strip()
        subject = request.form.get("subject", "").strip()
        faculty_name = flask_session.get("username", "Faculty")

        if class_name and subject:
            sess = AttendanceSession(
                class_name=class_name,
                subject=subject,
                faculty_name=faculty_name,
                date=datetime.utcnow().date(),
                start_time=datetime.utcnow().time(),
            )
            db.session.add(sess)
            db.session.commit()

            # open camera and mark attendance
            run_attendance_for_session(sess.id)

            sess.end_time = datetime.utcnow().time()
            db.session.commit()

            return redirect(url_for("dashboard"))

    return render_template("start_session.html")

@app.route("/export/session/<int:session_id>")
def export_session_excel(session_id):
    if "user_id" not in flask_session:
        return redirect(url_for("login"))

    session_obj = AttendanceSession.query.get(session_id)
    if not session_obj:
        return "Session not found", 404

    records = AttendanceRecord.query.filter_by(session_id=session_id).all()
    students = {s.id: s for s in Student.query.all()}

    data = []
    for r in records:
        stu = students.get(r.student_id)
        if not stu:
            continue


        date_str = session_obj.date.strftime("%d-%m-%Y") if session_obj.date else ""
        time_str = r.timestamp.strftime("%d-%m-%Y %H:%M:%S") if r.timestamp else ""

        data.append({
            "Session ID": session_obj.id,
            "Date": date_str,
            "Class": session_obj.class_name,
            "Subject": session_obj.subject,
            "Faculty": session_obj.faculty_name,
            "Student Name": stu.name,
            "Roll No": stu.roll_no,
            "Status": r.status,
            "Marked At": time_str,
        })

    if not data:
        return "No records for this session", 404

    df = pd.DataFrame(data)

    # Create Excel in memory (no temp file needed)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Attendance")
    output.seek(0)

    filename = f"attendance_session_{session_id}.xlsx"

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route("/attendance")
def view_attendance():
    if not login_required():
        return redirect(url_for("login"))

    sessions = AttendanceSession.query.order_by(AttendanceSession.id.desc()).all()
    records = AttendanceRecord.query.all()
    students = {s.id: s for s in Student.query.all()}

    return render_template(
        "view_attendance.html",
        sessions=sessions,
        records=records,
        students=students,
    )


if __name__ == "__main__":
    setup_database()
    app.run(host="0.0.0.0", port=5000, debug=True)


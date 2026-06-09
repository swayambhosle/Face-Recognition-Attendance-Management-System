from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # plain for now (for demo)
    role = db.Column(db.String(20), nullable=False)       # 'admin' or 'faculty'


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)  # e.g. "TE AI A"

    encodings = db.relationship("FaceEncoding", backref="student", lazy=True)
    records = db.relationship("AttendanceRecord", backref="student", lazy=True)


class FaceEncoding(db.Model):
    __tablename__ = "face_encodings"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)  # path to .npy file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AttendanceSession(db.Model):
    __tablename__ = "attendance_sessions"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    faculty_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    start_time = db.Column(db.Time, default=datetime.utcnow().time)
    end_time = db.Column(db.Time, nullable=True)

    records = db.relationship("AttendanceRecord", backref="session", lazy=True)


class AttendanceRecord(db.Model):
    __tablename__ = "attendance_records"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="present")  # present/absent
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from models import Student, FaceEncoding, AttendanceRecord, AttendanceSession, db

FACES_DIR = "student_faces"
os.makedirs(FACES_DIR, exist_ok=True)


def register_face_for_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        print("Student not found.")
        return False

    cam = cv2.VideoCapture(0)
    captured_images = []
    print("Press 'c' to capture image, 'q' to finish")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        cv2.imshow("Register Face - Student: " + student.name, frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            captured_images.append(frame.copy())
            print(f"Captured {len(captured_images)} image(s)")
        elif key == ord('q'):
            break

        if len(captured_images) >= 5:
            break

    cam.release()
    cv2.destroyAllWindows()

    encodings = []
    for img in captured_images:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        if len(boxes) == 0:
            continue
        face_enc = face_recognition.face_encodings(rgb, boxes)[0]
        encodings.append(face_enc)

    if not encodings:
        print("No face detected. Try again.")
        return False

    avg_encoding = np.mean(encodings, axis=0)
    file_path = os.path.join(FACES_DIR, f"{student_id}.npy")
    np.save(file_path, avg_encoding)

    fe = FaceEncoding(student_id=student_id, file_path=file_path)
    db.session.add(fe)
    db.session.commit()

    print(f"Face registered for {student.name}")
    return True


def load_known_faces():
    encodings = []
    ids = []

    all_fe = FaceEncoding.query.all()
    for fe in all_fe:
        if os.path.exists(fe.file_path):
            enc = np.load(fe.file_path)
            encodings.append(enc)
            ids.append(fe.student_id)

    return encodings, ids


def run_attendance_for_session(session_id, threshold=0.45):
    session = AttendanceSession.query.get(session_id)
    if not session:
        print("Session not found")
        return

    known_encodings, known_ids = load_known_faces()
    if not known_encodings:
        print("No registered faces found.")
        return

    cam = cv2.VideoCapture(0)
    marked_present = set()

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, boxes)

        for box, enc in zip(boxes, encs):
            distances = face_recognition.face_distance(known_encodings, enc)
            if len(distances) == 0:
                continue

            min_idx = np.argmin(distances)
            min_dist = distances[min_idx]

            if min_dist < threshold:
                student_id = known_ids[min_idx]
                top, right, bottom, left = box

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                student = Student.query.get(student_id)
                label = student.roll_no if student else str(student_id)
                cv2.putText(frame, label, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if student_id not in marked_present:
                    marked_present.add(student_id)
                    record = AttendanceRecord(
                        session_id=session_id,
                        student_id=student_id,
                        status="present"
                    )
                    db.session.add(record)
                    db.session.commit()
                    print(f"Marked present: {student_id} at {datetime.now()}")

        cv2.imshow("Attendance Session", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Session ended. Present:", marked_present)

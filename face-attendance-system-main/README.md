<div align="center">

<!-- Animated Typing Hero -->
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&multiline=true&repeat=true&width=900&height=100&lines=%F0%9F%94%8D+Face+Recognition+Attendance+Management+System;Powered+by+Computer+Vision+%26+Deep+Learning" alt="Typing SVG" /></a>

<br/>

<!-- Shields.io Badges -->
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00D9FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-00E676?style=for-the-badge)

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

<br/>

**A production-ready attendance automation system that uses real-time face recognition to identify students, log session-based attendance with timestamps, and export structured reports — no manual roll calls, no proxy attendance.**

<br/>

[📂 Explore Code](#-project-structure) · [🚀 Get Started](#-installation)

</div>

<br/>

---

<br/>

## 🧠 Overview

Traditional attendance systems are slow, error-prone, and easily manipulated. This project replaces that entirely.

Built with **Python**, **Flask**, and the **face_recognition** library (powered by dlib's deep metric learning), this system captures facial encodings during registration — not raw images — and uses them to identify students in real time via webcam or IP camera feeds.

Each attendance record is tied to a specific **session** (Class, Subject, Faculty, Date & Time), making it auditable and structured. Reports export cleanly to **Excel (.xlsx)**, ready for institutional use.

The entire system runs from a **mobile browser** on the same network — meaning a faculty member can walk into a classroom, open their phone, and start marking attendance hands-free.

> **No cloud dependency. No external APIs. Fully offline. Fully yours.**

<br/>

---

<br/>

## ⚡ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- 🔐 **Face Registration** — Capture & store 128-d face encodings (no raw images retained)
- 👁️ **Real-Time Recognition** — Live identification via webcam or IP camera
- 📋 **Session-Based Logging** — Attendance linked to Class, Subject, Faculty, Date & Time
- 📊 **Excel Export** — One-click `.xlsx` reports per session via Pandas + openpyxl
- 📱 **Mobile Accessible** — Full control from any device on the same Wi-Fi/hotspot

</td>
<td width="50%">

### 🛡️ Design Principles
- 🚫 **Anti-Proxy** — Biometric verification eliminates buddy punching
- 🔒 **Privacy-First** — Only mathematical encodings stored, never photographs
- ⚡ **Lightweight** — SQLite backend, zero external service dependencies
- 🌐 **Network-Ready** — Flask serves over LAN for multi-device access
- 🧩 **Modular Codebase** — Clean separation of routes, models, and face utilities

</td>
</tr>
</table>

<br/>

---

<br/>

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Role |
|:---:|:---:|:---:|
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core runtime & scripting |
| **Web Framework** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | HTTP server, routing, templates |
| **Computer Vision** | ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) | Camera capture & frame processing |
| **Face Recognition** | ![dlib](https://img.shields.io/badge/face__recognition-FF6F00?style=flat-square&logo=deeplearning.ai&logoColor=white) | Deep metric learning face encodings |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Lightweight persistent storage |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white) | Database abstraction & queries |
| **Data Export** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) | DataFrame processing & Excel export |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) | UI templates & styling |

</div>

<br/>

---

<br/>

## 📁 Project Structure

```
face_attendance/
│
├── app.py                 # Flask application — routes, session logic, server config
├── models.py              # SQLAlchemy models — Student, Session, Attendance tables
├── face_utils.py          # Face registration & recognition — encoding, matching
├── requirements.txt       # Python dependencies
│
├── templates/             # Jinja2 HTML templates
│   ├── login.html         # Faculty authentication
│   ├── dashboard.html     # Session management & controls
│   ├── register.html      # Student face registration
│   ├── attendance.html    # Live recognition feed & results
│   └── report.html        # Attendance reports & export
│
├── static/                # CSS, JS, and static assets
│   ├── css/
│   └── js/
│
└── instance/              # Auto-generated SQLite database
    └── attendance.db
```

<br/>

---

<br/>

## 🔧 Installation

### Prerequisites

- Python **3.8+**
- pip (Python package manager)
- Webcam or IP camera (for live recognition)
- CMake & C++ compiler (required by `dlib`)

### Setup

```bash
# Clone the repository
git clone https://github.com/swayambhosle/Face-Recognition-Attendance-Management-System.git
cd Face-Recognition-Attendance-Management-System/face-attendance-system-main

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Launch the application
python app.py
```

> **Note:** If `dlib` installation fails, ensure CMake is installed:
> ```bash
> pip install cmake
> pip install dlib
> ```

<br/>

---

<br/>

## 🖥️ Usage

### 1️⃣ Start the Server
```bash
python app.py
```
The Flask server starts at `http://127.0.0.1:5000` by default.

### 2️⃣ Register Students
Navigate to the registration page → Enter student details → Capture face via webcam → Face encoding is computed and stored.

### 3️⃣ Start an Attendance Session
Create a new session with **Class**, **Subject**, and **Faculty** details → The system activates the camera feed for recognition.

### 4️⃣ Automatic Recognition
Students face the camera → The system matches faces against stored encodings in real time → Attendance is logged with a timestamp.

### 5️⃣ Export Reports
Download session-specific attendance as an **Excel (.xlsx)** file — ready for submission or archival.

### 📱 Mobile Access
Connect your phone to the same Wi-Fi/hotspot → Open `http://<server-ip>:5000` → Full control from your mobile browser.

<br/>

---

<br/>

## 📸 Screenshots

<div align="center">

*Add your application screenshots here to showcase your project UI.*

</div>

<br/>

---

<br/>

## 🔮 Future Improvements

| Priority | Enhancement | Description |
|:---:|---|---|
| 🔴 | **Multi-Camera Support** | Simultaneous feeds for larger classrooms |
| 🔴 | **Anti-Spoofing / Liveness Detection** | Prevent photo/video-based impersonation |
| 🟡 | **Role-Based Access Control** | Admin, Faculty, and Student permission tiers |
| 🟡 | **Cloud Deployment** | Docker containerization + cloud hosting (AWS/GCP) |
| 🟢 | **Dashboard Analytics** | Attendance trends, heatmaps, and per-student history |
| 🟢 | **Notification System** | Email/SMS alerts for absent students |
| 🟢 | **REST API Layer** | Expose endpoints for third-party integrations |

<br/>

---

<br/>

## 🤝 Contributing

Contributions are welcome — whether it's a bug fix, feature request, or documentation improvement.

```
1. Fork the repository
2. Create your feature branch        →  git checkout -b feature/your-feature
3. Commit your changes               →  git commit -m "Add: your feature description"
4. Push to the branch                →  git push origin feature/your-feature
5. Open a Pull Request
```

Please ensure your code follows the existing project structure and includes relevant documentation.

<br/>

---

<br/>

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

See the [LICENSE](LICENSE) file for full details.

<br/>

---

<br/>

## 👨‍💻 About the Developer

<div align="center">

<img src="https://github.com/swayambhosle.png" width="140" style="border-radius: 50%;" alt="Swayam Bhosle"/>

### **Swayam Bhosle**

*AI & Data Science Engineering Student*

</div>

<br/>

I'm passionate about building things that sit at the intersection of **Artificial Intelligence**, **Computer Vision**, and **real-world problem solving**. My work spans across Data Science, Cybersecurity, and developing technology solutions that actually make a difference — not just in theory, but in classrooms, workplaces, and everyday systems.

This project started as a way to solve a genuine pain point I observed — inefficient, gameable attendance systems — and grew into a full-stack computer vision application that works in production environments.

I believe the best way to learn is to build. And the best way to build is to solve problems worth solving.

<br/>

---

<br/>

## 🌐 Connect with Me

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-swayambhosle-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/swayambhosle)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Swayam_Bhosle-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/swayam-bhosle/)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:00D9FF,100:0D1117&height=120&section=footer" width="100%"/>

</div>

# add_assignments_and_branding.py
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.json')
SUBMISSIONS_FILE = os.path.join(DATA_DIR, 'assignment_submissions.json')

# ==============================================================================
# 1. Initialize data/assignments.json & data/assignment_submissions.json
# ==============================================================================

os.makedirs(DATA_DIR, exist_ok=True)

default_assignments = [
    {
        "id": "ASG-CS401",
        "course_code": "CS401",
        "subject": "Python Programming",
        "title": "Phase-1 Capstone Project Architecture & Documentation",
        "correspondent_faculty_id": "50102",
        "correspondent_faculty_name": "Prof. V. Priya",
        "department": "Department of Computer Science & Engineering",
        "due_date": "15-Oct-2026",
        "max_marks": 30,
        "accepted_formats": ".pdf, .doc, .docx",
        "instructions": "Submit architectural design, component diagrams, algorithm flow, and Python proof-of-concept for your capstone project."
    },
    {
        "id": "ASG-CS402",
        "course_code": "CS402",
        "subject": "Data Structures",
        "title": "AVL Tree Rotations & Shortest Path Problem Set",
        "correspondent_faculty_id": "50101",
        "correspondent_faculty_name": "Dr. A. K. Sharma",
        "department": "Department of Computer Science & Engineering",
        "due_date": "10-Oct-2026",
        "max_marks": 25,
        "accepted_formats": ".pdf, .doc, .docx",
        "instructions": "Detailed handwritten or typed solutions for balance factor derivations, Dijkstra shortest path algorithm, and graph search implementations."
    },
    {
        "id": "ASG-MA401",
        "course_code": "MA401",
        "subject": "Mathematics",
        "title": "Fourier Transform Analysis & Matrix Eigenvalues",
        "correspondent_faculty_id": "50103",
        "correspondent_faculty_name": "Prof. R. K. Varma",
        "department": "Department of Basic Sciences & Mathematics",
        "due_date": "18-Oct-2026",
        "max_marks": 20,
        "accepted_formats": ".pdf, .doc, .docx",
        "instructions": "Complete analytical solutions for partial differential boundary value problems and Fourier transform series."
    },
    {
        "id": "ASG-PH401",
        "course_code": "PH401",
        "subject": "Physics",
        "title": "Quantum Optics & Semiconductor Bandgap Experiment",
        "correspondent_faculty_id": "50104",
        "correspondent_faculty_name": "Prof. S. N. Roy",
        "department": "Department of Applied Physics",
        "due_date": "20-Oct-2026",
        "max_marks": 25,
        "accepted_formats": ".pdf, .doc, .docx",
        "instructions": "Virtual lab simulation observations, absorption spectra graphs, and semiconductor energy band calculations."
    },
    {
        "id": "ASG-EN401",
        "course_code": "EN401",
        "subject": "English",
        "title": "Technical Research Paper on AI Ethics in Higher Education",
        "correspondent_faculty_id": "50105",
        "correspondent_faculty_name": "Prof. Meera Nair",
        "department": "Department of Humanities & Communication",
        "due_date": "22-Oct-2026",
        "max_marks": 20,
        "accepted_formats": ".pdf, .doc, .docx",
        "instructions": "Adhere strictly to IEEE formatting guidelines. Minimum 4 pages with proper scholarly citations and references."
    }
]

default_submissions = [
    {
        "id": "SUB-101",
        "student_id": "25B11CS380",
        "student_name": "KALYANAM MUKUNDHA",
        "assignment_id": "ASG-CS402",
        "course_code": "CS402",
        "subject": "Data Structures",
        "title": "AVL Tree Rotations and Graph Search Implementations",
        "correspondent_faculty_id": "50101",
        "correspondent_faculty_name": "Dr. A. K. Sharma",
        "filename": "Kalyanam_Mukundha_CS402_AVL_Report.pdf",
        "file_format": "PDF",
        "file_size": "2.4 MB",
        "notes": "Attached complete proofs and Python/C++ implementations with unit tests.",
        "submitted_at": "24-Sep-2026 16:45",
        "status": "Graded",
        "marks": "24 / 25",
        "faculty_remarks": "High mathematical rigor in height balancing. Well documented test cases. Excellent work."
    },
    {
        "id": "SUB-102",
        "student_id": "25B11CS380",
        "student_name": "KALYANAM MUKUNDHA",
        "assignment_id": "ASG-CS401",
        "course_code": "CS401",
        "subject": "Python Programming",
        "title": "Deep Learning Pipeline Architecture Phase-1",
        "correspondent_faculty_id": "50102",
        "correspondent_faculty_name": "Prof. V. Priya",
        "filename": "Mukundha_Python_Capstone_Phase1.docx",
        "file_format": "DOCX",
        "file_size": "3.8 MB",
        "notes": "Model training scripts, schema diagrams, and preliminary accuracy benchmarks included.",
        "submitted_at": "26-Sep-2026 11:20",
        "status": "Submitted - Under Review",
        "marks": "Pending Evaluation",
        "faculty_remarks": "Submission received on time. Evaluation and plagiarism check underway."
    }
]

with open(ASSIGNMENTS_FILE, 'w', encoding='utf-8') as f:
    json.dump(default_assignments, f, indent=2)

with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
    json.dump(default_submissions, f, indent=2)

print("Initialized assignments and submissions JSON databases.")

# ==============================================================================
# 2. Update portal_manager.py with Assignment functions
# ==============================================================================

with open("portal_manager.py", "r", encoding="utf-8") as f:
    pm_code = f.read()

assignments_backend_code = """

# ==============================================================================
# ASSIGNMENT SUBMISSION & FACULTY ROUTING ENGINE
# ==============================================================================

ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.json')
SUBMISSIONS_FILE = os.path.join(DATA_DIR, 'assignment_submissions.json')


def get_student_assignments_portal(student_id):
    clean_sid = str(student_id).strip().upper()
    available = load_json_file(ASSIGNMENTS_FILE, [])
    all_subs = load_json_file(SUBMISSIONS_FILE, [])
    student_subs = [s for s in all_subs if str(s.get('student_id', '')).upper() == clean_sid]
    return {
        'available': available,
        'submissions': student_subs,
        'total_active': len(available),
        'total_submitted': len(student_subs)
    }


def submit_student_assignment_portal(student_id, assignment_id, title, notes, filename, file_data_base64=None, file_size="1.5 MB"):
    clean_sid = str(student_id).strip().upper()
    available = load_json_file(ASSIGNMENTS_FILE, [])
    asg = next((a for a in available if a['id'] == assignment_id), None)
    if not asg:
        # Fallback assignment
        asg = available[0] if available else {
            'id': 'ASG-GEN', 'course_code': 'GEN', 'subject': 'General Coursework',
            'correspondent_faculty_id': '50101', 'correspondent_faculty_name': 'Dr. A. K. Sharma'
        }

    now_str = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
    sub_id = f"SUB-{random.randint(1000, 9999)}"
    
    ext = os.path.splitext(filename)[1].upper().replace('.', '') or 'PDF'
    
    # Lookup student name
    s_name = 'Student'
    try:
        df = data_manager.load_data()
        match = df[df['Student_ID'].astype(str).str.upper() == clean_sid]
        if not match.empty:
            s_name = match.iloc[0]['Name']
    except Exception:
        pass

    new_sub = {
        'id': sub_id,
        'student_id': clean_sid,
        'student_name': s_name,
        'assignment_id': asg.get('id', assignment_id),
        'course_code': asg.get('course_code', ''),
        'subject': asg.get('subject', 'Coursework'),
        'title': title or asg.get('title', 'Assignment Submission'),
        'correspondent_faculty_id': asg.get('correspondent_faculty_id', '50101'),
        'correspondent_faculty_name': asg.get('correspondent_faculty_name', 'Dr. A. K. Sharma'),
        'filename': filename,
        'file_format': ext,
        'file_size': file_size,
        'notes': notes or '',
        'submitted_at': now_str,
        'status': 'Submitted - Under Review',
        'marks': 'Pending Evaluation',
        'faculty_remarks': 'Document routed to correspondent faculty. Pending verification.'
    }

    all_subs = load_json_file(SUBMISSIONS_FILE, [])
    all_subs.insert(0, new_sub)
    save_json_file(SUBMISSIONS_FILE, all_subs)

    # Post notification for the student
    create_student_notification(
        student_id=clean_sid,
        title=f"Assignment Submitted: {asg.get('subject')}",
        message=f"Your assignment '{new_sub['title']}' was successfully submitted to correspondent faculty {asg.get('correspondent_faculty_name')}.",
        category="Academic Submission",
        sender=asg.get('correspondent_faculty_name')
    )

    return True, "Assignment successfully submitted to correspondent faculty!", new_sub


def get_faculty_assignment_submissions(faculty_id):
    clean_fid = str(faculty_id).strip()
    all_subs = load_json_file(SUBMISSIONS_FILE, [])
    # Filter by correspondent faculty or show all if admin
    fac_subs = [s for s in all_subs if str(s.get('correspondent_faculty_id', '')) == clean_fid]
    if not fac_subs and all_subs:
        fac_subs = all_subs[:5] # show sample if newly loaded
    return fac_subs


def grade_student_assignment_portal(faculty_id, submission_id, marks, remarks):
    all_subs = load_json_file(SUBMISSIONS_FILE, [])
    for s in all_subs:
        if s.get('id') == submission_id:
            s['status'] = 'Graded'
            s['marks'] = str(marks)
            s['faculty_remarks'] = remarks
            s['graded_at'] = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
            save_json_file(SUBMISSIONS_FILE, all_subs)
            
            # Notify student of grading
            create_student_notification(
                student_id=s.get('student_id'),
                title=f"Assignment Graded: {s.get('subject')}",
                message=f"Prof. {s.get('correspondent_faculty_name')} graded your assignment '{s.get('title')}' - Marks: {marks}. Feedback: {remarks}",
                category="Grade Announcement",
                sender=s.get('correspondent_faculty_name')
            )
            return True, "Assignment successfully graded and student notified!", s
            
    return False, "Submission ID not found", None
"""

if "get_student_assignments_portal" not in pm_code:
    pm_code += assignments_backend_code
    with open("portal_manager.py", "w", encoding="utf-8") as f:
        f.write(pm_code)
    print("Added Assignment logic to portal_manager.py")

# ==============================================================================
# 3. Update app.py with REST API endpoints
# ==============================================================================

with open("app.py", "r", encoding="utf-8") as f:
    app_code = f.read()

api_routes = """

@app.route('/api/student/assignments/<student_id>', methods=['GET'])
def get_student_assignments_api(student_id):
    data = portal_manager.get_student_assignments_portal(student_id)
    return jsonify(data)


@app.route('/api/student/submit-assignment', methods=['POST'])
def submit_student_assignment_api():
    data = request.get_json() or {}
    student_id = data.get('student_id', '25B11CS380')
    assignment_id = data.get('assignment_id')
    title = data.get('title', '')
    notes = data.get('notes', '')
    filename = data.get('filename', 'Assignment_Document.pdf')
    file_size = data.get('file_size', '2.1 MB')
    file_base64 = data.get('file_base64', '')
    
    success, msg, item = portal_manager.submit_student_assignment_portal(
        student_id=student_id,
        assignment_id=assignment_id,
        title=title,
        notes=notes,
        filename=filename,
        file_data_base64=file_base64,
        file_size=file_size
    )
    return jsonify({'success': success, 'message': msg, 'submission': item})


@app.route('/api/faculty/assignments/<faculty_id>', methods=['GET'])
def get_faculty_assignments_api(faculty_id):
    subs = portal_manager.get_faculty_assignment_submissions(faculty_id)
    return jsonify({'submissions': subs})


@app.route('/api/faculty/grade-assignment', methods=['POST'])
def grade_assignment_api():
    data = request.get_json() or {}
    faculty_id = data.get('faculty_id', '50101')
    submission_id = data.get('submission_id')
    marks = data.get('marks', '25/25')
    remarks = data.get('remarks', 'Good work')
    success, msg, item = portal_manager.grade_student_assignment_portal(faculty_id, submission_id, marks, remarks)
    return jsonify({'success': success, 'message': msg, 'item': item})
"""

if "get_student_assignments_api" not in app_code:
    # Insert before if __name__ == '__main__':
    app_code = app_code.replace("if __name__ == '__main__':", api_routes + "\n\nif __name__ == '__main__':")
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(app_code)
    print("Added Assignment REST endpoints to app.py")

print("Backend preparation completed successfully!")

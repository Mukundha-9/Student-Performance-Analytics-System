with open("portal_manager.py", "r", encoding="utf-8") as f:
    code = f.read()

old_block_start = "# ASSIGNMENT SUBMISSION & FACULTY ROUTING ENGINE"

new_block = '''# ==============================================================================
# ASSIGNMENT SUBMISSION & FACULTY ROUTING ENGINE
# ==============================================================================

ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.json')
SUBMISSIONS_FILE = os.path.join(DATA_DIR, 'assignment_submissions.json')


def create_student_notification(student_id, title, message, category="General", sender="Aditya University"):
    announcements = load_json_file(ANNOUNCEMENTS_FILE, [])
    now_str = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
    new_notif = {
        'id': f"NOTIF-{random.randint(1000, 9999)}",
        'student_id': str(student_id).strip().upper(),
        'title': title,
        'message': message,
        'category': category,
        'sender': sender,
        'date': now_str,
        'read': False
    }
    announcements.insert(0, new_notif)
    save_json_file(ANNOUNCEMENTS_FILE, announcements)
    return new_notif


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
        asg = available[0] if available else {
            'id': 'ASG-GEN', 'course_code': 'GEN', 'subject': 'General Coursework',
            'correspondent_faculty_id': '50101', 'correspondent_faculty_name': 'Dr. A. K. Sharma'
        }

    now_str = datetime.datetime.now().strftime('%d-%b-%Y %H:%M')
    sub_id = f"SUB-{random.randint(1000, 9999)}"
    
    ext = os.path.splitext(filename)[1].upper().replace('.', '') or 'PDF'
    
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
    fac_subs = [s for s in all_subs if str(s.get('correspondent_faculty_id', '')) == clean_fid]
    if not fac_subs and all_subs:
        fac_subs = all_subs[:5]
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
'''

pos = code.find(old_block_start)
if pos != -1:
    code = code[:pos] + new_block
    with open("portal_manager.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Fixed portal_manager.py with create_student_notification")

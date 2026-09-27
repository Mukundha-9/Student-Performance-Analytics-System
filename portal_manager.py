# ==============================================================================
# Portal Manager Module - Aditya University Multi-Portal System
# Manages Data, Authentication & Logic for Student, Faculty & Admin Portals
# ==============================================================================
import os
import json
import random
import datetime
import pandas as pd
from config import DATA_DIR, SUBJECTS, BRANCHES, SEMESTERS, DEFAULT_CSV_PATH, INSTITUTION, DEPARTMENT
import data_manager
import analytics

FACULTIES_FILE = os.path.join(DATA_DIR, 'faculties.json')
TIMETABLE_FILE = os.path.join(DATA_DIR, 'timetable.json')
FEES_FILE = os.path.join(DATA_DIR, 'fees.json')
ANNOUNCEMENTS_FILE = os.path.join(DATA_DIR, 'announcements.json')
PROCTORING_FILE = os.path.join(DATA_DIR, 'proctoring_logs.json')

DEFAULT_PASSWORD = 'aditya@123'


def load_json_file(filepath, default=None):
    if default is None:
        default = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json_file(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return True


# ==============================================================================
# 1. INITIALIZE DATA STORES
# ==============================================================================

def init_portal_data():
    df = data_manager.load_data()
    all_student_ids = df['Student_ID'].tolist() if not df.empty else []

    # 1. Initialize Faculties (with 5-digit Faculty Numbers)
    faculty_list = [
        {
            'faculty_id': '50101',
            'code': 'FAC-CSE-101',
            'name': 'Dr. A. K. Sharma',
            'designation': 'Professor & Head of Academic Council',
            'department': 'Computer Science & Engineering',
            'email': 'aksharma@aditya.ac.in',
            'phone': '+91 98765 43210',
            'office': 'Ramanujan Block - Room 402',
            'office_hours': 'Mon, Wed, Fri (03:00 PM - 05:00 PM)',
            'subjects_taught': ['Python_Programming', 'Data_Structures'],
            'proctee_ids': all_student_ids[0:25] if len(all_student_ids) >= 25 else all_student_ids
        },
        {
            'faculty_id': '50102',
            'code': 'FAC-CSE-102',
            'name': 'Prof. V. Priya',
            'designation': 'Associate Professor & AI Lab Incharge',
            'department': 'Computer Science & Engineering',
            'email': 'vpriya@aditya.ac.in',
            'phone': '+91 98765 43211',
            'office': 'Turing Block - Room 204',
            'office_hours': 'Tue, Thu (02:00 PM - 04:00 PM)',
            'subjects_taught': ['Python_Programming', 'Mathematics'],
            'proctee_ids': all_student_ids[25:50] if len(all_student_ids) >= 50 else []
        },
        {
            'faculty_id': '50103',
            'code': 'FAC-CSE-103',
            'name': 'Dr. K. Venkatesh Rao',
            'designation': 'Professor & Algorithms Specialist',
            'department': 'Computer Science & Engineering',
            'email': 'kvenkatesh@aditya.ac.in',
            'phone': '+91 98765 43212',
            'office': 'Aryabhata Block - Room 305',
            'office_hours': 'Mon, Thu (10:00 AM - 12:00 PM)',
            'subjects_taught': ['Data_Structures', 'Mathematics'],
            'proctee_ids': all_student_ids[50:75] if len(all_student_ids) >= 75 else []
        },
        {
            'faculty_id': '50201',
            'code': 'FAC-ECE-201',
            'name': 'Dr. S. R. Murthy',
            'designation': 'Professor & Dean of Research',
            'department': 'Electronics & Communication',
            'email': 'srmurthy@aditya.ac.in',
            'phone': '+91 98765 43213',
            'office': 'J.C. Bose Block - Room 101',
            'office_hours': 'Daily (04:00 PM - 05:00 PM)',
            'subjects_taught': ['Physics', 'Mathematics'],
            'proctee_ids': all_student_ids[75:100] if len(all_student_ids) >= 100 else []
        },
        {
            'faculty_id': '50301',
            'code': 'FAC-HUM-301',
            'name': 'Dr. Meenakshi Sundaram',
            'designation': 'Associate Professor of English',
            'department': 'Humanities & Sciences',
            'email': 'meenakshi@aditya.ac.in',
            'phone': '+91 98765 43214',
            'office': 'Tagore Block - Room 108',
            'office_hours': 'Wed, Fri (11:00 AM - 01:00 PM)',
            'subjects_taught': ['English'],
            'proctee_ids': all_student_ids[100:125] if len(all_student_ids) >= 125 else []
        }
    ]
    save_json_file(FACULTIES_FILE, faculty_list)

    # 2. Initialize Timetable
    if not os.path.exists(TIMETABLE_FILE):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        periods = [
            {'period': 1, 'time': '09:00 AM - 09:50 AM'},
            {'period': 2, 'time': '09:50 AM - 10:40 AM'},
            {'period': 3, 'time': '10:50 AM - 11:40 AM'},
            {'period': 4, 'time': '11:40 AM - 12:30 PM'},
            {'period': 5, 'time': '01:30 PM - 02:20 PM'},
            {'period': 6, 'time': '02:20 PM - 03:10 PM'},
            {'period': 7, 'time': '03:10 PM - 04:00 PM'}
        ]

        sub_pool = [
            {'sub': 'Python_Programming', 'faculty': 'Dr. A. K. Sharma', 'room': 'Lab 3 (Turing Block)'},
            {'sub': 'Data_Structures', 'faculty': 'Dr. K. Venkatesh Rao', 'room': 'Room 302 (Ramanujan Block)'},
            {'sub': 'Mathematics', 'faculty': 'Prof. V. Priya', 'room': 'Room 302 (Ramanujan Block)'},
            {'sub': 'Physics', 'faculty': 'Dr. S. R. Murthy', 'room': 'Physics Lab 1'},
            {'sub': 'English', 'faculty': 'Dr. Meenakshi Sundaram', 'room': 'Language Lab 2'},
            {'sub': 'Technical Seminar & Mentoring', 'faculty': 'Dr. A. K. Sharma', 'room': 'Seminar Hall 1'},
            {'sub': 'Project Lab Session', 'faculty': 'Prof. V. Priya', 'room': 'Innovation Hub'}
        ]

        schedule = {}
        for d in days:
            schedule[d] = []
            shuffled = sub_pool.copy()
            random.seed(len(d) * 7)
            random.shuffle(shuffled)
            for idx, p in enumerate(periods):
                assigned = shuffled[idx % len(shuffled)]
                schedule[d].append({
                    'period': p['period'],
                    'time': p['time'],
                    'subject': assigned['sub'],
                    'subject_name': assigned['sub'].replace('_', ' '),
                    'faculty': assigned['faculty'],
                    'room': assigned['room']
                })

        save_json_file(TIMETABLE_FILE, schedule)

    # 3. Initialize Announcements
    if not os.path.exists(ANNOUNCEMENTS_FILE):
        announcements = [
            {
                'id': 1,
                'title': 'End-Semester Theory & Practical Examination Schedule (AY 2025-26)',
                'category': 'Exam',
                'badge_class': 'badge-danger',
                'author': 'Office of Controller of Examinations',
                'date': '2026-08-25',
                'target': 'All',
                'content': 'The End-Semester regular examinations for all B.Tech branches will commence from 15th September 2026. Hall Tickets are available for download in the Student Portal.'
            },
            {
                'id': 2,
                'title': 'Campus Placement Drive: Google, Microsoft & TCS Digital Registration',
                'category': 'Placement',
                'badge_class': 'badge-success',
                'author': 'Department Training & Placement Cell',
                'date': '2026-08-22',
                'target': 'Student',
                'content': 'Eligible students with CGPA >= 7.5 and no active backlogs are advised to register on the placement portal before 5th September. Mock aptitude tests will be hosted this weekend.'
            },
            {
                'id': 3,
                'title': 'Continuous Internal Assessment (CIA-2) Marks Upload Deadline for Faculty',
                'category': 'Academic',
                'badge_class': 'badge-warning',
                'author': 'Dean of Academic Affairs',
                'date': '2026-08-20',
                'target': 'Faculty',
                'content': 'All department faculty members are requested to enter and finalize CIA-2 internal marks in the Faculty Grading Desk by 31st August 05:00 PM.'
            },
            {
                'id': 4,
                'title': 'Mandatory Attendance Warning: 75% Biometric/Digital Roster Compliance',
                'category': 'Urgent',
                'badge_class': 'badge-danger',
                'author': 'Office of Principal & Dean Student Affairs',
                'date': '2026-08-18',
                'target': 'All',
                'content': 'Students with overall attendance below 75% have been flagged for mandatory proctoring counselling. Non-compliance will result in detention from appearing in Semester Exams.'
            }
        ]
        save_json_file(ANNOUNCEMENTS_FILE, announcements)

    # 4. Initialize Fees
    if not os.path.exists(FEES_FILE):
        fee_records = {}
        for s_id in all_student_ids:
            fee_records[s_id] = {
                'student_id': s_id,
                'academic_year': '2025-2026',
                'semester': 'Semester 4',
                'tuition_fee': 75000.0,
                'exam_fee': 3500.0,
                'lab_library_fee': 6500.0,
                'special_training_fee': 5000.0,
                'total_amount': 90000.0,
                'amount_paid': 90000.0 if random.random() > 0.3 else 50000.0,
                'due_amount': 0.0,
                'status': 'Paid',
                'payment_history': [
                    {
                        'receipt_no': f"REC-ADITYA-{random.randint(10000, 99999)}",
                        'date': '2026-06-15',
                        'amount': 50000.0,
                        'mode': 'UPI / NetBanking',
                        'status': 'Success',
                        'remarks': 'Term-1 Tuition & Special Fee'
                    }
                ]
            }
            fee_records[s_id]['due_amount'] = max(0.0, fee_records[s_id]['total_amount'] - fee_records[s_id]['amount_paid'])
            if fee_records[s_id]['due_amount'] > 0:
                fee_records[s_id]['status'] = 'Pending'
            else:
                fee_records[s_id]['status'] = 'Paid'
                fee_records[s_id]['payment_history'].append({
                    'receipt_no': f"REC-ADITYA-{random.randint(10000, 99999)}",
                    'date': '2026-08-05',
                    'amount': 40000.0,
                    'mode': 'Debit Card / Razorpay',
                    'status': 'Success',
                    'remarks': 'Term-2 Clearance & Exam Fee'
                })

        save_json_file(FEES_FILE, fee_records)


# ==============================================================================
# 2. AUTHENTICATION & DEMO PROFILES
# ==============================================================================

def authenticate_user(role, username, password):
    clean_u = str(username).strip().upper()
    role = str(role).strip().lower()
    pw = str(password).strip()

    # Allow master password 'aditya@123' or empty for fast testing
    is_valid_pw = (pw == DEFAULT_PASSWORD or pw == '' or pw == 'aditya123' or pw == 'admin123' or pw == 'student123' or pw == 'faculty123')

    if role == 'admin':
        if clean_u in ['ADMIN', 'REGISTRAR', 'DEAN', '90001', 'AD-9001']:
            if not is_valid_pw and pw != DEFAULT_PASSWORD:
                return None
            return {
                'role': 'admin',
                'user_id': '90001',
                'name': 'Dr. K. Srinivas (University Registrar)',
                'title': 'Office of Controller of Examinations & Academic Affairs',
                'department': 'University Administration',
                'email': 'registrar@aditya.ac.in',
                'avatar': 'fa-solid fa-building-columns'
            }

    elif role == 'faculty':
        faculties = load_json_file(FACULTIES_FILE, [])
        for f in faculties:
            # Check 5-digit number, code, name or FACULTY
            if f['faculty_id'] == clean_u or f.get('code', '').upper() == clean_u or clean_u in f['name'].upper() or clean_u == 'FACULTY':
                if not is_valid_pw and pw != DEFAULT_PASSWORD:
                    return None
                return {
                    'role': 'faculty',
                    'user_id': f['faculty_id'],
                    'code': f.get('code', 'FAC-CSE-101'),
                    'name': f['name'],
                    'title': f['designation'],
                    'department': f['department'],
                    'email': f['email'],
                    'phone': f['phone'],
                    'office': f['office'],
                    'subjects': f['subjects_taught'],
                    'proctee_count': len(f['proctee_ids']),
                    'avatar': 'fa-solid fa-chalkboard-user'
                }
        if faculties and (clean_u == '' or clean_u == 'FACULTY' or clean_u == '50101'):
            f = faculties[0]
            return {
                'role': 'faculty',
                'user_id': f['faculty_id'],
                'code': f.get('code', 'FAC-CSE-101'),
                'name': f['name'],
                'title': f['designation'],
                'department': f['department'],
                'email': f['email'],
                'phone': f['phone'],
                'office': f['office'],
                'subjects': f['subjects_taught'],
                'proctee_count': len(f['proctee_ids']),
                'avatar': 'fa-solid fa-chalkboard-user'
            }

    elif role == 'student':
        df = data_manager.load_data()
        mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_u
        if mask.any():
            if not is_valid_pw and pw != DEFAULT_PASSWORD:
                return None
            s = df[mask].iloc[0]
            return {
                'role': 'student',
                'user_id': str(s['Student_ID']),
                'name': str(s['Name']),
                'branch': str(s['Branch']),
                'semester': str(s.get('Semester', 'Semester 4')),
                'attendance': float(s['Attendance']),
                'percentage': float(s['Percentage']),
                'grade': str(s['Grade']),
                'status': str(s['Status']),
                'email': f"{str(s['Student_ID']).lower()}@aditya.ac.in",
                'avatar': 'fa-solid fa-user-graduate'
            }
        elif not df.empty:
            s = df.iloc[0]
            return {
                'role': 'student',
                'user_id': str(s['Student_ID']),
                'name': str(s['Name']),
                'branch': str(s['Branch']),
                'semester': str(s.get('Semester', 'Semester 4')),
                'attendance': float(s['Attendance']),
                'percentage': float(s['Percentage']),
                'grade': str(s['Grade']),
                'status': str(s['Status']),
                'email': f"{str(s['Student_ID']).lower()}@aditya.ac.in",
                'avatar': 'fa-solid fa-user-graduate'
            }

    return None


def get_demo_user_list():
    df = data_manager.load_data()
    faculties = load_json_file(FACULTIES_FILE, [])

    students = []
    if not df.empty:
        for _, s in df.head(4).iterrows():
            students.append({
                'id': str(s['Student_ID']),
                'name': str(s['Name']),
                'branch': str(s['Branch']),
                'score': f"{s['Percentage']}% ({s['Grade']})"
            })

    fac_list = []
    for f in faculties[:3]:
        fac_list.append({
            'id': f['faculty_id'],
            'code': f.get('code', ''),
            'name': f['name'],
            'dept': f['department'],
            'designation': f['designation']
        })

    return {
        'default_password': DEFAULT_PASSWORD,
        'students': students,
        'faculties': fac_list,
        'admin': {
            'id': '90001',
            'name': 'Dr. K. Srinivas',
            'role': 'University Registrar & Academic Controller'
        }
    }


# ==============================================================================
# 3. STUDENT PORTAL DATA PROVIDERS
# ==============================================================================

def get_student_timetable(student_id):
    schedule = load_json_file(TIMETABLE_FILE, {})
    now = datetime.datetime.now()
    current_day = now.strftime('%A')
    if current_day not in schedule:
        current_day = 'Monday'

    current_hour = now.hour
    active_period = 1
    if 9 <= current_hour < 10: active_period = 1
    elif 10 <= current_hour < 11: active_period = 2
    elif 11 <= current_hour < 12: active_period = 3
    elif 12 <= current_hour < 13: active_period = 4
    elif 13 <= current_hour < 14: active_period = 5
    elif 14 <= current_hour < 15: active_period = 6
    else: active_period = 7

    return {
        'today': current_day,
        'active_period': active_period,
        'full_schedule': schedule,
        'today_classes': schedule.get(current_day, [])
    }


def get_student_faculties(student_id):
    clean_id = str(student_id).strip().upper()
    faculties = load_json_file(FACULTIES_FILE, [])

    assigned_proctor = None
    enrolled_faculty = []

    for f in faculties:
        if clean_id in [str(p).strip().upper() for p in f.get('proctee_ids', [])]:
            assigned_proctor = {
                'faculty_id': f['faculty_id'],
                'code': f.get('code', ''),
                'name': f['name'],
                'designation': f['designation'],
                'department': f['department'],
                'email': f['email'],
                'phone': f['phone'],
                'office': f['office'],
                'office_hours': f['office_hours']
            }

        enrolled_faculty.append({
            'faculty_id': f['faculty_id'],
            'code': f.get('code', ''),
            'name': f['name'],
            'designation': f['designation'],
            'department': f['department'],
            'subjects': [s.replace('_', ' ') for s in f['subjects_taught']],
            'email': f['email'],
            'office': f['office']
        })

    if not assigned_proctor and faculties:
        f = faculties[0]
        assigned_proctor = {
            'faculty_id': f['faculty_id'],
            'code': f.get('code', ''),
            'name': f['name'],
            'designation': f['designation'],
            'department': f['department'],
            'email': f['email'],
            'phone': f['phone'],
            'office': f['office'],
            'office_hours': f['office_hours']
        }

    return {
        'proctor': assigned_proctor,
        'enrolled_faculty': enrolled_faculty
    }


def get_student_fees(student_id):
    clean_id = str(student_id).strip().upper()
    fees_db = load_json_file(FEES_FILE, {})

    if clean_id in fees_db:
        return fees_db[clean_id]

    fee_rec = {
        'student_id': clean_id,
        'academic_year': '2025-2026',
        'semester': 'Semester 4',
        'tuition_fee': 75000.0,
        'exam_fee': 3500.0,
        'lab_library_fee': 6500.0,
        'special_training_fee': 5000.0,
        'total_amount': 90000.0,
        'amount_paid': 90000.0,
        'due_amount': 0.0,
        'status': 'Paid',
        'payment_history': [
            {
                'receipt_no': f"REC-ADITYA-{random.randint(10000, 99999)}",
                'date': '2026-06-15',
                'amount': 90000.0,
                'mode': 'UPI / NetBanking',
                'status': 'Success',
                'remarks': 'Annual Complete Clearance'
            }
        ]
    }
    fees_db[clean_id] = fee_rec
    save_json_file(FEES_FILE, fees_db)
    return fee_rec


def pay_student_fee(student_id, pay_amount, payment_mode='UPI'):
    clean_id = str(student_id).strip().upper()
    fees_db = load_json_file(FEES_FILE, {})
    fee_rec = get_student_fees(clean_id)

    amount = float(pay_amount)
    if amount <= 0:
        return False, 'Payment amount must be greater than zero.', None

    receipt_no = f"REC-ADITYA-{random.randint(10000, 99999)}"
    now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tx = {
        'receipt_no': receipt_no,
        'date': now_date,
        'amount': amount,
        'mode': payment_mode,
        'status': 'Success',
        'remarks': f"Online Fee Settlement ({payment_mode})"
    }

    fee_rec['amount_paid'] += amount
    fee_rec['due_amount'] = max(0.0, fee_rec['total_amount'] - fee_rec['amount_paid'])
    if fee_rec['due_amount'] == 0:
        fee_rec['status'] = 'Paid'
    else:
        fee_rec['status'] = 'Partial'

    fee_rec['payment_history'].insert(0, tx)
    fees_db[clean_id] = fee_rec
    save_json_file(FEES_FILE, fees_db)

    return True, 'Fee Payment Processed Successfully!', tx


def get_student_hall_ticket(student_id):
    df = data_manager.load_data()
    clean_id = str(student_id).strip().upper()
    mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_id
    if not mask.any():
        s = df.iloc[0]
    else:
        s = df[mask].iloc[0]

    exam_schedule = [
        {'date': '15-Sep-2026 (10:00 AM - 01:00 PM)', 'code': 'CS401', 'subject': 'Mathematics - IV', 'room': 'Block-A / Room 302'},
        {'date': '17-Sep-2026 (10:00 AM - 01:00 PM)', 'code': 'CS402', 'subject': 'Applied Physics', 'room': 'Block-A / Room 302'},
        {'date': '20-Sep-2026 (10:00 AM - 01:00 PM)', 'code': 'CS403', 'subject': 'Python Programming', 'room': 'Block-A / Room 302'},
        {'date': '22-Sep-2026 (10:00 AM - 01:00 PM)', 'code': 'CS404', 'subject': 'Data Structures & Algorithms', 'room': 'Block-A / Room 302'},
        {'date': '25-Sep-2026 (10:00 AM - 01:00 PM)', 'code': 'CS405', 'subject': 'Professional English', 'room': 'Block-A / Room 302'}
    ]

    fees = get_student_fees(clean_id)
    financial_clearance = 'CLEARED (No Dues)' if fees['due_amount'] == 0 else f"PENDING DUES (Rs. {fees['due_amount']})"

    return {
        'student_id': str(s['Student_ID']),
        'name': str(s['Name']),
        'gender': str(s.get('Gender', 'Male')),
        'branch': str(s['Branch']),
        'semester': str(s.get('Semester', 'Semester 4')),
        'attendance': float(s['Attendance']),
        'exam_center': 'Aditya University Campus Examination Hall, Surampalem',
        'financial_clearance': financial_clearance,
        'attendance_clearance': 'APPROVED' if float(s['Attendance']) >= 75.0 else 'CONDITIONAL (Warning)',
        'exams': exam_schedule
    }


# ==============================================================================
# 4. FACULTY PORTAL DATA PROVIDERS
# ==============================================================================

def get_faculty_dashboard(faculty_id):
    faculties = load_json_file(FACULTIES_FILE, [])
    clean_id = str(faculty_id).strip().upper()

    fac = None
    for f in faculties:
        if f['faculty_id'] == clean_id or f.get('code', '').upper() == clean_id:
            fac = f
            break
    if not fac and faculties:
        fac = faculties[0]

    df = data_manager.load_data()

    # Get Assigned Proctee Students
    proctee_ids = [str(pid).strip().upper() for pid in fac.get('proctee_ids', [])]
    proctee_df = df[df['Student_ID'].astype(str).str.strip().str.upper().isin(proctee_ids)] if not df.empty else pd.DataFrame()

    proctee_list = []
    if not proctee_df.empty:
        for _, row in proctee_df.iterrows():
            att = float(row['Attendance'])
            pct = float(row['Percentage'])
            risk_flags = []
            if att < 75.0: risk_flags.append('Low Attendance (<75%)')
            if pct < 50.0: risk_flags.append('Critical Score (<50%)')

            proctee_list.append({
                'student_id': str(row['Student_ID']),
                'name': str(row['Name']),
                'branch': str(row['Branch']),
                'semester': str(row.get('Semester', 'Sem 4')),
                'attendance': att,
                'percentage': pct,
                'grade': str(row['Grade']),
                'status': str(row['Status']),
                'is_at_risk': len(risk_flags) > 0,
                'risk_reasons': ' & '.join(risk_flags) if risk_flags else 'Good Academic Standing'
            })

    # Subject performance statistics
    subject_stats = {}
    for sub in fac.get('subjects_taught', []):
        if sub in df.columns:
            marks = df[sub].to_numpy(dtype=float)
            pass_mask = marks >= 40.0
            subject_stats[sub.replace('_', ' ')] = {
                'raw_subject': sub,
                'mean': round(float(marks.mean()), 1),
                'highest': round(float(marks.max()), 1),
                'lowest': round(float(marks.min()), 1),
                'pass_percentage': round(float(pass_mask.mean() * 100.0), 1),
                'failed_count': int((~pass_mask).sum())
            }

    return {
        'faculty': fac,
        'proctees_count': len(proctee_list),
        'at_risk_proctees_count': sum(1 for p in proctee_list if p['is_at_risk']),
        'proctees': proctee_list,
        'subject_analytics': subject_stats
    }


def post_daily_attendance(subject, date, attendance_dict):
    df = data_manager.load_data()
    updated_count = 0

    for s_id, status in attendance_dict.items():
        clean_id = str(s_id).strip().upper()
        mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_id
        if mask.any():
            idx = df[mask].index[0]
            current_att = float(df.at[idx, 'Attendance'])
            if status == 'Present':
                new_att = min(100.0, current_att + 0.2)
            else:
                new_att = max(0.0, current_att - 0.4)
            df.at[idx, 'Attendance'] = round(new_att, 1)
            updated_count += 1

    data_manager.save_data(df)
    return True, f"Attendance registered for {updated_count} students in {subject.replace('_', ' ')}."


def post_subject_marks(subject, marks_dict):
    df = data_manager.load_data()
    updated_count = 0

    if subject not in df.columns:
        return False, f"Invalid subject: {subject}"

    for s_id, mark_val in marks_dict.items():
        clean_id = str(s_id).strip().upper()
        mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_id
        if mask.any():
            idx = df[mask].index[0]
            val = max(0.0, min(100.0, float(mark_val)))
            df.at[idx, subject] = round(val, 1)

            sub_marks = {s: float(df.at[idx, s]) for s in SUBJECTS if s in df.columns}
            metrics = data_manager.calculate_metrics_for_marks(sub_marks)
            for k, v in metrics.items():
                df.at[idx, k] = v
            updated_count += 1

    data_manager.save_data(df)
    return True, f"Updated marks for {updated_count} students in {subject.replace('_', ' ')}."


init_portal_data()


# ==============================================================================
# 5. UNIQUE FACULTY FEATURES (Remedial Action Planner & Leave Desk)
# ==============================================================================

LEAVES_FILE = os.path.join(DATA_DIR, 'faculty_leaves.json')

def get_faculty_remedial_plan(faculty_id):
    fac_info = get_faculty_dashboard(faculty_id)
    fac = fac_info.get('faculty', {})
    subjects = fac.get('subjects_taught', ['Python_Programming'])
    
    df = data_manager.load_data()
    struggling_students = []
    
    for sub in subjects:
        if sub in df.columns:
            weak_mask = df[sub] < 50.0
            weak_df = df[weak_mask]
            for _, r in weak_df.head(10).iterrows():
                struggling_students.append({
                    'student_id': str(r['Student_ID']),
                    'name': str(r['Name']),
                    'branch': str(r['Branch']),
                    'subject': sub.replace('_', ' '),
                    'current_score': float(r[sub]),
                    'attendance': float(r['Attendance']),
                    'gap_analysis': f"Requires reinforcement in core problem solving and practical lab drills.",
                    'target_score': 65.0
                })
                
    remedial_schedule = [
        {'week': 'Week 1', 'topic': 'Foundational Concepts, Control Flow & Debugging Techniques', 'day_time': 'Every Tuesday (04:00 PM - 05:30 PM)', 'venue': 'Lab-3 (Turing Block)'},
        {'week': 'Week 2', 'topic': 'Data Structures Implementation & Memory Optimization Drills', 'day_time': 'Every Thursday (04:00 PM - 05:30 PM)', 'venue': 'Seminar Hall 2'},
        {'week': 'Week 3', 'topic': 'Previous Year Question Analysis & Mock Speed Tests', 'day_time': 'Every Saturday (02:00 PM - 04:00 PM)', 'venue': 'Room 402 (Ramanujan Block)'},
        {'week': 'Week 4', 'topic': '1-on-1 Code Review & Final Remedial Assessment Test', 'day_time': 'Next Monday (03:30 PM - 05:00 PM)', 'venue': 'Innovation Lab'}
    ]
    
    return {
        'faculty_name': fac.get('name', 'Faculty Member'),
        'subjects': [s.replace('_', ' ') for s in subjects],
        'total_struggling_students': len(struggling_students),
        'students_list': struggling_students,
        'schedule': remedial_schedule
    }


def get_faculty_leaves(faculty_id):
    leaves = load_json_file(LEAVES_FILE, [
        {
            'leave_id': 'LV-2026-101',
            'faculty_id': '50101',
            'faculty_name': 'Dr. A. K. Sharma',
            'date': '2026-09-02',
            'type': 'On Duty (National Conference)',
            'substitute_faculty': 'Prof. V. Priya (50102)',
            'slot_details': 'Period 1 & 2: Python Programming in Lab-3',
            'status': 'Approved'
        }
    ])
    return [l for l in leaves if l.get('faculty_id') == str(faculty_id)] or leaves


def apply_faculty_leave(faculty_id, date, leave_type, substitute_faculty, slot_details):
    leaves = load_json_file(LEAVES_FILE, [])
    faculties = load_json_file(FACULTIES_FILE, [])
    fac_name = next((f['name'] for f in faculties if f['faculty_id'] == str(faculty_id)), 'Faculty Member')
    
    new_leave = {
        'leave_id': f"LV-2026-{random.randint(100, 999)}",
        'faculty_id': str(faculty_id),
        'faculty_name': fac_name,
        'date': date,
        'type': leave_type,
        'substitute_faculty': substitute_faculty,
        'slot_details': slot_details,
        'status': 'Approved (Auto-Synced)'
    }
    leaves.insert(0, new_leave)
    save_json_file(LEAVES_FILE, leaves)
    return True, f"Leave recorded and substitute lecture assigned to {substitute_faculty}."


# ==============================================================================
# 6. UNIQUE ADMIN FEATURES (Result Moderation, NAAC Audit & Detention Desk)
# ==============================================================================

MODERATION_FILE = os.path.join(DATA_DIR, 'moderation_status.json')

def get_admin_moderation_status():
    status = load_json_file(MODERATION_FILE, {
        'results_published': True,
        'published_date': '2026-08-25',
        'semester': 'Semester 4 Regular Examinations (AY 2025-26)',
        'moderation_applied': False,
        'grace_marks_applied': 0,
        'borderline_beneficiaries': 0
    })
    return status


def apply_admin_moderation(grace_marks=3):
    df = data_manager.load_data()
    status = get_admin_moderation_status()
    
    initial_fail_count = int((df['Status'] == 'Fail').sum())
    beneficiaries = 0
    
    for sub in SUBJECTS:
        if sub in df.columns:
            # Check borderline failing students between (40 - grace_marks) and 39
            borderline_mask = (df[sub] >= (40.0 - grace_marks)) & (df[sub] < 40.0)
            count = int(borderline_mask.sum())
            if count > 0:
                df.loc[borderline_mask, sub] = 40.0
                beneficiaries += count
                
    # Recalculate all student metrics
    for idx, row in df.iterrows():
        sub_marks = {s: float(row[s]) for s in SUBJECTS if s in df.columns}
        metrics = data_manager.calculate_metrics_for_marks(sub_marks)
        for k, v in metrics.items():
            df.at[idx, k] = v
            
    data_manager.save_data(df)
    
    new_fail_count = int((df['Status'] == 'Fail').sum())
    passed_count = int((df['Status'] == 'Pass').sum())
    pass_pct = round(float((passed_count / len(df)) * 100.0), 2)
    
    status['moderation_applied'] = True
    status['grace_marks_applied'] = grace_marks
    status['borderline_beneficiaries'] = beneficiaries
    status['new_pass_percentage'] = pass_pct
    save_json_file(MODERATION_FILE, status)
    
    return True, f"Moderation of +{grace_marks} grace marks applied. {beneficiaries} subject-level borderline grades upgraded! New Pass Rate: {pass_pct}%."


def toggle_result_publishing():
    status = get_admin_moderation_status()
    status['results_published'] = not status.get('results_published', True)
    save_json_file(MODERATION_FILE, status)
    state_str = "Published Online" if status['results_published'] else "Withheld / Draft Mode"
    return True, f"Semester Results status changed to: {state_str}."


def get_admin_accreditation_audit():
    df = data_manager.load_data()
    total = len(df) if not df.empty else 500
    pass_count = int((df['Status'] == 'Pass').sum()) if not df.empty else 448
    pass_pct = round(float((pass_count / total) * 100.0), 1)
    
    branch_stats = []
    for b in BRANCHES:
        b_df = df[df['Branch'] == b] if not df.empty else pd.DataFrame()
        if not b_df.empty:
            b_pass = (b_df['Status'] == 'Pass').mean() * 100.0
            b_avg = b_df['Percentage'].mean()
            branch_stats.append({
                'branch': b,
                'enrolled': len(b_df),
                'pass_rate': round(float(b_pass), 1),
                'mean_score': round(float(b_avg), 1),
                'obe_attainment': round(float(b_pass * 0.95), 1),
                'status': 'Accredited' if b_pass >= 75.0 else 'Under Review'
            })
            
    return {
        'institution': INSTITUTION,
        'department': DEPARTMENT,
        'audit_cycle': 'NAAC Cycle-3 & NBA Tier-1 Compliance (2025-2026)',
        'overall_institutional_score': '3.78 / 4.00 (Grade A++)',
        'faculty_student_ratio': '1 : 15 (Approved Standard)',
        'obe_outcome_attainment': '88.4%',
        'campus_pass_rate': f"{pass_pct}%",
        'placement_index': '91.2%',
        'criteria': [
            {'criterion': 'Criterion 1: Curricular Aspects & OBE Mapping', 'score': '3.85 / 4.0', 'status': 'Excellent'},
            {'criterion': 'Criterion 2: Teaching-Learning & Continuous Evaluation', 'score': '3.80 / 4.0', 'status': 'Excellent'},
            {'criterion': 'Criterion 3: Research, Innovations & Faculty Publications', 'score': '3.65 / 4.0', 'status': 'Very Good'},
            {'criterion': 'Criterion 4: Infrastructure, Computing & AI Labs', 'score': '3.90 / 4.0', 'status': 'Outstanding'},
            {'criterion': 'Criterion 5: Student Progression & Placement Track', 'score': '3.75 / 4.0', 'status': 'Excellent'}
        ],
        'branch_audit': branch_stats
    }


def get_admin_detention_list():
    df = data_manager.load_data()
    detained_students = []
    
    if not df.empty:
        low_att_df = df[df['Attendance'] < 75.0].sort_values(by='Attendance', ascending=True)
        for _, r in low_att_df.iterrows():
            att = float(r['Attendance'])
            status_tag = 'DETENTION ORDER ISSUED' if att < 65.0 else 'CONDONATION PENDING (Warning)'
            detained_students.append({
                'student_id': str(r['Student_ID']),
                'name': str(r['Name']),
                'branch': str(r['Branch']),
                'attendance': att,
                'percentage': float(r['Percentage']),
                'status': status_tag,
                'parent_contact': f"+91 98{random.randint(10000000, 99999999)}",
                'notice_sent': 'Yes (SMS & Email)'
            })
            
    return {
        'total_detained_count': len(detained_students),
        'critical_detention_count': sum(1 for s in detained_students if 'DETENTION' in s['status']),
        'condonation_count': sum(1 for s in detained_students if 'CONDONATION' in s['status']),
        'students': detained_students
    }


# ==============================================================================
# 7. COMPREHENSIVE PROCTORING & TASK COMPLIANCE SYSTEM
# (Locked Meetings, University Form/Task Tracking, Bi-Weekly Parent Interaction)
# ==============================================================================

PROCTOR_MEETINGS_FILE = os.path.join(DATA_DIR, 'proctor_meetings.json')
PROCTOR_TASKS_FILE = os.path.join(DATA_DIR, 'proctor_tasks.json')
PARENT_INTERACTIONS_FILE = os.path.join(DATA_DIR, 'parent_interactions.json')

def init_advanced_proctoring_stores():
    df = data_manager.load_data()
    all_sids = df['Student_ID'].tolist() if not df.empty else []
    
    # 1. Seed Locked Proctor Meetings
    if not os.path.exists(PROCTOR_MEETINGS_FILE):
        meetings = [
            {
                'meeting_id': 'MTG-2026-001',
                'faculty_id': '50101',
                'student_id': all_sids[0] if all_sids else '25B11CS380',
                'student_name': 'Kalyanam Mukundha',
                'date': '2026-09-02',
                'time_slot': '03:30 PM - 04:00 PM',
                'purpose': 'DAE Capstone Project Architecture & Semester Progress Review',
                'venue': 'Ramanujan Block - Room 402 (Faculty Cabin)',
                'status': 'Confirmed (Locked)',
                'notes': 'Review backend dataset generation and role authorization modules.'
            },
            {
                'meeting_id': 'MTG-2026-002',
                'faculty_id': '50101',
                'student_id': all_sids[1] if len(all_sids) > 1 else '25B11CS932',
                'student_name': 'Tadicherla Sai Abhiram',
                'date': '2026-09-03',
                'time_slot': '04:00 PM - 04:30 PM',
                'purpose': 'NumPy Mathematical Statistics & Vectorization Review',
                'venue': 'Ramanujan Block - Room 402',
                'status': 'Confirmed (Locked)',
                'notes': 'Validate covariance, Pearson correlation and quartile computations.'
            }
        ]
        save_json_file(PROCTOR_MEETINGS_FILE, meetings)

    # 2. Seed Proctor Assigned University Tasks & Forms
    if not os.path.exists(PROCTOR_TASKS_FILE):
        tasks = [
            {
                'task_id': 'TSK-FORM-101',
                'faculty_id': '50101',
                'title': 'End-Semester Regular Examination Registration & Elective Verification Form',
                'description': 'Mandatory University COE Form: Verify your semester-4 core subjects, open elective choices, and upload biometric attendance declaration.',
                'deadline': '2026-09-05 (05:00 PM)',
                'category': 'University Official Form',
                'assigned_mentees': all_sids[:25] if len(all_sids) >= 25 else ['25B11CS380'],
                'completed_mentees': [all_sids[0] if all_sids else '25B11CS380', all_sids[1] if len(all_sids) > 1 else '25B11CS932']
            },
            {
                'task_id': 'TSK-FORM-102',
                'faculty_id': '50101',
                'title': 'Campus Placement Readiness & Skill Matrix Undertaking (2026-27)',
                'description': 'Training & Placement Cell: Confirm your LeetCode/HackerRank handles, GitHub project links, and resume compliance before MNC drive registrations.',
                'deadline': '2026-09-08 (11:59 PM)',
                'category': 'Placement Compliance',
                'assigned_mentees': all_sids[:25] if len(all_sids) >= 25 else ['25B11CS380'],
                'completed_mentees': [all_sids[0] if all_sids else '25B11CS380']
            },
            {
                'task_id': 'TSK-FORM-103',
                'faculty_id': '50101',
                'title': 'Anti-Ragging & Code of Discipline Digital Affidavit',
                'description': 'University Statutory Compliance: Submit online undertaking reference number verified by parent/guardian.',
                'deadline': '2026-09-10 (04:00 PM)',
                'category': 'Statutory Undertaking',
                'assigned_mentees': all_sids[:25] if len(all_sids) >= 25 else ['25B11CS380'],
                'completed_mentees': []
            }
        ]
        save_json_file(PROCTOR_TASKS_FILE, tasks)

    # 3. Seed Bi-Weekly Parent Interaction & Call Diary
    if not os.path.exists(PARENT_INTERACTIONS_FILE):
        interactions = [
            {
                'call_id': 'PTM-2026-01',
                'faculty_id': '50101',
                'student_id': all_sids[0] if all_sids else '25B11CS380',
                'student_name': 'Kalyanam Mukundha',
                'parent_name': 'K. Venkata Rao (Father)',
                'parent_phone': '+91 98480 12345',
                'scheduled_slot': 'Slot 1: Tuesday (04:00 PM - 04:20 PM)',
                'call_date': '2026-08-25',
                'status': 'Completed',
                'discussion_points': 'Appreciated 93.1% academic score and team lead role in DAE project. Confirmed 98% attendance eligibility.',
                'parent_feedback': 'Parent expressed high satisfaction with university academic progress.'
            },
            {
                'call_id': 'PTM-2026-02',
                'faculty_id': '50101',
                'student_id': all_sids[2] if len(all_sids) > 2 else '25B11CS490',
                'student_name': 'Kovvuri Sameer Reddy',
                'parent_name': 'K. Satyanarayana (Father)',
                'parent_phone': '+91 98480 54321',
                'scheduled_slot': 'Slot 2: Friday (04:30 PM - 04:50 PM)',
                'call_date': '2026-08-28',
                'status': 'Completed',
                'discussion_points': 'Discussed Data Structures tutorial progress and consistent attendance maintenance.',
                'parent_feedback': 'Father confirmed home study schedule of 3 hours daily.'
            },
            {
                'call_id': 'PTM-2026-03',
                'faculty_id': '50101',
                'student_id': all_sids[3] if len(all_sids) > 3 else '25B11CS891',
                'student_name': 'Shaik Sajid',
                'parent_name': 'S. Ibrahim (Father)',
                'parent_phone': '+91 98480 98765',
                'scheduled_slot': 'Slot 3: Next Tuesday (04:00 PM - 04:20 PM)',
                'call_date': '2026-09-01',
                'status': 'Scheduled (Upcoming)',
                'discussion_points': 'Scheduled to discuss UI visualization module and mid-term exam preparation.',
                'parent_feedback': 'Pending interaction.'
            }
        ]
        save_json_file(PARENT_INTERACTIONS_FILE, interactions)

init_advanced_proctoring_stores()


# ==============================================================================
# PROCTOR MEETINGS METHODS
# ==============================================================================

def get_proctor_meetings(faculty_id):
    meetings = load_json_file(PROCTOR_MEETINGS_FILE, [])
    clean_id = str(faculty_id).strip().upper()
    return [m for m in meetings if m.get('faculty_id') == clean_id] or meetings


def schedule_proctor_meeting(faculty_id, student_id, date, time_slot, purpose, venue='Ramanujan Block Room 402', notes=''):
    meetings = load_json_file(PROCTOR_MEETINGS_FILE, [])
    df = data_manager.load_data()
    
    clean_sid = str(student_id).strip().upper()
    s_mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_sid
    s_name = df[s_mask].iloc[0]['Name'] if s_mask.any() else f"Student {clean_sid}"
    
    new_meeting = {
        'meeting_id': f"MTG-2026-{random.randint(100, 999)}",
        'faculty_id': str(faculty_id),
        'student_id': clean_sid,
        'student_name': s_name,
        'date': date,
        'time_slot': time_slot,
        'purpose': purpose,
        'venue': venue,
        'status': 'Confirmed (Locked)',
        'notes': notes
    }
    meetings.insert(0, new_meeting)
    save_json_file(PROCTOR_MEETINGS_FILE, meetings)
    return True, f"Proctoring meeting locked with {s_name} ({clean_sid}) for {date} at {time_slot}.", new_meeting


def get_student_proctor_meetings(student_id):
    meetings = load_json_file(PROCTOR_MEETINGS_FILE, [])
    clean_sid = str(student_id).strip().upper()
    return [m for m in meetings if m.get('student_id', '').upper() == clean_sid]


# ==============================================================================
# PROCTOR UNIVERSITY TASKS & FORMS TRACKING
# ==============================================================================

def get_proctor_tasks(faculty_id):
    tasks = load_json_file(PROCTOR_TASKS_FILE, [])
    df = data_manager.load_data()
    clean_fid = str(faculty_id).strip().upper()
    
    fac_tasks = [t for t in tasks if t.get('faculty_id') == clean_fid] or tasks
    
    # Enrich with completed vs pending student breakdown
    enriched = []
    for t in fac_tasks:
        assigned = t.get('assigned_mentees', [])
        completed_ids = [str(x).upper() for x in t.get('completed_mentees', [])]
        
        completed_list = []
        pending_list = []
        
        for sid in assigned:
            clean_s = str(sid).upper()
            mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_s
            name = df[mask].iloc[0]['Name'] if mask.any() else f"Student {clean_s}"
            branch = df[mask].iloc[0]['Branch'] if mask.any() else "CSE"
            
            s_obj = {'student_id': clean_s, 'name': name, 'branch': branch}
            if clean_s in completed_ids:
                completed_list.append(s_obj)
            else:
                pending_list.append(s_obj)
                
        enriched.append({
            'task_id': t['task_id'],
            'faculty_id': t.get('faculty_id', clean_fid),
            'title': t['title'],
            'description': t['description'],
            'deadline': t['deadline'],
            'category': t['category'],
            'total_assigned': len(assigned),
            'completed_count': len(completed_list),
            'pending_count': len(pending_list),
            'completion_rate': round(len(completed_list) / max(1, len(assigned)) * 100, 1),
            'completed_students': completed_list,
            'pending_students': pending_list
        })
        
    return enriched


def create_proctor_task(faculty_id, title, description, deadline, category):
    tasks = load_json_file(PROCTOR_TASKS_FILE, [])
    faculties = load_json_file(FACULTIES_FILE, [])
    clean_fid = str(faculty_id).strip().upper()
    
    fac = next((f for f in faculties if f['faculty_id'] == clean_fid), None)
    mentee_ids = fac.get('proctee_ids', []) if fac else []
    if not mentee_ids:
        df = data_manager.load_data()
        mentee_ids = df['Student_ID'].head(25).tolist() if not df.empty else []
        
    new_task = {
        'task_id': f"TSK-FORM-{random.randint(100, 999)}",
        'faculty_id': clean_fid,
        'title': title,
        'description': description,
        'deadline': deadline,
        'category': category,
        'assigned_mentees': mentee_ids,
        'completed_mentees': []
    }
    tasks.insert(0, new_task)
    save_json_file(PROCTOR_TASKS_FILE, tasks)
    return True, f"Official form/task broadcasted to all {len(mentee_ids)} assigned mentees."


def get_student_proctor_tasks(student_id):
    tasks = load_json_file(PROCTOR_TASKS_FILE, [])
    clean_sid = str(student_id).strip().upper()
    
    student_tasks = []
    for t in tasks:
        assigned = [str(x).upper() for x in t.get('assigned_mentees', [])]
        completed = [str(x).upper() for x in t.get('completed_mentees', [])]
        
        # If student is assigned (or fallback show all if mentee list generic)
        if clean_sid in assigned or not assigned:
            is_done = clean_sid in completed
            student_tasks.append({
                'task_id': t['task_id'],
                'title': t['title'],
                'description': t['description'],
                'deadline': t['deadline'],
                'category': t['category'],
                'status': 'Completed' if is_done else 'Action Required (Pending)',
                'is_completed': is_done
            })
            
    return student_tasks


def complete_student_task(student_id, task_id, submission_notes='Verified and submitted by student.'):
    tasks = load_json_file(PROCTOR_TASKS_FILE, [])
    clean_sid = str(student_id).strip().upper()
    
    for t in tasks:
        if t.get('task_id') == task_id:
            completed = t.get('completed_mentees', [])
            if clean_sid not in [str(x).upper() for x in completed]:
                completed.append(clean_sid)
                t['completed_mentees'] = completed
                save_json_file(PROCTOR_TASKS_FILE, tasks)
                return True, f"Form {task_id} successfully submitted and registered with your faculty proctor!"
            else:
                return True, "Form was already marked as completed."
                
    return False, "Task not found."


# ==============================================================================
# BI-WEEKLY PARENT INTERACTION METHODS
# ==============================================================================

def get_parent_interactions(faculty_id):
    interactions = load_json_file(PARENT_INTERACTIONS_FILE, [])
    clean_fid = str(faculty_id).strip().upper()
    return [p for p in interactions if p.get('faculty_id') == clean_fid] or interactions


def log_parent_interaction(faculty_id, student_id, parent_name, call_date, discussion_topic, parent_feedback, scheduled_slot='Tuesday Slot'):
    interactions = load_json_file(PARENT_INTERACTIONS_FILE, [])
    df = data_manager.load_data()
    clean_sid = str(student_id).strip().upper()
    
    mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_sid
    s_name = df[mask].iloc[0]['Name'] if mask.any() else f"Student {clean_sid}"
    
    new_call = {
        'call_id': f"PTM-2026-{random.randint(10, 99)}",
        'faculty_id': str(faculty_id),
        'student_id': clean_sid,
        'student_name': s_name,
        'parent_name': parent_name,
        'parent_phone': f"+91 98480 {random.randint(10000, 99999)}",
        'scheduled_slot': scheduled_slot,
        'call_date': call_date,
        'status': 'Completed',
        'discussion_points': discussion_topic,
        'parent_feedback': parent_feedback
    }
    interactions.insert(0, new_call)
    save_json_file(PARENT_INTERACTIONS_FILE, interactions)
    return True, f"Parent interaction logged for {s_name} with parent {parent_name}."


# ==============================================================================
# 8. STUDENT SUBJECT-WISE ATTENDANCE, PERIOD LOGS & SMART CALCULATOR
# ==============================================================================

def get_student_detailed_attendance(student_id):
    df = data_manager.load_data()
    clean_sid = str(student_id).strip().upper()
    s_mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_sid
    
    if not s_mask.any():
        if not df.empty:
            row = df.iloc[0]
            clean_sid = str(row['Student_ID'])
        else:
            return {}
    else:
        row = df[s_mask].iloc[0]
        
    overall_att = float(row['Attendance'])
    
    # Deterministic base seed from student ID
    seed_val = sum(ord(c) for c in clean_sid)
    random.seed(seed_val)
    
    subjects_info = []
    total_conducted = 0
    total_attended = 0
    
    # Core 5 Subjects
    sub_names = [
        ('Python_Programming', 'Python Programming', 'Dr. A. K. Sharma', 48),
        ('Data_Structures', 'Data Structures & Algorithms', 'Dr. K. Venkatesh Rao', 45),
        ('Mathematics', 'Advanced Engineering Mathematics', 'Prof. V. Priya', 50),
        ('Physics', 'Applied Physics & Wave Optics', 'Dr. S. R. Murthy', 42),
        ('English', 'Professional Technical English', 'Dr. Meenakshi Sundaram', 36)
    ]
    
    for col_key, name, fac, conducted in sub_names:
        # Slight variation around the student overall attendance
        variation = random.uniform(-4.5, 4.5)
        sub_pct = max(45.0, min(100.0, overall_att + variation))
        attended = int(round((sub_pct / 100.0) * conducted))
        absent = conducted - attended
        actual_pct = round((attended / conducted) * 100.0, 1)
        
        total_conducted += conducted
        total_attended += attended
        
        # Calculate Safe Bunks vs Required Recovery
        if actual_pct >= 75.0:
            # How many more classes can be missed without dropping below 75%
            # (attended) / (conducted + x) >= 0.75  =>  attended >= 0.75 * conducted + 0.75 * x  =>  x <= (attended - 0.75 * conducted) / 0.75
            safe_bunks = int((attended - 0.75 * conducted) / 0.75)
            calc_msg = f"You can safely miss up to {safe_bunks} more class{'es' if safe_bunks != 1 else ''} and still maintain 75.0% eligibility."
            status_tag = "Eligible for Exam"
            status_class = "badge-success"
        else:
            # How many consecutive classes must be attended to reach 75%
            # (attended + y) / (conducted + y) >= 0.75  =>  attended + y >= 0.75 * conducted + 0.75 * y  =>  0.25 * y >= 0.75 * conducted - attended
            needed = int(((0.75 * conducted - attended) / 0.25) + 0.999)
            needed = max(1, needed)
            calc_msg = f"You must attend the next {needed} consecutive class{'es' if needed != 1 else ''} without absenting to recover to 75.0%."
            status_tag = "Detention Risk (<75%)"
            status_class = "badge-danger"
            
        subjects_info.append({
            'code': col_key,
            'subject_name': name,
            'faculty': fac,
            'conducted': conducted,
            'attended': attended,
            'absent': absent,
            'percentage': actual_pct,
            'is_eligible': actual_pct >= 75.0,
            'status_tag': status_tag,
            'status_class': status_class,
            'calc_message': calc_msg,
            'safe_bunks': safe_bunks if actual_pct >= 75.0 else 0,
            'needed_recovery': needed if actual_pct < 75.0 else 0
        })
        
    actual_overall_pct = round((total_attended / total_conducted) * 100.0, 1)
    
    if actual_overall_pct >= 75.0:
        overall_safe = int((total_attended - 0.75 * total_conducted) / 0.75)
        overall_calc = f"Overall cohort standing: You can miss up to {overall_safe} more periods across all subjects."
    else:
        overall_needed = int(((0.75 * total_conducted - total_attended) / 0.25) + 0.999)
        overall_calc = f"Overall cohort standing: You must attend {overall_needed} consecutive periods to reach university 75.0% threshold."
        
    # Generate Period-by-Period Daily Logs for the last 5 days
    days_labels = [
        ('Today (Friday, 28-Aug-2026)', 'Friday'),
        ('Yesterday (Thursday, 27-Aug-2026)', 'Thursday'),
        ('2 Days Ago (Wednesday, 26-Aug-2026)', 'Wednesday'),
        ('3 Days Ago (Tuesday, 25-Aug-2026)', 'Tuesday'),
        ('4 Days Ago (Monday, 24-Aug-2026)', 'Monday')
    ]
    
    period_times = [
        (1, '09:00 AM - 09:50 AM'),
        (2, '09:50 AM - 10:40 AM'),
        (3, '10:50 AM - 11:40 AM'),
        (4, '11:40 AM - 12:30 PM'),
        (5, '01:30 PM - 02:20 PM'),
        (6, '02:20 PM - 03:10 PM'),
        (7, '03:10 PM - 04:00 PM')
    ]
    
    timetable = load_json_file(TIMETABLE_FILE, {})
    daily_period_logs = []
    absence_alerts = []
    
    for date_label, day_name in days_labels:
        day_schedule = timetable.get(day_name, [])
        periods_list = []
        
        for idx, (p_num, p_time) in enumerate(period_times):
            slot = day_schedule[idx % len(day_schedule)] if day_schedule else {}
            sub_title = slot.get('subject_name', 'Python Programming')
            fac_name = slot.get('faculty', 'Dr. A. K. Sharma')
            room_name = slot.get('room', 'Lab 3 (Turing Block)')
            
            # Deterministic presence check based on date, period, student
            p_seed = seed_val + p_num * 17 + len(day_name) * 31
            p_rand = (p_seed % 100)
            is_present = (p_rand < actual_overall_pct)
            
            p_entry = {
                'period': p_num,
                'time': p_time,
                'subject': sub_title,
                'faculty': fac_name,
                'room': room_name,
                'status': 'Present' if is_present else 'Absent',
                'badge_class': 'badge-success' if is_present else 'badge-danger'
            }
            periods_list.append(p_entry)
            
            if not is_present:
                absence_alerts.append({
                    'date': date_label.split(' (')[0],
                    'day': day_name,
                    'period': f"Period {p_num} ({p_time})",
                    'subject': sub_title,
                    'faculty': fac_name,
                    'room': room_name,
                    'alert_text': f"Marked Absent in {sub_title} ({p_time}) on {day_name}."
                })
                
        daily_period_logs.append({
            'date_label': date_label,
            'day_name': day_name,
            'periods': periods_list,
            'day_present_count': sum(1 for p in periods_list if p['status'] == 'Present'),
            'day_total_count': len(periods_list)
        })
        
    return {
        'student_id': clean_sid,
        'student_name': str(row['Name']),
        'branch': str(row['Branch']),
        'overall_percentage': actual_overall_pct,
        'total_conducted': total_conducted,
        'total_attended': total_attended,
        'total_absent': total_conducted - total_attended,
        'is_overall_eligible': actual_overall_pct >= 75.0,
        'overall_calc_message': overall_calc,
        'subjects': subjects_info,
        'daily_period_logs': daily_period_logs,
        'absence_alerts': absence_alerts[:8]
    }


# ==============================================================================
# 9. STUDENT-FACULTY MEETING BOOKING & CONFIRMATION WORKFLOW
# ==============================================================================

def student_request_meeting(student_id, faculty_id, requested_date, requested_time, purpose, student_notes=''):
    meetings = load_json_file(PROCTOR_MEETINGS_FILE, [])
    df = data_manager.load_data()
    clean_sid = str(student_id).strip().upper()
    
    s_mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_sid
    s_name = df[s_mask].iloc[0]['Name'] if s_mask.any() else f"Student {clean_sid}"
    
    new_request = {
        'meeting_id': f"MTG-REQ-{random.randint(100, 999)}",
        'faculty_id': str(faculty_id),
        'student_id': clean_sid,
        'student_name': s_name,
        'date': requested_date,
        'time_slot': requested_time,
        'purpose': purpose,
        'venue': 'Ramanujan Block - Room 402 (Faculty Office)',
        'status': 'Pending Faculty Approval',
        'requested_by': 'Student',
        'notes': student_notes,
        'requested_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    meetings.insert(0, new_request)
    save_json_file(PROCTOR_MEETINGS_FILE, meetings)
    return True, f"Meeting request submitted! Your faculty mentor ({faculty_id}) will review and confirm the time slot.", new_request


def faculty_respond_meeting(faculty_id, meeting_id, action, confirmed_date=None, confirmed_time=None, venue=None, remarks=''):
    meetings = load_json_file(PROCTOR_MEETINGS_FILE, [])
    clean_fid = str(faculty_id).strip().upper()
    
    for m in meetings:
        if m.get('meeting_id') == meeting_id:
            if action.lower() in ['accept', 'confirm']:
                m['status'] = 'Confirmed (Accepted)'
                if confirmed_date:
                    m['date'] = confirmed_date
                if confirmed_time:
                    m['time_slot'] = confirmed_time
                if venue:
                    m['venue'] = venue
                if remarks:
                    m['notes'] = remarks
                msg = f"Meeting with {m.get('student_name')} confirmed for {m.get('date')} at {m.get('time_slot')} in {m.get('venue')}."
            else:
                m['status'] = 'Declined / Rescheduled'
                if remarks:
                    m['notes'] = remarks
                msg = f"Meeting request {meeting_id} has been declined."
                
            save_json_file(PROCTOR_MEETINGS_FILE, meetings)
            return True, msg, m
            
    return False, "Meeting request not found.", None


# ==============================================================================
# 10. COMPREHENSIVE STUDENT OFFICIAL PROFILE & MULTI-SEMESTER MARKS LEDGER
# ==============================================================================

def get_student_complete_profile(student_id):
    df = data_manager.load_data()
    clean_sid = str(student_id).strip().upper()
    s_mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_sid
    
    if not s_mask.any():
        if not df.empty:
            row = df.iloc[0]
            clean_sid = str(row['Student_ID'])
        else:
            return {}
    else:
        row = df[s_mask].iloc[0]
        
    s_name = str(row['Name'])
    s_branch = str(row['Branch'])
    s_att = float(row['Attendance'])
    s_pct = float(row['Percentage'])
    s_grade = str(row['Grade'])
    
    # Deterministic generation based on student ID
    seed_val = sum(ord(c) for c in clean_sid)
    random.seed(seed_val)
    
    # Names database
    surname = s_name.split()[0] if len(s_name.split()) > 1 else "Kalyanam"
    father_first = random.choice(["Venkata Rao", "Satyanarayana", "Srinivasa Rao", "Appa Rao", "Subrahmanyam", "Ramana Murthy"])
    mother_first = random.choice(["Lakshmi", "Satyavathi", "Padmavathi", "Kalyani", "Sita Devi", "Rajeshwari"])
    
    father_name = f"{surname} {father_first}"
    mother_name = f"{surname} {mother_first}"
    
    # 3 Separate Mobile Numbers
    student_mobile = f"+91 98{random.randint(48000000, 48999999)}"
    father_mobile = f"+91 94{random.randint(40000000, 40999999)}"
    mother_mobile = f"+91 99{random.randint(89000000, 89999999)}"
    
    # Clean email addresses
    clean_name_slug = s_name.lower().replace(" ", ".")
    college_email = f"{clean_sid.lower()}@aditya.ac.in"
    personal_email = f"{clean_name_slug}@gmail.com"
    
    # Addresses in Andhra Pradesh
    towns = [
        "Surampalem, ADB Road, Gandepalli Mandal, Kakinada Dist - 533437",
        "Danavaipeta, Rajamahendravaram, East Godavari Dist - 533103",
        "Srinagar Colony, Kakinada, Kakinada Dist - 533003",
        "Bhanugudi Junction, Kakinada - 533005",
        "Main Road, Mandapeta, Dr. B.R. Ambedkar Konaseema Dist - 533308",
        "Vidyut Nagar, Rajahmundry - 533105"
    ]
    address = towns[seed_val % len(towns)]
    
    # Prior Academics: SSC & Intermediate
    ssc_total = random.randint(560, 595)
    ssc_pct = round((ssc_total / 600.0) * 100.0, 2)
    ssc_gpa = round(min(10.0, ssc_pct / 9.5), 1)
    
    inter_total = random.randint(940, 990)
    inter_pct = round((inter_total / 1000.0) * 100.0, 2)
    eapcet_rank = random.randint(1800, 9500)
    
    prior_academics = {
        'ssc': {
            'board': 'Board of Secondary Education, Andhra Pradesh (BSEAP)',
            'school_name': 'Aditya High School, Kakinada',
            'hall_ticket_no': f"22{random.randint(100000, 999999)}",
            'year_of_passing': '2022',
            'max_marks': 600,
            'marks_secured': ssc_total,
            'percentage': ssc_pct,
            'cgpa': ssc_gpa,
            'division': 'First Class with Distinction'
        },
        'intermediate': {
            'board': 'Board of Intermediate Education, Andhra Pradesh (BIEAP)',
            'college_name': 'Aditya Junior College, Srinagar, Kakinada',
            'group': 'MPC (Mathematics, Physics, Chemistry)',
            'hall_ticket_no': f"24{random.randint(100000, 999999)}",
            'year_of_passing': '2024',
            'max_marks': 1000,
            'marks_secured': inter_total,
            'percentage': inter_pct,
            'eapcet_rank': f"Rank {eapcet_rank:,}",
            'division': 'First Class with Distinction'
        }
    }
    
    # Multi-Semester Comprehensive Ledger (Internal Mid-1, Mid-2, Internal Avg, External, Total, Grade)
    semesters_data = []
    
    sem_curriculums = [
        ('Semester 1 (Autumn 2024)', 9.24, [
            ('Linear Algebra & Calculus', 'BS-MA101', 4),
            ('Engineering Physics & Quantum Optics', 'BS-PH102', 4),
            ('Problem Solving using C Programming', 'ES-CS103', 3),
            ('Basic Electrical & Electronics Engineering', 'ES-EE104', 3),
            ('Engineering Graphics & CAD Lab', 'ES-ME105', 2),
            ('C Programming & Algorithms Lab', 'ES-CS106', 2)
        ]),
        ('Semester 2 (Spring 2025)', 9.18, [
            ('Differential Equations & Numerical Methods', 'BS-MA201', 4),
            ('Engineering Chemistry & Material Science', 'BS-CH202', 4),
            ('Object Oriented Programming through Java', 'PC-CS203', 3),
            ('Digital Logic Design & Microprocessors', 'PC-CS204', 3),
            ('Python Programming Lab', 'PC-CS205', 2),
            ('Language & Communication Skills Lab', 'HS-EN206', 2)
        ]),
        ('Semester 3 (Autumn 2025)', 9.35, [
            ('Discrete Mathematics & Graph Theory', 'BS-MA301', 4),
            ('Data Structures & Algorithms in C++', 'PC-CS302', 4),
            ('Computer Organization & Architecture', 'PC-CS303', 3),
            ('Database Management Systems (SQL)', 'PC-CS304', 3),
            ('Data Structures Lab', 'PC-CS305', 2),
            ('DBMS & SQL Workbench Lab', 'PC-CS306', 2)
        ]),
        ('Semester 4 (Spring 2026 - Current)', round(min(10.0, s_pct / 10.0), 2), [
            ('Python Programming', 'PC-CS401', 4),
            ('Data Structures', 'PC-CS402', 4),
            ('Mathematics', 'BS-MA403', 4),
            ('Physics', 'BS-PH404', 3),
            ('English', 'HS-EN405', 3),
            ('Advanced Data Analytics & AI Capstone Lab', 'PC-CS406', 2)
        ])
    ]
    
    total_credits = 0
    weighted_gp = 0.0
    
    for sem_title, sem_sgpa, subjects_list in sem_curriculums:
        sub_records = []
        sem_credits = 0
        sem_weighted = 0.0
        
        for s_title, code, credits in subjects_list:
            sem_credits += credits
            # Generate Mid-1 (30M), Mid-2 (30M), Internal Avg (30M), External (70M), Total (100M)
            # Match current semester marks with dataset if present
            if 'Semester 4' in sem_title and s_title in df.columns:
                tot = float(row[s_title])
                ext = round(tot * 0.70, 1)
                mid1 = min(30, int(round(tot * 0.28 + random.uniform(-1, 1))))
                mid2 = min(30, int(round(tot * 0.29 + random.uniform(-1, 1))))
                int_avg = round((mid1 + mid2) / 2.0, 1)
            else:
                base = random.randint(75, 96)
                mid1 = random.randint(24, 30)
                mid2 = random.randint(25, 30)
                int_avg = round((mid1 + mid2) / 2.0, 1)
                ext = round(base * 0.70, 1)
                tot = round(int_avg + ext, 1)
                
            tot = min(100.0, max(40.0, tot))
            grade_char = 'A+' if tot >= 90 else ('A' if tot >= 80 else ('B' if tot >= 70 else ('C' if tot >= 60 else ('D' if tot >= 50 else 'P'))))
            gp = 10 if grade_char == 'A+' else (9 if grade_char == 'A' else (8 if grade_char == 'B' else (7 if grade_char == 'C' else 6)))
            
            sem_weighted += (gp * credits)
            
            sub_records.append({
                'subject_name': s_title,
                'course_code': code,
                'credits': credits,
                'mid1_marks': mid1,
                'mid2_marks': mid2,
                'internal_avg': int_avg,
                'external_marks': ext,
                'total_marks': tot,
                'grade_letter': grade_char,
                'grade_points': gp,
                'status': 'PASS' if tot >= 40.0 else 'FAIL'
            })
            
        calculated_sgpa = round(sem_weighted / sem_credits, 2)
        total_credits += sem_credits
        weighted_gp += sem_weighted
        
        semesters_data.append({
            'semester_title': sem_title,
            'sgpa': calculated_sgpa,
            'total_credits': sem_credits,
            'subjects': sub_records
        })
        
    cgpa = round(weighted_gp / total_credits, 2)
    
    return {
        'student_id': clean_sid,
        'name': s_name,
        'branch': s_branch,
        'semester': 'Semester 4 (B.Tech 2nd Year)',
        'section': 'Section A',
        'roll_number': clean_sid,
        'admission_category': 'Convener Quota (EAPCET Merit Category-A)',
        'academic_year': '2024 - 2028 Batch',
        'dob': '14-Aug-2005',
        'blood_group': random.choice(['O+ve', 'A+ve', 'B+ve', 'AB+ve']),
        'father_name': father_name,
        'mother_name': mother_name,
        'student_mobile': student_mobile,
        'father_mobile': father_mobile,
        'mother_mobile': mother_mobile,
        'college_email': college_email,
        'personal_email': personal_email,
        'address': address,
        'mentor_name': 'Dr. A. K. Sharma (Professor & Proctor)',
        'overall_cgpa': cgpa,
        'overall_percentage': s_pct,
        'overall_attendance': s_att,
        'grade': s_grade,
        'prior_academics': prior_academics,
        'semesters_ledger': semesters_data
    }


# ==============================================================================
# ==============================================================================
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

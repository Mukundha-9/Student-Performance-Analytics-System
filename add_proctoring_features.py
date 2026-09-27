# add_proctoring_features.py
import os

code = """

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
"""

with open('portal_manager.py', 'a', encoding='utf-8') as f:
    f.write(code)
print('Successfully appended comprehensive Proctoring & Task Compliance logic to portal_manager.py')

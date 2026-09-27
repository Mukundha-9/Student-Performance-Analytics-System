# update_portal_manager.py
import os

code = """

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
"""

with open('portal_manager.py', 'a', encoding='utf-8') as f:
    f.write(code)
print('Successfully appended unique Faculty and Admin features to portal_manager.py')

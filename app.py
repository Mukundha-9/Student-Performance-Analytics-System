# ==============================================================================
# Flask Web Backend & REST API Server - Aditya University Analytics Portal
# Multi-Role Support: Student Portal | Faculty Portal | University Admin Portal
# ==============================================================================
import os
import json
import io
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from config import (
    BASE_DIR,
    DATA_DIR,
    REPORTS_DIR,
    DEFAULT_CSV_PATH,
    INSTITUTION,
    DEPARTMENT,
    PROJECT_TITLE,
    TEAM_MEMBERS,
    SUBJECTS,
    BRANCHES,
    SEMESTERS
)
import data_manager
import analytics
import visualizer
import sample_data
import portal_manager
import generate_report

app = Flask(__name__)
INTERVENTIONS_FILE = os.path.join(DATA_DIR, 'interventions.json')


def load_interventions():
    if os.path.exists(INTERVENTIONS_FILE):
        try:
            with open(INTERVENTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_interventions(data):
    with open(INTERVENTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


# ==============================================================================
# AUTHENTICATION & DEMO USERS API
# ==============================================================================

@app.route('/api/auth/demo-users', methods=['GET'])
def get_demo_users():
    demos = portal_manager.get_demo_user_list()
    return jsonify(demos)


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    role = data.get('role', 'student')
    username = data.get('username', '')
    password = data.get('password', '')

    user_profile = portal_manager.authenticate_user(role, username, password)
    if user_profile:
        return jsonify({
            'success': True,
            'user': user_profile,
            'message': f"Welcome back, {user_profile['name']}!"
        })

    return jsonify({
        'success': False,
        'message': 'Invalid credentials. Please verify your ID or select a Demo Profile.'
    }), 401


# ==============================================================================
# STUDENT PORTAL API
# ==============================================================================

@app.route('/api/student/timetable/<student_id>', methods=['GET'])
def get_timetable(student_id):
    tt = portal_manager.get_student_timetable(student_id)
    return jsonify(tt)


@app.route('/api/student/faculties/<student_id>', methods=['GET'])
def get_student_faculties(student_id):
    facs = portal_manager.get_student_faculties(student_id)
    return jsonify(facs)


@app.route('/api/student/fees/<student_id>', methods=['GET'])
def get_student_fees(student_id):
    fees = portal_manager.get_student_fees(student_id)
    return jsonify(fees)


@app.route('/api/student/pay-fee', methods=['POST'])
def pay_fee():
    data = request.get_json() or {}
    student_id = data.get('student_id')
    amount = data.get('amount', 0)
    mode = data.get('mode', 'UPI / NetBanking')

    success, msg, receipt = portal_manager.pay_student_fee(student_id, amount, mode)
    if success:
        return jsonify({'success': True, 'message': msg, 'receipt': receipt}), 200
    return jsonify({'success': False, 'message': msg}), 400


@app.route('/api/student/hall-ticket/<student_id>', methods=['GET'])
def get_hall_ticket(student_id):
    ht = portal_manager.get_student_hall_ticket(student_id)
    return jsonify(ht)


# ==============================================================================
# FACULTY PORTAL API
# ==============================================================================

@app.route('/api/faculty/dashboard/<faculty_id>', methods=['GET'])
def get_faculty_dashboard(faculty_id):
    dash = portal_manager.get_faculty_dashboard(faculty_id)
    return jsonify(dash)


@app.route('/api/faculty/roster', methods=['GET'])
def get_faculty_roster():
    branch = request.args.get('branch', 'Computer Science & Engineering')
    df = data_manager.load_data()
    filtered = df[df['Branch'] == branch] if not df.empty and branch != 'All' else df
    roster = []
    for _, r in filtered.iterrows():
        roster.append({
            'student_id': str(r['Student_ID']),
            'name': str(r['Name']),
            'attendance': float(r['Attendance']),
            'status': 'Present'
        })
    return jsonify({'roster': roster, 'total': len(roster)})


@app.route('/api/faculty/post-attendance', methods=['POST'])
def post_attendance():
    data = request.get_json() or {}
    subject = data.get('subject', 'Python_Programming')
    date = data.get('date', 'Today')
    records = data.get('attendance', {})

    success, msg = portal_manager.post_daily_attendance(subject, date, records)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/faculty/post-marks', methods=['POST'])
def post_marks():
    data = request.get_json() or {}
    subject = data.get('subject', 'Python_Programming')
    marks_dict = data.get('marks', {})

    success, msg = portal_manager.post_subject_marks(subject, marks_dict)
    return jsonify({'success': success, 'message': msg})


# ==============================================================================
# ADMIN PORTAL API (ANNOUNCEMENTS & RESULTS)
# ==============================================================================

@app.route('/api/announcements', methods=['GET'])
@app.route('/api/admin/announcements', methods=['GET', 'POST'])
def handle_announcements():
    ann_file = os.path.join(DATA_DIR, 'announcements.json')
    announcements = portal_manager.load_json_file(ann_file, [])

    if request.method == 'POST':
        data = request.get_json() or {}
        new_item = {
            'id': len(announcements) + 1,
            'title': data.get('title', 'Official Notice'),
            'category': data.get('category', 'Academic'),
            'badge_class': 'badge-warning' if data.get('category') == 'Academic' else 'badge-danger' if data.get('category') == 'Exam' else 'badge-success',
            'author': data.get('author', 'Office of Registrar'),
            'date': '2026-08-28',
            'target': data.get('target', 'All'),
            'content': data.get('content', '')
        }
        announcements.insert(0, new_item)
        portal_manager.save_json_file(ann_file, announcements)
        return jsonify({'success': True, 'message': 'Announcement published to campus network!', 'item': new_item}), 201

    return jsonify({'announcements': announcements})


@app.route('/api/admin/announcements/<int:ann_id>', methods=['DELETE'])
def delete_announcement(ann_id):
    ann_file = os.path.join(DATA_DIR, 'announcements.json')
    announcements = portal_manager.load_json_file(ann_file, [])
    announcements = [a for a in announcements if a.get('id') != ann_id]
    portal_manager.save_json_file(ann_file, announcements)
    return jsonify({'success': True, 'message': 'Announcement deleted'})


# ==============================================================================
# CORE DAE ANALYTICS & CRUD API
# ==============================================================================

@app.route('/api/summary', methods=['GET'])
def get_summary():
    df = data_manager.load_data()
    overall = analytics.compute_overall_statistics(df)
    sub_stats = analytics.compute_subject_statistics(df)
    corr = analytics.compute_attendance_correlation(df)
    grades = analytics.compute_grade_distribution(df)
    branches = analytics.compute_branch_analytics(df)
    toppers = data_manager.get_top_performers(df, top_n=10)
    at_risk = analytics.identify_at_risk_students(df)

    low_att_count = int((df['Attendance'] < 75.0).sum()) if not df.empty else 0

    return jsonify({
        'overall': overall,
        'subject_stats': sub_stats,
        'correlation': corr,
        'grade_distribution': grades,
        'branch_stats': branches,
        'top_10': toppers.to_dict(orient='records'),
        'at_risk_count': len(at_risk),
        'at_risk_students': at_risk[:15],
        'low_attendance_count': low_att_count,
        'institution': INSTITUTION,
        'department': DEPARTMENT,
        'project_title': PROJECT_TITLE,
        'team_members': TEAM_MEMBERS
    })


@app.route('/api/students', methods=['GET'])
def get_students():
    df = data_manager.load_data()

    query = request.args.get('q', '')
    branch = request.args.get('branch', 'All')
    grade = request.args.get('grade', 'All')
    status = request.args.get('status', 'All')
    min_att = request.args.get('min_attendance', None)
    max_att = request.args.get('max_attendance', None)

    min_att_val = float(min_att) if min_att else None
    max_att_val = float(max_att) if max_att else None

    filtered_df = data_manager.search_and_filter(
        df,
        query=query if query else None,
        branch=branch if branch != 'All' else None,
        grade=grade if grade != 'All' else None,
        status=status if status != 'All' else None,
        min_att=min_att_val,
        max_att=max_att_val
    )

    sort_by = request.args.get('sort_by', 'Percentage')
    order = request.args.get('order', 'desc')
    ascending = (order == 'asc')
    if sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    total_records = len(filtered_df)
    total_pages = max(1, (total_records + page_size - 1) // page_size)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_df = filtered_df.iloc[start_idx:end_idx]

    return jsonify({
        'total': total_records,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'records': paginated_df.to_dict(orient='records')
    })


@app.route('/api/student/<student_id>', methods=['GET'])
def get_student(student_id):
    df = data_manager.load_data()
    clean_id = str(student_id).strip().upper()
    card = analytics.get_student_rank_card(df, clean_id)
    if not card and not df.empty:
        card = analytics.get_student_rank_card(df, df.iloc[0]['Student_ID'])
    if not card:
        return jsonify({'error': f'Student {student_id} not found'}), 404
    return jsonify(card)


@app.route('/api/student', methods=['POST'])
def add_student():
    df = data_manager.load_data()
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    updated_df, success, message = data_manager.add_student(df, data)
    if success:
        return jsonify({'success': True, 'message': message}), 201
    return jsonify({'success': False, 'message': message}), 400


@app.route('/api/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    df = data_manager.load_data()
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    updated_df, success, message = data_manager.update_student(df, student_id, data)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


@app.route('/api/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    df = data_manager.load_data()
    updated_df, success, message = data_manager.delete_student(df, student_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400


@app.route('/api/ai-insights/<student_id>', methods=['GET'])
def get_ai_student_insights(student_id):
    df = data_manager.load_data()
    clean_id = str(student_id).strip().upper()
    mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_id
    if not mask.any() and not df.empty:
        student_id = str(df.iloc[0]['Student_ID'])

    insights = analytics.generate_ai_student_insights(df, student_id)
    if not insights:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(insights)


@app.route('/api/ai-cohort-insights', methods=['GET'])
def get_ai_cohort_insights():
    df = data_manager.load_data()
    insights = analytics.generate_cohort_executive_insights(df)
    return jsonify(insights)


@app.route('/api/compare', methods=['GET'])
def compare_entities():
    df = data_manager.load_data()
    id1 = request.args.get('id1', '').strip().upper()
    if not id1 or not (df['Student_ID'].astype(str).str.strip().str.upper() == id1).any():
        id1 = str(df.iloc[0]['Student_ID'])

    id2 = request.args.get('id2', 'branch_avg').strip()
    if id2 not in ['branch_avg', 'topper']:
        if not (df['Student_ID'].astype(str).str.strip().str.upper() == id2.upper()).any():
            id2 = 'branch_avg'

    comp = analytics.compare_two_entities(df, id1, id2)
    if not comp:
        return jsonify({'error': 'Comparison entities not found'}), 404
    return jsonify(comp)


@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    data = request.get_json() or {}
    student_id = str(data.get('student_id', '')).strip().upper()
    new_att = float(data.get('attendance', 85.0))
    deltas = data.get('marks_delta', {})

    df = data_manager.load_data()
    if not student_id or not (df['Student_ID'].astype(str).str.strip().str.upper() == student_id).any():
        student_id = str(df.iloc[0]['Student_ID'])

    res = analytics.simulate_grade_impact(df, student_id, new_att, deltas)
    if not res:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(res)


@app.route('/api/interventions', methods=['GET', 'POST'])
def manage_interventions():
    if request.method == 'POST':
        data = request.get_json() or {}
        interventions = load_interventions()
        item = {
            'id': len(interventions) + 1,
            'student_id': data.get('student_id'),
            'student_name': data.get('student_name'),
            'faculty_name': data.get('faculty_name', 'Faculty Mentor'),
            'action_type': data.get('action_type', 'Remedial Tutorial'),
            'notes': data.get('notes', ''),
            'status': data.get('status', 'In Progress'),
            'date': 'Today'
        }
        interventions.append(item)
        save_interventions(interventions)
        return jsonify({'success': True, 'item': item}), 201

    return jsonify({'interventions': load_interventions()})


@app.route('/api/certificate/<student_id>', methods=['GET'])
def get_certificate(student_id):
    df = data_manager.load_data()
    card = analytics.get_student_rank_card(df, student_id)
    if not card and not df.empty:
        card = analytics.get_student_rank_card(df, df.iloc[0]['Student_ID'])
    if not card:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify({
        'student_id': card['student_id'],
        'name': card['name'],
        'branch': card['branch'],
        'percentage': card['percentage'],
        'grade': card['grade'],
        'class_rank': card['class_rank'],
        'institution': INSTITUTION,
        'department': DEPARTMENT,
        'issue_date': 'Academic Year 2025-2026'
    })


@app.route('/api/charts/list', methods=['GET'])
def list_charts():
    chart_info = [
        {'id': 1, 'filename': '01_subject_averages.png', 'name': 'Subject-Wise Performance (Min, Mean, Max)', 'type': 'Bar Chart'},
        {'id': 2, 'filename': '02_grade_distribution.png', 'name': 'Academic Grade Distribution & Donut', 'type': 'Donut Chart'},
        {'id': 3, 'filename': '03_score_distribution.png', 'name': 'Class Marks Distribution & Gaussian Bell Curve', 'type': 'Histogram'},
        {'id': 4, 'filename': '04_attendance_correlation.png', 'name': 'Attendance vs Academic Score Regression', 'type': 'Scatter Plot'},
        {'id': 5, 'filename': '05_performance_trends.png', 'name': 'Cohort Academic Progression & Percentile Bands', 'type': 'Line Chart'},
        {'id': 6, 'filename': '06_department_comparison.png', 'name': 'Branch-Wise Performance Comparison', 'type': 'Box Plot'},
        {'id': 7, 'filename': '07_comprehensive_dashboard.png', 'name': '4-in-1 Executive Performance Analytics Dashboard', 'type': 'Multi-Panel Dashboard'}
    ]
    return jsonify({'charts': chart_info})


@app.route('/api/charts/<filename>', methods=['GET'])
def get_chart_image(filename):
    file_path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(file_path):
        df = data_manager.load_data()
        visualizer.save_all_visualizations(df)
    return send_from_directory(REPORTS_DIR, filename)


@app.route('/api/export-csv', methods=['GET'])
def export_csv():
    df = data_manager.load_data()
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return send_file(
        io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='aditya_students_performance_data.csv'
    )


@app.route('/api/regenerate', methods=['POST'])
def regenerate_data():
    df = sample_data.generate_sample_dataset(500)
    visualizer.save_all_visualizations(df)
    portal_manager.init_portal_data()
    return jsonify({
        'success': True,
        'message': f'Successfully regenerated official dataset with {len(df)} records.'
    })


@app.route('/api/report/markdown', methods=['GET'])
def get_report_markdown():
    report_file = os.path.join(REPORTS_DIR, 'academic_performance_report.md')
    if not os.path.exists(report_file):
        df = data_manager.load_data()
        generate_report.generate_academic_report(df)
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception:
        df = data_manager.load_data()
        md_content = generate_report.generate_academic_report(df)
    return jsonify({'markdown': md_content})


@app.route('/api/faculty/remedial-plan/<faculty_id>', methods=['GET'])
def get_faculty_remedial(faculty_id):
    plan = portal_manager.get_faculty_remedial_plan(faculty_id)
    return jsonify(plan)


@app.route('/api/faculty/leaves', methods=['GET', 'POST'])
def manage_faculty_leaves():
    if request.method == 'POST':
        data = request.get_json() or {}
        fac_id = data.get('faculty_id', '50101')
        date = data.get('date', 'Tomorrow')
        l_type = data.get('leave_type', 'Casual Leave')
        sub = data.get('substitute_faculty', 'Prof. V. Priya')
        slot = data.get('slot_details', 'Period 1 & 2 in Lab-3')
        success, msg = portal_manager.apply_faculty_leave(fac_id, date, l_type, sub, slot)
        return jsonify({'success': success, 'message': msg})
    fac_id = request.args.get('faculty_id', '50101')
    return jsonify({'leaves': portal_manager.get_faculty_leaves(fac_id)})


@app.route('/api/admin/moderation-status', methods=['GET'])
def get_moderation_status():
    return jsonify(portal_manager.get_admin_moderation_status())


@app.route('/api/admin/apply-moderation', methods=['POST'])
def apply_moderation():
    data = request.get_json() or {}
    grace = int(data.get('grace_marks', 3))
    success, msg = portal_manager.apply_admin_moderation(grace)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/admin/toggle-result-publish', methods=['POST'])
def toggle_result_publishing():
    success, msg = portal_manager.toggle_result_publishing()
    return jsonify({'success': success, 'message': msg})


@app.route('/api/admin/accreditation-audit', methods=['GET'])
def get_accreditation_audit():
    return jsonify(portal_manager.get_admin_accreditation_audit())


@app.route('/api/admin/detention-list', methods=['GET'])
def get_detention_list():
    return jsonify(portal_manager.get_admin_detention_list())


@app.route('/api/proctor/meetings/<faculty_id>', methods=['GET'])
def get_proctor_meetings_api(faculty_id):
    return jsonify({'meetings': portal_manager.get_proctor_meetings(faculty_id)})


@app.route('/api/proctor/schedule-meeting', methods=['POST'])
def schedule_meeting_api():
    data = request.get_json() or {}
    fac_id = data.get('faculty_id', '50101')
    s_id = data.get('student_id')
    date = data.get('date')
    time_slot = data.get('time_slot')
    purpose = data.get('purpose')
    venue = data.get('venue', 'Ramanujan Block - Room 402')
    notes = data.get('notes', '')
    success, msg, item = portal_manager.schedule_proctor_meeting(fac_id, s_id, date, time_slot, purpose, venue, notes)
    return jsonify({'success': success, 'message': msg, 'item': item})


@app.route('/api/student/proctor-meetings/<student_id>', methods=['GET'])
def get_student_meetings_api(student_id):
    return jsonify({'meetings': portal_manager.get_student_proctor_meetings(student_id)})


@app.route('/api/proctor/tasks/<faculty_id>', methods=['GET'])
def get_proctor_tasks_api(faculty_id):
    return jsonify({'tasks': portal_manager.get_proctor_tasks(faculty_id)})


@app.route('/api/proctor/create-task', methods=['POST'])
def create_task_api():
    data = request.get_json() or {}
    fac_id = data.get('faculty_id', '50101')
    title = data.get('title')
    desc = data.get('description')
    deadline = data.get('deadline')
    category = data.get('category', 'University Official Form')
    success, msg = portal_manager.create_proctor_task(fac_id, title, desc, deadline, category)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/student/proctor-tasks/<student_id>', methods=['GET'])
def get_student_tasks_api(student_id):
    return jsonify({'tasks': portal_manager.get_student_proctor_tasks(student_id)})


@app.route('/api/student/complete-task', methods=['POST'])
def complete_task_api():
    data = request.get_json() or {}
    s_id = data.get('student_id')
    t_id = data.get('task_id')
    notes = data.get('submission_notes', 'Completed and verified.')
    success, msg = portal_manager.complete_student_task(s_id, t_id, notes)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/proctor/parent-interactions/<faculty_id>', methods=['GET'])
def get_parent_interactions_api(faculty_id):
    return jsonify({'interactions': portal_manager.get_parent_interactions(faculty_id)})


@app.route('/api/proctor/log-parent-call', methods=['POST'])
def log_parent_call_api():
    data = request.get_json() or {}
    fac_id = data.get('faculty_id', '50101')
    s_id = data.get('student_id')
    p_name = data.get('parent_name')
    date = data.get('call_date', 'Today')
    topic = data.get('discussion_topic')
    feedback = data.get('parent_feedback')
    slot = data.get('scheduled_slot', 'Tuesday Slot')
    success, msg = portal_manager.log_parent_interaction(fac_id, s_id, p_name, date, topic, feedback, slot)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/student/detailed-attendance/<student_id>', methods=['GET'])
def get_student_detailed_attendance_api(student_id):
    data = portal_manager.get_student_detailed_attendance(student_id)
    return jsonify(data)


@app.route('/api/student/request-meeting', methods=['POST'])
def request_meeting_api():
    data = request.get_json() or {}
    s_id = data.get('student_id')
    fac_id = data.get('faculty_id', '50101')
    date = data.get('date')
    time_slot = data.get('time_slot')
    purpose = data.get('purpose')
    notes = data.get('notes', '')
    success, msg, item = portal_manager.student_request_meeting(s_id, fac_id, date, time_slot, purpose, notes)
    return jsonify({'success': success, 'message': msg, 'item': item})


@app.route('/api/faculty/respond-meeting', methods=['POST'])
def respond_meeting_api():
    data = request.get_json() or {}
    fac_id = data.get('faculty_id', '50101')
    meeting_id = data.get('meeting_id')
    action = data.get('action', 'accept')
    confirmed_date = data.get('confirmed_date')
    confirmed_time = data.get('confirmed_time')
    venue = data.get('venue')
    remarks = data.get('remarks', '')
    success, msg, item = portal_manager.faculty_respond_meeting(fac_id, meeting_id, action, confirmed_date, confirmed_time, venue, remarks)
    return jsonify({'success': success, 'message': msg, 'item': item})


@app.route('/api/student/profile/<student_id>', methods=['GET'])
def get_student_profile_api(student_id):
    profile = portal_manager.get_student_complete_profile(student_id)
    return jsonify(profile)




@app.route('/api/student/assignments/<student_id>', methods=['GET'])
@app.route('/api/student/<student_id>/assignments', methods=['GET'])
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


if __name__ == '__main__':
    print("\n" + "="*70)
    print(f" {INSTITUTION.upper()} - {PROJECT_TITLE.upper()}")
    print(" Local URL:   http://127.0.0.1:5000  (or http://localhost:5000)")
    print(" Network URL: http://192.168.0.199:5000  (for Mobile / Other Devices on Wi-Fi)")
    print(" Multi-Portal Mode: Student | Faculty | Admin Online")
    print("="*70 + "\n")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('RENDER', '').lower() != 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

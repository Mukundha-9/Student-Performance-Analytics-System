# add_attendance_and_booking_features.py
import os

code = """

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
"""

with open('portal_manager.py', 'a', encoding='utf-8') as f:
    f.write(code)
print('Successfully appended Attendance & Meeting Booking logic to portal_manager.py')

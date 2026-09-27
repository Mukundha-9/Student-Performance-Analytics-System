# add_student_profile_backend.py
import os

code = """

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
"""

with open('portal_manager.py', 'a', encoding='utf-8') as f:
    f.write(code)
print('Successfully appended Comprehensive Student Profile and Multi-Semester Ledger to portal_manager.py')

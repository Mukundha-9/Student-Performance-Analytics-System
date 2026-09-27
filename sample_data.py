# ==============================================================================
# Sample Data Generator Module - Aditya University Student Dataset (500 Records)
# Generates realistic academic data using NumPy and Pandas with 100% unique IDs.
# ==============================================================================
import os
import numpy as np
import pandas as pd
from config import (
    SUBJECTS,
    BRANCHES,
    SEMESTERS,
    PASS_MARK_PER_SUBJECT,
    GRADE_RULES,
    DEFAULT_CSV_PATH,
    TEAM_MEMBERS
)

FIRST_NAMES_MALE = [
    'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna',
    'Ishaan', 'Shaurya', 'Atharv', 'Advik', 'Pranav', 'Advaith', 'Kabir', 'Rohan', 'Dhruv',
    'Kunal', 'Rahul', 'Aniket', 'Sameer', 'Vikram', 'Manish', 'Siddharth', 'Nikhil', 'Dev',
    'Harsh', 'Mohit', 'Varun', 'Tarun', 'Manoj', 'Deepak', 'Suresh', 'Ramesh', 'Karthik',
    'Chaitanya', 'Abhinav', 'Bhuvan', 'Charan', 'Dileep', 'Ganesh', 'Harish', 'Jagadeesh',
    'Kishore', 'Lokesh', 'Madhav', 'Naveen', 'Pavan', 'Rakesh', 'Sanjay', 'Venkatesh'
]

FIRST_NAMES_FEMALE = [
    'Aanya', 'Aadhya', 'Aarohi', 'Ananya', 'Diya', 'Gauri', 'Isha', 'Kavya', 'Khushi',
    'Manya', 'Navya', 'Pari', 'Prisha', 'Riya', 'Saanvi', 'Sara', 'Siya', 'Sneha',
    'Tanvi', 'Vanya', 'Pooja', 'Priya', 'Neha', 'Shreya', 'Anjali', 'Meera', 'Ritu',
    'Divya', 'Payal', 'Simran', 'Bhavana', 'Keerthi', 'Harini', 'Swathi', 'Lavanya',
    'Anupama', 'Chandana', 'Deepika', 'Geethika', 'Hema', 'Indira', 'Jahnavi', 'Kusuma',
    'Lakshmi', 'Manasa', 'Nandini', 'Pranathi', 'Radhika', 'Sindhu', 'Tejaswini', 'Yamini'
]

LAST_NAMES = [
    'Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Patel', 'Reddy', 'Mehta', 'Nair',
    'Iyer', 'Joshi', 'Chopra', 'Malhotra', 'Bhatia', 'Saxena', 'Deshmukh', 'Kulkarni',
    'Rao', 'Choudhary', 'Das', 'Sen', 'Ghosh', 'Chatterjee', 'Banerjee', 'Bose',
    'Mishra', 'Pandey', 'Yadav', 'Agarwal', 'Jain', 'Kalyanam', 'Tadicherla', 'Kovvuri',
    'Shaik', 'Nallamilli', 'Gollapudi', 'Marella', 'Peddireddy', 'Gudipati', 'Chintalapati',
    'Bandaru', 'Velagapudi', 'Yarlagadda', 'Kanumuri', 'Dandu', 'Datla', 'Sagi', 'Penmatsa'
]


def determine_grade_and_status(percentage, subject_marks):
    has_failed_subject = any(m < PASS_MARK_PER_SUBJECT for m in subject_marks)
    if has_failed_subject or percentage < 50.0:
        return 'F', 0.0, 'Fail'

    for min_pct, grade_letter, grade_pt, _ in GRADE_RULES:
        if percentage >= min_pct:
            return grade_letter, grade_pt, 'Pass'

    return 'F', 0.0, 'Fail'


def generate_sample_dataset(n_students=500, seed=42, save_to_csv=True, filepath=None):
    np.random.seed(seed)
    if filepath is None:
        filepath = DEFAULT_CSV_PATH

    records = []

    # 1. Add the 4 Official Team Members with High Honor Standing
    team_data = [
        {'name': 'KALYANAM MUKUNDHA', 'roll_no': '25B11CS380', 'gender': 'Male', 'att': 94.5, 'base': 92.0, 'sem': 'Semester 4'},
        {'name': 'TADICHERLA SAI ABHIRAM', 'roll_no': '25B11CS932', 'gender': 'Male', 'att': 96.0, 'base': 95.0, 'sem': 'Semester 4'},
        {'name': 'KOVVURI SAMEER REDDY', 'roll_no': '25B11CS490', 'gender': 'Male', 'att': 91.5, 'base': 90.0, 'sem': 'Semester 4'},
        {'name': 'SHAIK SAJID', 'roll_no': '25B11CS891', 'gender': 'Male', 'att': 93.0, 'base': 91.5, 'sem': 'Semester 4'}
    ]

    for member in team_data:
        sub_marks = []
        for _ in SUBJECTS:
            score = float(np.clip(member['base'] + np.random.normal(0, 2.5), 82.0, 99.0))
            sub_marks.append(round(score, 1))

        total_marks = round(float(np.sum(sub_marks)), 1)
        percentage = round(total_marks / len(SUBJECTS), 2)
        grade, grade_pt, status = determine_grade_and_status(percentage, sub_marks)

        row = {
            'Student_ID': member['roll_no'],
            'Name': member['name'],
            'Gender': member['gender'],
            'Branch': 'Computer Science & Engineering',
            'Semester': member['sem'],
            'Attendance': member['att']
        }
        for sub, mark in zip(SUBJECTS, sub_marks):
            row[sub] = mark

        row['Total_Marks'] = total_marks
        row['Percentage'] = percentage
        row['Grade'] = grade
        row['Grade_Point'] = grade_pt
        row['Status'] = status
        records.append(row)

    # 2. Generate Remaining Students up to exactly n_students
    remaining = n_students - len(records)
    n_male = remaining // 2
    n_female = remaining - n_male

    male_names = [f"{np.random.choice(FIRST_NAMES_MALE)} {np.random.choice(LAST_NAMES)}" for _ in range(n_male)]
    female_names = [f"{np.random.choice(FIRST_NAMES_FEMALE)} {np.random.choice(LAST_NAMES)}" for _ in range(n_female)]

    names = male_names + female_names
    genders = ['Male'] * n_male + ['Female'] * n_female

    idx = np.random.permutation(remaining)
    names = [names[i] for i in idx]
    genders = [genders[i] for i in idx]

    branch_codes = {
        'Computer Science & Engineering': 'CS',
        'Electronics & Communication': 'EC',
        'Electrical & Electronics': 'EE',
        'Mechanical Engineering': 'ME',
        'Civil Engineering': 'CE',
        'Information Technology': 'IT'
    }

    subject_means = {
        'Mathematics': 70.0,
        'Physics': 68.0,
        'Python_Programming': 76.0,
        'Data_Structures': 72.0,
        'English': 78.0
    }

    # Use branch counter to guarantee 100% unique student IDs
    branch_counters = {b: 101 for b in BRANCHES}

    for i in range(remaining):
        branch = str(np.random.choice(BRANCHES))
        b_code = branch_codes.get(branch, 'CS')
        sem = str(np.random.choice(SEMESTERS))
        
        counter = branch_counters[branch]
        branch_counters[branch] += 1
        student_id = f"25B11{b_code}{counter:04d}"

        # Realistic attendance distribution (around 80.5%, ~12% have < 75%)
        att = float(np.clip(np.random.normal(80.5, 12.0), 40.0, 99.5))
        attendance = round(att, 1)

        # Baseline ability linked with attendance and realistic variance
        ability_factor = ((attendance - 65.0) / 35.0) * 0.40 + np.random.normal(0.85, 0.22)

        sub_marks = []
        for sub in SUBJECTS:
            b_mean = subject_means.get(sub, 72.0)
            score = float(np.clip(b_mean * ability_factor + np.random.normal(0, 8.0), 15.0, 99.5))
            sub_marks.append(round(score, 1))

        total_marks = round(float(np.sum(sub_marks)), 1)
        percentage = round(total_marks / len(SUBJECTS), 2)
        grade, grade_pt, status = determine_grade_and_status(percentage, sub_marks)

        row = {
            'Student_ID': student_id,
            'Name': names[i],
            'Gender': genders[i],
            'Branch': branch,
            'Semester': sem,
            'Attendance': attendance
        }
        for sub, mark in zip(SUBJECTS, sub_marks):
            row[sub] = mark

        row['Total_Marks'] = total_marks
        row['Percentage'] = percentage
        row['Grade'] = grade
        row['Grade_Point'] = grade_pt
        row['Status'] = status
        records.append(row)

    df = pd.DataFrame(records)

    if save_to_csv:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"[+] Successfully generated exactly {len(df)} unique student records saved to: {filepath}")

    return df


if __name__ == '__main__':
    generate_sample_dataset(500)

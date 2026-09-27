# ==============================================================================
# Data Manager Module - Aditya University Student Performance Analytics
# Handles CSV persistence, data validation, cleaning, and CRUD operations.
# ==============================================================================
import os
import pandas as pd
from config import (
    SUBJECTS,
    BRANCHES,
    SEMESTERS,
    DEFAULT_CSV_PATH,
    PASS_MARK_PER_SUBJECT,
    GRADE_RULES
)
from sample_data import generate_sample_dataset, determine_grade_and_status


def load_data(filepath=None):
    if filepath is None:
        filepath = DEFAULT_CSV_PATH

    if not os.path.exists(filepath):
        print('[!] Dataset not found at ' + str(filepath) + '. Generating new sample dataset...')
        return generate_sample_dataset(filepath=filepath)

    try:
        df = pd.read_csv(filepath)
        # Handle missing values & type conversion
        num_cols = ['Attendance', 'Total_Marks', 'Percentage', 'Grade_Point'] + SUBJECTS
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Fill any NaN marks with 0.0, and attendance with mean
        for sub in SUBJECTS:
            if sub in df.columns:
                df[sub] = df[sub].fillna(0.0)

        if 'Attendance' in df.columns:
            df['Attendance'] = df['Attendance'].fillna(df['Attendance'].mean().round(1))

        # Drop duplicate student IDs if any
        if 'Student_ID' in df.columns:
            df = df.drop_duplicates(subset=['Student_ID'], keep='first').reset_index(drop=True)

        return df
    except Exception as e:
        print('[!] Error loading data: ' + str(e))
        return generate_sample_dataset(filepath=filepath)


def save_data(df, filepath=None):
    if filepath is None:
        filepath = DEFAULT_CSV_PATH
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    return True


def calculate_metrics_for_marks(subject_marks_dict):
    marks = [float(subject_marks_dict.get(sub, 0.0)) for sub in SUBJECTS]
    total_marks = round(sum(marks), 1)
    percentage = round(total_marks / len(SUBJECTS), 2)
    grade, grade_pt, status = determine_grade_and_status(percentage, marks)
    return {
        'Total_Marks': total_marks,
        'Percentage': percentage,
        'Grade': grade,
        'Grade_Point': grade_pt,
        'Status': status
    }


def add_student(df, student_dict):
    student_id = str(student_dict.get('Student_ID', '')).strip().upper()
    if not student_id:
        return df, False, 'Student ID cannot be empty.'

    if not df.empty and (df['Student_ID'].astype(str).str.strip().str.upper() == student_id).any():
        return df, False, 'Student with ID ' + student_id + ' already exists.'

    name = str(student_dict.get('Name', '')).strip()
    if not name:
        return df, False, 'Student Name cannot be empty.'

    branch = student_dict.get('Branch', BRANCHES[0])
    if branch not in BRANCHES:
        branch = BRANCHES[0]

    semester = student_dict.get('Semester', SEMESTERS[0])
    gender = student_dict.get('Gender', 'Male')
    if gender not in ['Male', 'Female', 'Other']:
        gender = 'Male'

    try:
        attendance = float(student_dict.get('Attendance', 80.0))
        if not (0.0 <= attendance <= 100.0):
            return df, False, 'Attendance must be between 0 and 100.'
    except ValueError:
        return df, False, 'Invalid attendance value.'

    subject_marks = {}
    for sub in SUBJECTS:
        try:
            val = float(student_dict.get(sub, 0.0))
            if not (0.0 <= val <= 100.0):
                return df, False, 'Marks for ' + sub + ' must be between 0 and 100.'
            subject_marks[sub] = round(val, 1)
        except ValueError:
            return df, False, 'Invalid mark for ' + sub

    metrics = calculate_metrics_for_marks(subject_marks)

    new_row = {
        'Student_ID': student_id,
        'Name': name,
        'Gender': gender,
        'Branch': branch,
        'Semester': semester,
        'Attendance': round(attendance, 1),
        **subject_marks,
        **metrics
    }

    new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(new_df)
    return new_df, True, 'Student ' + name + ' (' + student_id + ') added successfully!'


def update_student(df, student_id, update_dict):
    clean_id = str(student_id).strip().upper()
    mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_id
    if not mask.any():
        return df, False, 'No student found with ID: ' + student_id

    idx = df[mask].index[0]

    if 'Name' in update_dict and str(update_dict['Name']).strip():
        df.at[idx, 'Name'] = str(update_dict['Name']).strip()
    if 'Gender' in update_dict and update_dict['Gender'] in ['Male', 'Female', 'Other']:
        df.at[idx, 'Gender'] = update_dict['Gender']
    if 'Branch' in update_dict and update_dict['Branch'] in BRANCHES:
        df.at[idx, 'Branch'] = update_dict['Branch']
    if 'Semester' in update_dict and update_dict['Semester'] in SEMESTERS:
        df.at[idx, 'Semester'] = update_dict['Semester']
    if 'Attendance' in update_dict:
        try:
            att = float(update_dict['Attendance'])
            if 0.0 <= att <= 100.0:
                df.at[idx, 'Attendance'] = round(att, 1)
        except ValueError:
            pass

    subject_marks = {}
    for sub in SUBJECTS:
        if sub in update_dict:
            try:
                m = float(update_dict[sub])
                if 0.0 <= m <= 100.0:
                    df.at[idx, sub] = round(m, 1)
            except ValueError:
                pass
        subject_marks[sub] = df.at[idx, sub]

    metrics = calculate_metrics_for_marks(subject_marks)
    for k, v in metrics.items():
        df.at[idx, k] = v

    save_data(df)
    s_name = str(df.at[idx, 'Name'])
    return df, True, 'Record for ' + s_name + ' (' + student_id + ') updated successfully!'


def delete_student(df, student_id):
    clean_id = str(student_id).strip().upper()
    mask = df['Student_ID'].astype(str).str.strip().str.upper() == clean_id
    if not mask.any():
        return df, False, 'Student with ID ' + student_id + ' not found.'

    student_name = df.loc[mask, 'Name'].values[0]
    updated_df = df[~mask].reset_index(drop=True)
    save_data(updated_df)
    return updated_df, True, 'Student ' + student_name + ' (' + student_id + ') deleted successfully.'


def search_and_filter(df, query=None, branch=None, semester=None, grade=None, status=None, min_att=None, max_att=None, min_attendance=None, max_attendance=None, **kwargs):
    if df.empty:
        return df

    filtered = df.copy()

    if query:
        q = str(query).strip().lower()
        mask = (
            filtered['Student_ID'].astype(str).str.lower().str.contains(q, na=False) |
            filtered['Name'].astype(str).str.lower().str.contains(q, na=False)
        )
        filtered = filtered[mask]

    if branch and branch != 'All':
        filtered = filtered[filtered['Branch'] == branch]
    if semester and semester != 'All':
        filtered = filtered[filtered['Semester'] == semester]
    if grade and grade != 'All':
        filtered = filtered[filtered['Grade'] == grade]
    if status and status != 'All':
        filtered = filtered[filtered['Status'] == status]

    actual_min_att = min_att if min_att is not None else min_attendance
    actual_max_att = max_att if max_att is not None else max_attendance

    if actual_min_att is not None:
        filtered = filtered[filtered['Attendance'] >= float(actual_min_att)]
    if actual_max_att is not None:
        filtered = filtered[filtered['Attendance'] <= float(actual_max_att)]

    return filtered.reset_index(drop=True)


def get_top_performers(df, top_n=10, branch=None):
    if df.empty:
        return df
    data = df if branch is None or branch == 'All' else df[df['Branch'] == branch]
    return data.sort_values('Percentage', ascending=False).head(top_n).reset_index(drop=True)


def get_low_attendance_students(df, threshold=75.0):
    if df.empty:
        return df
    return df[df['Attendance'] < threshold].sort_values('Attendance').reset_index(drop=True)


def get_failed_students(df):
    if df.empty:
        return df
    return df[df['Status'] == 'Fail'].sort_values('Percentage').reset_index(drop=True)

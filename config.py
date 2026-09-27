# ==============================================================================
# Configuration Module for Student Performance Analytics System
# Department of Computer Science & Engineering  Aditya University
# ==============================================================================
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
DEFAULT_CSV_PATH = os.path.join(DATA_DIR, 'students_data.csv')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Project Information
INSTITUTION = 'Aditya University'
DEPARTMENT = 'Department of Computer Science & Engineering'
PROJECT_TITLE = 'Student Performance Analytics System'
PROJECT_SUBTITLE = 'Data-Driven Analysis of Student Academic Performance'

TEAM_MEMBERS = [
    {'name': 'KALYANAM MUKUNDHA', 'roll_no': '25B11CS380', 'role': 'Team Lead & Backend Developer'},
    {'name': 'TADICHERLA SAI ABHIRAM', 'roll_no': '25B11CS932', 'role': 'Data Analyst & NumPy Specialist'},
    {'name': 'KOVVURI SAMEER REDDY', 'roll_no': '25B11CS490', 'role': 'Data Engineer & Pandas Specialist'},
    {'name': 'SHAIK SAJID', 'roll_no': '25B11CS891', 'role': 'Frontend & Visualization Specialist'}
]

# Academic Subjects
SUBJECTS = [
    'Mathematics',
    'Physics',
    'Python_Programming',
    'Data_Structures',
    'English'
]

# Academic Constants
MAX_MARKS_PER_SUBJECT = 100.0
PASS_MARK_PER_SUBJECT = 40.0
TOTAL_MAX_MARKS = len(SUBJECTS) * MAX_MARKS_PER_SUBJECT  # 500.0
MIN_ATTENDANCE_REQUIRED = 75.0  # in percentage

# Branches / Departments
BRANCHES = [
    'Computer Science & Engineering',
    'Electronics & Communication',
    'Electrical & Electronics',
    'Mechanical Engineering',
    'Civil Engineering',
    'Information Technology'
]

# Semesters
SEMESTERS = [
    'Semester 1', 'Semester 2', 'Semester 3', 'Semester 4',
    'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8'
]

# Grade Classification System (From Project Presentation Slide 7)
# (Min_Percentage, Grade_Letter, Grade_Point, Description)
GRADE_RULES = [
    (90.0, 'A+', 10.0, 'Outstanding'),
    (80.0, 'A', 9.0, 'Excellent'),
    (70.0, 'B', 8.0, 'Good'),
    (60.0, 'C', 7.0, 'Average'),
    (50.0, 'D', 6.0, 'Below Average'),
    (0.0, 'F', 0.0, 'Fail')
]

# Colors for UI & Matplotlib
GRADE_COLORS = {
    'A+': '#10b981',  # Emerald Green
    'A': '#3b82f6',   # Blue
    'B': '#6366f1',   # Indigo
    'C': '#f59e0b',   # Amber
    'D': '#ec4899',   # Pink
    'F': '#ef4444'    # Red
}

PLOT_COLORS = {
    'primary': '#1e3a8a',
    'secondary': '#3b82f6',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'dark': '#0f172a'
}

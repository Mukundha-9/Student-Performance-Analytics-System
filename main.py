# ==============================================================================
# Main Interactive CLI Application
# Student Performance Analytics System - Aditya University
# ==============================================================================
import os
import sys
import pandas as pd
from config import (
    INSTITUTION,
    DEPARTMENT,
    PROJECT_TITLE,
    TEAM_MEMBERS,
    SUBJECTS,
    BRANCHES,
    DEFAULT_CSV_PATH
)
import data_manager
import analytics
import visualizer
import generate_report


def print_banner():
    print("\n" + "="*80)
    print(f"  {INSTITUTION.upper()} - {DEPARTMENT.upper()}")
    print(f"  {PROJECT_TITLE.upper()}")
    print("  Powered by Python 3.x, NumPy, Pandas, Matplotlib & Modern Web Frontend")
    print("="*80)


def print_team():
    print("\n[+] PROJECT TEAM MEMBERS:")
    for m in TEAM_MEMBERS:
        print(f"  - {m['name']} ({m['roll_no']}) -> {m['role']}")
    print("-" * 80)


def view_all_students(df):
    print("\n--- ALL REGISTERED STUDENTS ---")
    if df.empty:
        print("No student records found.")
        return

    cols = ['Student_ID', 'Name', 'Branch', 'Attendance', 'Total_Marks', 'Percentage', 'Grade', 'Status']
    avail = [c for c in cols if c in df.columns]
    print(df[avail].to_string(index=False))
    print(f"\nTotal Records: {len(df)}")


def show_statistics(df):
    print("\n" + "="*80)
    print("  NUMPY STATISTICAL SUMMARY & COHORT BENCHMARKS")
    print("="*80)
    stats = analytics.compute_overall_statistics(df)
    corr = analytics.compute_attendance_correlation(df)

    print(f"Total Cohort Size    : {stats.get('total_students', 0)} Students")
    print(f"Passed Students      : {stats.get('pass_count', 0)} ({stats.get('pass_percentage', 0.0)}%)")
    print(f"Failed Students      : {stats.get('fail_count', 0)} ({round(100 - stats.get('pass_percentage', 0.0), 2)}%)")
    print(f"Class Average (mu)   : {stats.get('mean_percentage', 0.0)}%")
    print(f"Median Score (Q2)    : {stats.get('median_percentage', 0.0)}%")
    print(f"Std Deviation (sigma): {stats.get('std_percentage', 0.0)}%")
    print(f"Variance (sigma^2)   : {stats.get('var_percentage', 0.0)}")
    print(f"Quartiles (Q1, Q3)   : Q1={stats.get('q1', 0.0)}%, Q3={stats.get('q3', 0.0)}% (IQR={stats.get('iqr_percentage', 0.0)}%)")
    print(f"Average Attendance   : {stats.get('mean_attendance', 0.0)}%")
    print(f"Pearson Corr (r)     : {corr.get('r', 0.0)} ({corr.get('interpretation', 'N/A')})")
    print(f"Regression Model     : {corr.get('equation', 'N/A')}")

    topper = stats.get('topper', {})
    print(f"\nCLASS TOPPER: {topper.get('name', 'N/A')} ({topper.get('student_id', 'N/A')}) - {topper.get('percentage', 0.0)}% [{topper.get('grade', 'N/A')}]")


def main_menu():
    df = data_manager.load_data()
    print_banner()
    print_team()

    while True:
        print("\n" + "-"*50)
        print("                 MAIN MENU")
        print("-" * 50)
        print("[1]  View All Student Records")
        print("[2]  Add New Student Record")
        print("[3]  Update Student Information / Marks")
        print("[4]  Delete Student Record")
        print("[5]  Search & Filter Records")
        print("[6]  NumPy Statistical Summary & Benchmarks")
        print("[7]  Subject-Wise Performance Analysis")
        print("[8]  Branch-Wise Performance Breakdown")
        print("[9]  Individual Student Report Card Lookup")
        print("[10] At-Risk & Attendance Warning Alerts (< 75%)")
        print("[11] Generate & Save All Matplotlib Charts")
        print("[12] Generate Full Academic Performance Report")
        print("[13] Launch Modern Web Dashboard (HTML/CSS/JS)")
        print("[14] Reset / Regenerate Sample Dataset")
        print("[0]  Exit Application")
        print("-" * 50)

        choice = input("Select an option (0-14): ").strip()

        if choice == '1':
            df = data_manager.load_data()
            view_all_students(df)
        elif choice == '2':
            print("\n--- ADD NEW STUDENT ---")
            s_id = input("Student ID (e.g. 25B11CS999): ").strip()
            name = input("Student Name: ").strip()
            branch = input(f"Branch ({', '.join(BRANCHES)}): ").strip()
            gender = input("Gender (Male/Female): ").strip() or "Male"
            att = float(input("Attendance % (0-100): ").strip() or 80.0)

            sub_marks = {}
            for sub in SUBJECTS:
                sub_marks[sub] = float(input(f"Marks in {sub} (0-100): ").strip() or 75.0)

            df, ok, msg = data_manager.add_student(df, {
                'Student_ID': s_id, 'Name': name, 'Branch': branch,
                'Gender': gender, 'Attendance': att, **sub_marks
            })
            print(f"\n[Result] {msg}")
        elif choice == '3':
            s_id = input("\nEnter Student ID to Update: ").strip()
            att = input("New Attendance (press Enter to skip): ").strip()
            update_data = {}
            if att: update_data['Attendance'] = float(att)
            for sub in SUBJECTS:
                m = input(f"New Marks for {sub} (press Enter to skip): ").strip()
                if m: update_data[sub] = float(m)
            df, ok, msg = data_manager.update_student(df, s_id, update_data)
            print(f"\n[Result] {msg}")
        elif choice == '4':
            s_id = input("\nEnter Student ID to Delete: ").strip()
            df, ok, msg = data_manager.delete_student(df, s_id)
            print(f"\n[Result] {msg}")
        elif choice == '5':
            q = input("\nEnter search keyword (Name or ID): ").strip()
            results = data_manager.search_and_filter(df, query=q)
            view_all_students(results)
        elif choice == '6':
            show_statistics(df)
        elif choice == '7':
            sub_stats = analytics.compute_subject_statistics(df)
            print("\n--- SUBJECT-WISE PERFORMANCE ANALYSIS ---")
            for sub, sdata in sub_stats.items():
                print(f"\n* {sub.replace('_', ' ')}:")
                print(f"  Mean: {sdata['mean']} | Std: {sdata['std']} | Min: {sdata['min']} | Max: {sdata['max']}")
                print(f"  Pass Rate: {sdata['pass_rate']}% | Passed: {sdata['passed_count']} | Failed: {sdata['failed_count']}")
                print(f"  Topper: {sdata['topper_name']} ({sdata['topper_score']})")
        elif choice == '8':
            b_stats = analytics.compute_branch_analytics(df)
            print("\n--- BRANCH-WISE BREAKDOWN ---")
            for b, bdata in b_stats.items():
                print(f"\n* {b}: {bdata['student_count']} Students | Mean: {bdata['mean_percentage']}% | Pass Rate: {bdata['pass_rate']}%")
        elif choice == '9':
            s_id = input("\nEnter Student ID for Report Card: ").strip()
            card = analytics.get_student_rank_card(df, s_id)
            if not card:
                print(f"[!] Student ID '{s_id}' not found.")
            else:
                print("\n" + "="*60)
                print(f"  ADITYA UNIVERSITY - OFFICIAL STUDENT GRADE SHEET")
                print("="*60)
                print(f"Name      : {card['name']} ({card['student_id']})")
                print(f"Branch    : {card['branch']} | Attendance: {card['attendance']}%")
                print(f"Class Rank: #{card['class_rank']} of {card['total_students']} (Percentile: {card['percentile']}%)")
                print(f"Total     : {card['total_marks']}/500 ({card['percentage']}%) -> Grade: {card['grade']} ({card['status']})")
                print("\nSUBJECT BREAKDOWN:")
                for sub, c in card['subject_comparisons'].items():
                    print(f"  - {sub:20s}: {c['score']:5.1f} / 100 | Class Avg: {c['class_mean']:5.1f} | Z-Score: {c['z_score']:5.2f} [{c['status']}]")
        elif choice == '10':
            at_risk = analytics.identify_at_risk_students(df)
            print(f"\n--- AT-RISK & ATTENDANCE WARNING ALERTS ({len(at_risk)} Flagged) ---")
            for s in at_risk:
                print(f"  - [{s['Student_ID']}] {s['Name']:22s} | Score: {s['Percentage']:5.1f}% | Att: {s['Attendance']:4.1f}% | Reasons: {s['Risk_Reasons']}")
        elif choice == '11':
            print("\n[+] Generating all 7 publication-quality Matplotlib figures...")
            files = visualizer.save_all_visualizations(df)
            print(f"[+] Saved {len(files)} charts to 'reports/' folder.")
        elif choice == '12':
            report_path = generate_report.generate_academic_report(df)
            print(f"\n[+] Academic Performance Report generated: {report_path}")
        elif choice == '13':
            print("\n[+] Starting Flask Web Application at http://127.0.0.1:5000 ...")
            print("[+] Press Ctrl+C to stop the web server and return to CLI.")
            os.system(f"{sys.executable} app.py")
        elif choice == '14':
            df = data_manager.generate_sample_dataset(100)
            visualizer.save_all_visualizations(df)
            print("\n[+] Dataset regenerated successfully!")
        elif choice == '0':
            print("\nThank you for using Aditya University Student Performance Analytics System. Goodbye!\n")
            break
        else:
            print("[!] Invalid choice. Please try again.")


if __name__ == '__main__':
    main_menu()

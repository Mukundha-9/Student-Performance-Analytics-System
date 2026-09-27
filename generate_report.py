# ==============================================================================
# Performance Report Generator Module - Aditya University
# Generates academic markdown and text performance reports.
# ==============================================================================
import os
import datetime
import pandas as pd
from config import REPORTS_DIR, SUBJECTS, DEFAULT_CSV_PATH, INSTITUTION, DEPARTMENT, PROJECT_TITLE, TEAM_MEMBERS
import data_manager
import analytics
import visualizer


def generate_academic_report(df=None, output_dir=None):
    if df is None:
        df = data_manager.load_data()
    if output_dir is None:
        output_dir = REPORTS_DIR

    os.makedirs(output_dir, exist_ok=True)
    overall = analytics.compute_overall_statistics(df)
    sub_stats = analytics.compute_subject_statistics(df)
    corr = analytics.compute_attendance_correlation(df)
    grades = analytics.compute_grade_distribution(df)
    branch_stats = analytics.compute_branch_analytics(df)
    toppers = data_manager.get_top_performers(df, top_n=10)
    at_risk = analytics.identify_at_risk_students(df)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    md = []
    md.append(f'# {INSTITUTION.upper()}')
    md.append(f'## {DEPARTMENT}')
    md.append(f'### {PROJECT_TITLE}')
    md.append(f'**Generated on:** {timestamp} | **Course:** Data Analysis Essentials (DAE)')
    md.append('')
    md.append('**Project Team Members:**')
    for m in TEAM_MEMBERS:
        md.append(f"- {m['name']} ({m['roll_no']}) - *{m['role']}*")
    md.append('')
    md.append('---')
    md.append('## 1. Executive Summary & Key Performance Indicators')
    md.append('')
    md.append('| Key Performance Metric | Statistical Value | Description / Benchmark |')
    md.append('| :--- | :--- | :--- |')
    md.append(f"| **Total Cohort Size** | {overall.get('total_students', 0)} Students | Active student records in database |")
    md.append(f"| **Passed Students** | {overall.get('pass_count', 0)} ({overall.get('pass_percentage', 0.0)}%) | Overall Percentage >= 50% and all subjects >= 40 |")
    md.append(f"| **Failed Students** | {overall.get('fail_count', 0)} ({round(100 - overall.get('pass_percentage', 0.0), 2)}%) | Students requiring academic intervention |")
    md.append(f"| **Class Average ($\\\\mu$)** | {overall.get('mean_percentage', 0.0)}% | Primary benchmark for cohort performance |")
    md.append(f"| **Median Score ($Q_2$)** | {overall.get('median_percentage', 0.0)}% | Middle value in marks distribution (outlier robust) |")
    md.append(f"| **Standard Deviation ($\\\\sigma$)** | {overall.get('std_percentage', 0.0)}% | Measure of performance variability |")
    md.append(f"| **Variance ($\\\\sigma^2$)** | {overall.get('var_percentage', 0.0)} | Spread of marks around the mean |")
    md.append(f"| **Quartile Analysis** | Q1: {overall.get('q1', 0.0)}%, Q3: {overall.get('q3', 0.0)}% | IQR: {overall.get('iqr_percentage', 0.0)}% |")
    md.append(f"| **90th / 95th Percentile** | P90: {overall.get('p90', 0.0)}%, P95: {overall.get('p95', 0.0)}% | Top academic performance tier |")
    md.append(f"| **Average Attendance** | {overall.get('mean_attendance', 0.0)}% | Cohort regularity rate |")
    topper = overall.get('topper', {})
    md.append(f"| **Class Topper** | **{topper.get('name', 'N/A')}** ({topper.get('student_id', 'N/A')}) | **{topper.get('percentage', 0.0)}%** ({topper.get('grade', 'N/A')}) - {topper.get('branch', 'N/A')} |")
    md.append('')
    md.append('---')
    md.append('## 2. Attendance & Performance Correlation Analysis')
    md.append(f"- **Pearson Correlation Coefficient ($r$):** `{corr.get('r', 0.0)}` ({corr.get('interpretation', 'N/A')})")
    md.append(f"- **Coefficient of Determination ($R^2$):** `{corr.get('r_squared', 0.0)}` (Explains {round(corr.get('r_squared', 0.0)*100, 1)}% of total academic variance)")
    md.append(f"- **Fitted Linear Regression Model:** `{corr.get('equation', 'N/A')}`")
    md.append('')
    md.append('---')
    md.append('## 3. Subject-Wise Performance Breakdown')
    md.append('')
    md.append('| Subject | Mean Mark ($\\\\mu$) | Std Dev ($\\\\sigma$) | Min | Max | Pass Rate (%) | Subject Topper |')
    md.append('| :--- | :--- | :--- | :--- | :--- | :--- | :--- |')
    for sub, data in sub_stats.items():
        s_clean = sub.replace('_', ' ')
        md.append(f"| {s_clean} | {data['mean']} | {data['std']} | {data['min']} | {data['max']} | {data['pass_rate']}% | {data['topper_name']} ({data['topper_score']}) |")
    md.append('')
    md.append('---')
    md.append('## 4. Academic Grade Classification (Aditya University Standard)')
    md.append('')
    md.append('| Grade | Count | Percentage | Classification |')
    md.append('| :--- | :--- | :--- | :--- |')
    for g, gdata in grades.items():
        md.append(f"| **{g}** | {gdata['count']} | {gdata['percentage']}% | {gdata['description']} |")
    md.append('')
    md.append('---')
    md.append('## 5. Branch / Department Comparison')
    md.append('')
    md.append('| Branch | Students | Mean Score | Avg Attendance | Pass Rate | Branch Topper |')
    md.append('| :--- | :--- | :--- | :--- | :--- | :--- |')
    for b, bdata in branch_stats.items():
        md.append(f"| {b} | {bdata['student_count']} | {bdata['mean_percentage']}% | {bdata['avg_attendance']}% | {bdata['pass_rate']}% | {bdata['topper_name']} ({bdata['highest_score']}%) |")
    md.append('')
    md.append('---')
    md.append('## 6. Top 10 Ranking Students (Honor Roll)')
    md.append('')
    md.append('| Rank | Student ID | Name | Branch | Attendance | Total Marks | Percentage | Grade |')
    md.append('| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |')
    for idx, row in toppers.iterrows():
        s_id = row.get('Student_ID', row.get('Roll_No', 'N/A'))
        b_name = row.get('Branch', row.get('Department', 'N/A'))
        md.append(f"| #{idx + 1} | {s_id} | {row['Name']} | {b_name} | {row['Attendance']}% | {row['Total_Marks']} | {row['Percentage']}% | {row['Grade']} |")
    md.append('')
    md.append('---')
    md.append(f"## 7. Students Requiring Academic Intervention ({len(at_risk)} Flagged)")
    md.append('')
    if at_risk:
        md.append('| Student ID | Name | Branch | Attendance | Percentage | Flagged Reasons |')
        md.append('| :--- | :--- | :--- | :--- | :--- | :--- |')
        for s in at_risk:
            md.append(f"| {s['Student_ID']} | {s['Name']} | {s['Branch']} | {s['Attendance']}% | {s['Percentage']}% | {s['Risk_Reasons']} |")
    else:
        md.append('*No students currently flagged for academic intervention.*')
    md.append('')
    md.append('---')
    md.append('## 8. Exported Visualization Gallery')
    md.append('- `01_subject_averages.png` - Subject-Wise Performance (Min, Mean, Max Bar Chart)')
    md.append('- `02_grade_distribution.png` - Academic Grade Distribution Donut Chart')
    md.append('- `03_score_distribution.png` - Class Marks Distribution & Gaussian Normal Fit Histogram')
    md.append('- `04_attendance_correlation.png` - Attendance vs Academic Performance Scatter & Regression')
    md.append('- `05_performance_trends.png` - Academic Performance Progression & Percentile Bands')
    md.append('- `06_department_comparison.png` - Branch-Wise Performance Box Plot')
    md.append('- `07_comprehensive_dashboard.png` - 4-in-1 Executive Performance Analytics Dashboard')

    md_report_path = os.path.join(output_dir, 'academic_performance_report.md')
    with open(md_report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    visualizer.save_all_visualizations(df, output_dir=output_dir)
    print(f'[+] Academic Report generated: {md_report_path}')
    return md_report_path


if __name__ == '__main__':
    generate_academic_report()

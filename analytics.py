# ==============================================================================
# Analytics Engine Module - Aditya University Student Performance Analytics
# Performs mathematical & statistical computations using NumPy + AI Insights.
# ==============================================================================
import numpy as np
import pandas as pd
from config import SUBJECTS, PASS_MARK_PER_SUBJECT, MIN_ATTENDANCE_REQUIRED, GRADE_RULES


def compute_overall_statistics(df):
    if df.empty:
        return {}

    percentages = df['Percentage'].to_numpy(dtype=float)
    totals = df['Total_Marks'].to_numpy(dtype=float)
    attendances = df['Attendance'].to_numpy(dtype=float)
    statuses = df['Status'].to_numpy(dtype=str)

    n_students = len(df)
    pass_mask = statuses == 'Pass'
    pass_count = int(np.sum(pass_mask))
    fail_count = n_students - pass_count
    pass_rate = round(float((pass_count / n_students) * 100.0), 2)

    pct_25, pct_50, pct_75, pct_90, pct_95 = np.percentile(percentages, [25, 50, 75, 90, 95])
    iqr = round(float(pct_75 - pct_25), 2)

    topper_idx = int(np.argmax(percentages))
    topper_row = df.iloc[topper_idx]

    lowest_idx = int(np.argmin(percentages))
    lowest_row = df.iloc[lowest_idx]

    stats = {
        'total_students': n_students,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'pass_percentage': pass_rate,
        'mean_percentage': round(float(np.mean(percentages)), 2),
        'median_percentage': round(float(np.median(percentages)), 2),
        'std_percentage': round(float(np.std(percentages)), 2),
        'var_percentage': round(float(np.var(percentages)), 2),
        'min_percentage': round(float(np.min(percentages)), 2),
        'max_percentage': round(float(np.max(percentages)), 2),
        'range_percentage': round(float(np.ptp(percentages)), 2),
        'q1': round(float(pct_25), 2),
        'q2': round(float(pct_50), 2),
        'q3': round(float(pct_75), 2),
        'p90': round(float(pct_90), 2),
        'p95': round(float(pct_95), 2),
        'iqr_percentage': iqr,
        'mean_total': round(float(np.mean(totals)), 2),
        'mean_attendance': round(float(np.mean(attendances)), 2),
        'min_attendance': round(float(np.min(attendances)), 2),
        'max_attendance': round(float(np.max(attendances)), 2),
        'topper': {
            'student_id': str(topper_row.get('Student_ID', topper_row.get('Roll_No', 'N/A'))),
            'name': str(topper_row['Name']),
            'branch': str(topper_row.get('Branch', topper_row.get('Department', 'N/A'))),
            'total_marks': float(topper_row['Total_Marks']),
            'percentage': float(topper_row['Percentage']),
            'grade': str(topper_row['Grade'])
        },
        'lowest_performer': {
            'student_id': str(lowest_row.get('Student_ID', lowest_row.get('Roll_No', 'N/A'))),
            'name': str(lowest_row['Name']),
            'branch': str(lowest_row.get('Branch', lowest_row.get('Department', 'N/A'))),
            'percentage': float(lowest_row['Percentage']),
            'grade': str(lowest_row['Grade'])
        }
    }
    return stats


def compute_subject_statistics(df):
    if df.empty:
        return {}

    subject_stats = {}
    for sub in SUBJECTS:
        if sub not in df.columns:
            continue

        marks = df[sub].to_numpy(dtype=float)
        mean_val = float(np.mean(marks))
        median_val = float(np.median(marks))
        std_val = float(np.std(marks))
        var_val = float(np.var(marks))
        min_val = float(np.min(marks))
        max_val = float(np.max(marks))
        pass_mask = marks >= PASS_MARK_PER_SUBJECT
        pass_rate = float(np.mean(pass_mask) * 100.0)

        max_idx = int(np.argmax(marks))
        top_student = df.iloc[max_idx]

        subject_stats[sub] = {
            'mean': round(mean_val, 2),
            'median': round(median_val, 2),
            'std': round(std_val, 2),
            'variance': round(var_val, 2),
            'min': round(min_val, 1),
            'max': round(max_val, 1),
            'pass_rate': round(pass_rate, 2),
            'passed_count': int(np.sum(pass_mask)),
            'failed_count': int(len(marks) - np.sum(pass_mask)),
            'topper_name': str(top_student['Name']),
            'topper_id': str(top_student.get('Student_ID', top_student.get('Roll_No', 'N/A'))),
            'topper_score': round(max_val, 1)
        }
    return subject_stats


def compute_attendance_correlation(df):
    if df.empty or len(df) < 2:
        return {'r': 0.0, 'slope': 0.0, 'intercept': 0.0, 'equation': 'N/A', 'interpretation': 'N/A'}

    att = df['Attendance'].to_numpy(dtype=float)
    pct = df['Percentage'].to_numpy(dtype=float)

    corr_matrix = np.corrcoef(att, pct)
    r = float(corr_matrix[0, 1])

    poly = np.polyfit(att, pct, deg=1)
    slope = float(poly[0])
    intercept = float(poly[1])

    if abs(r) >= 0.7:
        interp = 'Strong Positive Correlation' if r > 0 else 'Strong Negative Correlation'
    elif abs(r) >= 0.4:
        interp = 'Moderate Positive Correlation' if r > 0 else 'Moderate Negative Correlation'
    else:
        interp = 'Weak / Negligible Correlation'

    eq_sign = '+' if intercept >= 0 else '-'
    eq_str = 'Percentage = ' + str(round(slope, 3)) + ' * Attendance ' + eq_sign + ' ' + str(round(abs(intercept), 2))

    return {
        'r': round(r, 4),
        'r_squared': round(r ** 2, 4),
        'slope': round(slope, 3),
        'intercept': round(intercept, 2),
        'equation': eq_str,
        'interpretation': interp
    }


def compute_grade_distribution(df):
    if df.empty:
        return {}
    grades = df['Grade'].to_numpy(dtype=str)
    n_total = len(grades)
    distribution = {}

    for _, grade_letter, _, desc in GRADE_RULES:
        cnt = int(np.sum(grades == grade_letter))
        pct = round(float((cnt / n_total) * 100.0), 2) if n_total > 0 else 0.0
        distribution[grade_letter] = {
            'count': cnt,
            'percentage': pct,
            'description': desc
        }
    return distribution


def compute_branch_analytics(df):
    col = 'Branch' if 'Branch' in df.columns else 'Department'
    if df.empty or col not in df.columns:
        return {}

    branch_stats = {}
    branches = sorted(df[col].unique())

    for b in branches:
        b_df = df[df[col] == b]
        if b_df.empty:
            continue

        pct_arr = b_df['Percentage'].to_numpy(dtype=float)
        att_arr = b_df['Attendance'].to_numpy(dtype=float)
        status_arr = b_df['Status'].to_numpy(dtype=str)

        b_topper_idx = int(np.argmax(pct_arr))
        b_topper = b_df.iloc[b_topper_idx]

        branch_stats[b] = {
            'student_count': len(b_df),
            'mean_percentage': round(float(np.mean(pct_arr)), 2),
            'median_percentage': round(float(np.median(pct_arr)), 2),
            'std_percentage': round(float(np.std(pct_arr)), 2),
            'avg_attendance': round(float(np.mean(att_arr)), 2),
            'pass_count': int(np.sum(status_arr == 'Pass')),
            'fail_count': int(np.sum(status_arr == 'Fail')),
            'pass_rate': round(float((np.sum(status_arr == 'Pass') / len(b_df)) * 100.0), 2),
            'highest_score': round(float(np.max(pct_arr)), 2),
            'lowest_score': round(float(np.min(pct_arr)), 2),
            'topper_name': str(b_topper['Name']),
            'topper_id': str(b_topper.get('Student_ID', b_topper.get('Roll_No', 'N/A')))
        }
    return branch_stats


def get_student_rank_card(df, student_id):
    clean_id = str(student_id).strip().upper()
    col = 'Student_ID' if 'Student_ID' in df.columns else 'Roll_No'
    mask = df[col].astype(str).str.strip().str.upper() == clean_id
    if not mask.any():
        return None

    student = df[mask].iloc[0]
    percentages = df['Percentage'].to_numpy(dtype=float)
    s_pct = float(student['Percentage'])

    sorted_percentages = np.sort(percentages)[::-1]
    rank = int(np.where(sorted_percentages == s_pct)[0][0]) + 1
    percentile = round(float((np.sum(percentages <= s_pct) / len(percentages)) * 100.0), 2)

    branch_col = 'Branch' if 'Branch' in df.columns else 'Department'
    branch_name = student[branch_col]
    b_df = df[df[branch_col] == branch_name]
    b_pcts = np.sort(b_df['Percentage'].to_numpy(dtype=float))[::-1]
    branch_rank = int(np.where(b_pcts == s_pct)[0][0]) + 1

    sub_comparisons = {}
    for sub in SUBJECTS:
        if sub in df.columns:
            s_mark = float(student[sub])
            all_marks = df[sub].to_numpy(dtype=float)
            sub_mean = float(np.mean(all_marks))
            sub_std = float(np.std(all_marks))
            sub_z = (s_mark - sub_mean) / sub_std if sub_std > 0 else 0.0
            sub_comparisons[sub] = {
                'score': round(s_mark, 1),
                'class_mean': round(sub_mean, 1),
                'difference': round(s_mark - sub_mean, 1),
                'z_score': round(float(sub_z), 2),
                'status': 'Pass' if s_mark >= PASS_MARK_PER_SUBJECT else 'Fail'
            }

    return {
        'student_id': str(student[col]),
        'name': str(student['Name']),
        'gender': str(student.get('Gender', 'N/A')),
        'branch': str(student[branch_col]),
        'semester': str(student.get('Semester', 'N/A')),
        'attendance': float(student['Attendance']),
        'total_marks': float(student['Total_Marks']),
        'percentage': s_pct,
        'grade': str(student['Grade']),
        'grade_point': float(student['Grade_Point']),
        'status': str(student['Status']),
        'class_rank': rank,
        'total_students': len(df),
        'branch_rank': branch_rank,
        'branch_total': len(b_df),
        'percentile': percentile,
        'subject_comparisons': sub_comparisons
    }


def identify_at_risk_students(df):
    if df.empty:
        return []

    id_col = 'Student_ID' if 'Student_ID' in df.columns else 'Roll_No'
    branch_col = 'Branch' if 'Branch' in df.columns else 'Department'
    at_risk = []

    for idx, row in df.iterrows():
        reasons = []
        att = float(row['Attendance'])
        pct = float(row['Percentage'])
        status = str(row['Status'])

        if att < MIN_ATTENDANCE_REQUIRED:
            reasons.append('Low Attendance (' + str(att) + '% < ' + str(MIN_ATTENDANCE_REQUIRED) + '%)')

        if pct < 50.0:
            reasons.append('Below Average Percentage (' + str(pct) + '%)')

        failed_subs = [sub for sub in SUBJECTS if float(row[sub]) < PASS_MARK_PER_SUBJECT]
        if failed_subs:
            clean_subs = [s.replace('_', ' ') for s in failed_subs]
            reasons.append('Failed Subjects: ' + ', '.join(clean_subs))

        if reasons:
            at_risk.append({
                'Student_ID': str(row[id_col]),
                'Name': str(row['Name']),
                'Branch': str(row[branch_col]),
                'Semester': str(row.get('Semester', 'N/A')),
                'Attendance': att,
                'Percentage': pct,
                'Grade': str(row['Grade']),
                'Status': status,
                'Risk_Reasons': ' | '.join(reasons)
            })

    return at_risk


# ==============================================================================
# UNIQUE ADVANCED FEATURES: AI Insights, Simulator & Student Comparison
# ==============================================================================

def generate_ai_student_insights(df, student_id):
    card = get_student_rank_card(df, student_id)
    if not card:
        return None

    insights = {
        'strengths': [],
        'areas_for_improvement': [],
        'learning_trajectory': '',
        'actionable_recommendations': [],
        'attendance_impact_analysis': ''
    }

    sub_comps = card['subject_comparisons']
    scores = {s: comp['score'] for s, comp in sub_comps.items()}
    best_sub = max(scores, key=scores.get)
    worst_sub = min(scores, key=scores.get)

    for sub, comp in sub_comps.items():
        s_name = sub.replace('_', ' ')
        if comp['z_score'] >= 1.0:
            insights['strengths'].append(f"Outstanding mastery in {s_name} ({comp['score']}/100, Z=+{comp['z_score']}) - performing top tier across cohort.")
        elif comp['z_score'] >= 0.3:
            insights['strengths'].append(f"Strong performance in {s_name} ({comp['score']}/100), exceeding class average by +{comp['difference']} marks.")
        elif comp['z_score'] <= -1.0:
            insights['areas_for_improvement'].append(f"Critical deficiency in {s_name} ({comp['score']}/100, Z={comp['z_score']}) - significantly below class average by {abs(comp['difference'])} marks.")
        elif comp['z_score'] < 0.0:
            insights['areas_for_improvement'].append(f"Room for growth in {s_name} ({comp['score']}/100), trailing class mean by {abs(comp['difference'])} marks.")

    # Trajectory
    pct = card['percentage']
    if pct >= 90:
        insights['learning_trajectory'] = 'Elite Academic Performance (Honor Roll Candidate)'
    elif pct >= 80:
        insights['learning_trajectory'] = 'Strong Progressive Learner (Excellence Potential)'
    elif pct >= 65:
        insights['learning_trajectory'] = 'Consistent Average Performer (Targeted Upskilling Required)'
    elif pct >= 50:
        insights['learning_trajectory'] = 'Marginal Standing (High Remedial Priority)'
    else:
        insights['learning_trajectory'] = 'Academic Probation Alert (Immediate Mentorship Mandated)'

    # Attendance impact
    att = card['attendance']
    corr = compute_attendance_correlation(df)
    predicted_from_att = round(corr['slope'] * att + corr['intercept'], 1)
    diff_from_pred = round(pct - predicted_from_att, 1)

    if att < 75.0:
        insights['attendance_impact_analysis'] = f"Attendance ({att}%) is critically below the 75% threshold. Increasing attendance to 85% is mathematically projected to boost overall score by ~+{round(corr['slope'] * (85 - att), 1)}%."
    elif diff_from_pred >= 5.0:
        insights['attendance_impact_analysis'] = f"Student is outperforming attendance-predicted score ({predicted_from_att}%) by +{diff_from_pred}%, demonstrating superior subject aptitude."
    else:
        insights['attendance_impact_analysis'] = f"Regular attendance ({att}%) is effectively anchoring academic consistency."

    # Actionable Recommendations
    w_clean = worst_sub.replace('_', ' ')
    b_clean = best_sub.replace('_', ' ')
    insights['actionable_recommendations'].append(f"Prioritize daily 45-minute revision blocks dedicated to {w_clean} to close the {abs(sub_comps[worst_sub]['difference'])} mark deficit.")
    insights['actionable_recommendations'].append(f"Leverage strong conceptual intuition in {b_clean} for peer mentoring or technical project competitions.")
    if att < 80.0:
        insights['actionable_recommendations'].append(f"Target 100% lecture attendance in the next 4 weeks to unlock higher internal grading thresholds.")

    return insights


def generate_cohort_executive_insights(df):
    if df.empty:
        return {}

    overall = compute_overall_statistics(df)
    sub_stats = compute_subject_statistics(df)
    corr = compute_attendance_correlation(df)
    branch_stats = compute_branch_analytics(df)

    # Find highest variance subject and lowest average subject
    means = {s: d['mean'] for s, d in sub_stats.items()}
    stds = {s: d['std'] for s, d in sub_stats.items()}

    hardest_sub = min(means, key=means.get)
    most_polarized_sub = max(stds, key=stds.get)
    top_branch = max(branch_stats, key=lambda b: branch_stats[b]['mean_percentage']) if branch_stats else 'N/A'

    insights = [
        {
            'type': 'subject_focus',
            'title': f"Hardest Subject: {hardest_sub.replace('_', ' ')}",
            'detail': f"Has the lowest cohort mean score ({sub_stats[hardest_sub]['mean']}/100) with a pass rate of {sub_stats[hardest_sub]['pass_rate']}%. Recommended for departmental remedial tutorials.",
            'icon': 'fa-triangle-exclamation',
            'severity': 'warning'
        },
        {
            'type': 'polarization',
            'title': f"High Variance Alert: {most_polarized_sub.replace('_', ' ')}",
            'detail': f"Shows standard deviation of {sub_stats[most_polarized_sub]['std']} marks, indicating a significant knowledge gap between top performers and struggling students.",
            'icon': 'fa-chart-line',
            'severity': 'info'
        },
        {
            'type': 'correlation',
            'title': f"Attendance Impact: r = {corr['r']}",
            'detail': f"Attendance statistically explains {round(corr['r_squared']*100, 1)}% of score variance. Institutional policy enforcing 75% attendance will directly reduce fail count.",
            'icon': 'fa-user-check',
            'severity': 'success'
        },
        {
            'type': 'branch_lead',
            'title': f"Leading Department: {top_branch}",
            'detail': f"Ranked #1 with average percentage of {branch_stats[top_branch]['mean_percentage']}% and pass rate of {branch_stats[top_branch]['pass_rate']}%.",
            'icon': 'fa-award',
            'severity': 'primary'
        }
    ]

    return {
        'executive_insights': insights,
        'hardest_subject': hardest_sub.replace('_', ' '),
        'most_polarized_subject': most_polarized_sub.replace('_', ' '),
        'top_branch': top_branch
    }


def compare_two_entities(df, id1, id2_or_type='branch_avg'):
    card1 = get_student_rank_card(df, id1)
    if not card1:
        return None

    if id2_or_type == 'branch_avg':
        branch = card1['branch']
        b_df = df[df['Branch'] == branch]
        entity2_name = f"{branch} Average"
        scores2 = {sub: round(float(np.mean(b_df[sub].to_numpy())), 1) for sub in SUBJECTS}
        att2 = round(float(np.mean(b_df['Attendance'].to_numpy())), 1)
        pct2 = round(float(np.mean(b_df['Percentage'].to_numpy())), 1)
    elif id2_or_type == 'topper':
        stats = compute_overall_statistics(df)
        topper_id = stats['topper']['student_id']
        card2 = get_student_rank_card(df, topper_id)
        entity2_name = f"Class Topper ({card2['name']})"
        scores2 = {sub: card2['subject_comparisons'][sub]['score'] for sub in SUBJECTS}
        att2 = card2['attendance']
        pct2 = card2['percentage']
    else:
        card2 = get_student_rank_card(df, id2_or_type)
        if not card2:
            return None
        entity2_name = f"{card2['name']} ({card2['student_id']})"
        scores2 = {sub: card2['subject_comparisons'][sub]['score'] for sub in SUBJECTS}
        att2 = card2['attendance']
        pct2 = card2['percentage']

    radar_labels = [s.replace('_', ' ') for s in SUBJECTS]
    radar_data1 = [card1['subject_comparisons'][s]['score'] for s in SUBJECTS]
    radar_data2 = [scores2[s] for s in SUBJECTS]

    return {
        'entity1': {
            'name': f"{card1['name']} ({card1['student_id']})",
            'student_id': card1['student_id'],
            'branch': card1['branch'],
            'attendance': card1['attendance'],
            'percentage': card1['percentage'],
            'grade': card1['grade'],
            'scores': {s.replace('_', ' '): card1['subject_comparisons'][s]['score'] for s in SUBJECTS}
        },
        'entity2': {
            'name': entity2_name,
            'attendance': att2,
            'percentage': pct2,
            'scores': {s.replace('_', ' '): scores2[s] for s in SUBJECTS}
        },
        'radar_labels': radar_labels,
        'radar_data1': radar_data1,
        'radar_data2': radar_data2
    }


def simulate_grade_impact(df, student_id, new_attendance, subject_marks_delta):
    card = get_student_rank_card(df, student_id)
    if not card:
        return None

    current_scores = {sub: card['subject_comparisons'][sub]['score'] for sub in SUBJECTS}
    simulated_scores = {}
    for sub in SUBJECTS:
        delta = float(subject_marks_delta.get(sub, 0.0))
        simulated_scores[sub] = float(np.clip(current_scores[sub] + delta, 0.0, 100.0))

    sim_total = round(sum(simulated_scores.values()), 1)
    sim_percentage = round(sim_total / len(SUBJECTS), 2)

    has_failed = any(m < PASS_MARK_PER_SUBJECT for m in simulated_scores.values()) or sim_percentage < 50.0
    sim_status = 'Fail' if has_failed else 'Pass'
    sim_grade = 'F'
    if not has_failed:
        for min_pct, g, _, _ in GRADE_RULES:
            if sim_percentage >= min_pct:
                sim_grade = g
                break

    # Calculate simulated class rank
    percentages = df['Percentage'].to_numpy(dtype=float).copy()
    # Replace current student's pct with simulated pct
    mask = df['Student_ID'] == card['student_id']
    if mask.any():
        idx = np.where(mask)[0][0]
        percentages[idx] = sim_percentage
    sim_rank = int(np.sum(percentages > sim_percentage)) + 1
    sim_percentile = round(float((np.sum(percentages <= sim_percentage) / len(percentages)) * 100.0), 2)

    return {
        'student_id': card['student_id'],
        'name': card['name'],
        'current': {
            'attendance': card['attendance'],
            'total_marks': card['total_marks'],
            'percentage': card['percentage'],
            'grade': card['grade'],
            'class_rank': card['class_rank'],
            'percentile': card['percentile'],
            'scores': current_scores
        },
        'simulated': {
            'attendance': new_attendance,
            'total_marks': sim_total,
            'percentage': sim_percentage,
            'grade': sim_grade,
            'status': sim_status,
            'class_rank': sim_rank,
            'percentile': sim_percentile,
            'rank_gain': card['class_rank'] - sim_rank,
            'percentage_gain': round(sim_percentage - card['percentage'], 2),
            'scores': simulated_scores
        }
    }

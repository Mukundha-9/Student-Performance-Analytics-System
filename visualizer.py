# ==============================================================================
# Visualization Suite Module - Aditya University Student Performance Analytics
# Generates academic charts & dashboards using Matplotlib and NumPy.
# ==============================================================================
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import (
    SUBJECTS,
    PASS_MARK_PER_SUBJECT,
    MIN_ATTENDANCE_REQUIRED,
    GRADE_RULES,
    GRADE_COLORS,
    PLOT_COLORS,
    REPORTS_DIR,
    INSTITUTION,
    DEPARTMENT
)
from analytics import (
    compute_overall_statistics,
    compute_subject_statistics,
    compute_attendance_correlation,
    compute_grade_distribution,
    get_student_rank_card
)

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except Exception:
    plt.style.use('default')


def plot_subject_averages(df, save_path=None, show_plot=False):
    sub_stats = compute_subject_statistics(df)
    if not sub_stats:
        return None

    subjects = list(sub_stats.keys())
    clean_names = [s.replace('_', ' ') for s in subjects]
    means = [sub_stats[s]['mean'] for s in subjects]
    highest = [sub_stats[s]['max'] for s in subjects]
    lowest = [sub_stats[s]['min'] for s in subjects]

    x = np.arange(len(subjects))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    rects1 = ax.bar(x - width, lowest, width, label='Lowest Mark', color='#ef4444', alpha=0.85)
    rects2 = ax.bar(x, means, width, label='Average Mark', color='#3b82f6', alpha=0.9)
    rects3 = ax.bar(x + width, highest, width, label='Highest Mark', color='#10b981', alpha=0.85)

    ax.axhline(PASS_MARK_PER_SUBJECT, color='#f59e0b', linestyle='--', linewidth=1.5, label='Pass Mark (40)')

    ax.set_ylabel('Marks Obtained (out of 100)', fontsize=11, fontweight='bold')
    ax.set_title(f'{INSTITUTION} - Subject-Wise Performance Analysis (Min, Mean, Max)', fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(clean_names, fontsize=9, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(axis='y', linestyle=':', alpha=0.7)

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(str(round(h, 1)),
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_grade_distribution(df, save_path=None, show_plot=False):
    grade_dist = compute_grade_distribution(df)
    if not grade_dist:
        return None

    labels = []
    sizes = []
    colors = []

    for grade_letter, data in grade_dist.items():
        if data['count'] > 0:
            labels.append(grade_letter + ' (' + str(data['count']) + ')')
            sizes.append(data['count'])
            colors.append(GRADE_COLORS.get(grade_letter, '#999999'))

    fig, ax = plt.subplots(figsize=(8, 7))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')

    stats = compute_overall_statistics(df)
    pass_pct = stats.get('pass_percentage', 0.0)
    total = stats.get('total_students', 0)

    center_text = 'Total\n' + str(total) + '\n\nPass Rate\n' + str(pass_pct) + '%'
    ax.text(0, 0, center_text, ha='center', va='center', fontsize=11, fontweight='bold', color='#1e293b')

    ax.set_title(f'{INSTITUTION} - Academic Grade Distribution', fontsize=13, fontweight='bold', pad=20)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_score_distribution(df, save_path=None, show_plot=False):
    percentages = df['Percentage'].to_numpy(dtype=float)
    mean = float(np.mean(percentages))
    std = float(np.std(percentages))
    median = float(np.median(percentages))

    fig, ax = plt.subplots(figsize=(10, 6))

    n, bins, patches = ax.hist(
        percentages, bins=12, density=True,
        color='#1e3a8a', edgecolor='white', alpha=0.75, label='Actual Frequency'
    )

    x_curve = np.linspace(min(percentages) - 5, max(percentages) + 5, 200)
    if std > 0:
        y_curve = (1.0 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - mean) / std) ** 2)
        curve_lbl = 'Normal Curve (mu=' + str(round(mean, 1)) + ', sigma=' + str(round(std, 1)) + ')'
        ax.plot(x_curve, y_curve, color='#ef4444', linewidth=2.5, label=curve_lbl)

    ax.axvline(mean, color='#ef4444', linestyle='--', linewidth=2, label='Mean (' + str(round(mean, 1)) + '%)')
    ax.axvline(median, color='#10b981', linestyle=':', linewidth=2, label='Median (' + str(round(median, 1)) + '%)')
    ax.axvline(50.0, color='#f59e0b', linestyle='-', linewidth=1.5, label='Pass Threshold (50%)')

    ax.set_xlabel('Percentage Score (%)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=11, fontweight='bold')
    ax.set_title(f'{INSTITUTION} - Class Marks Distribution & Gaussian Normal Fit', fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_attendance_vs_performance(df, save_path=None, show_plot=False):
    att = df['Attendance'].to_numpy(dtype=float)
    pct = df['Percentage'].to_numpy(dtype=float)
    status = df['Status'].to_numpy(dtype=str)

    corr_info = compute_attendance_correlation(df)
    r_val = corr_info['r']
    slope = corr_info['slope']
    intercept = corr_info['intercept']

    fig, ax = plt.subplots(figsize=(10, 6))

    pass_mask = status == 'Pass'
    ax.scatter(att[pass_mask], pct[pass_mask], color='#10b981', alpha=0.8, s=65, label='Passed Students', edgecolors='#0f172a', linewidth=0.5)
    ax.scatter(att[~pass_mask], pct[~pass_mask], color='#ef4444', alpha=0.9, s=80, marker='X', label='Failed Students')

    x_vals = np.linspace(att.min() - 2, att.max() + 2, 100)
    y_vals = slope * x_vals + intercept
    ax.plot(x_vals, y_vals, color='#3b82f6', linestyle='--', linewidth=2.5, label='Trendline: ' + corr_info['equation'])

    ax.axvline(MIN_ATTENDANCE_REQUIRED, color='#f59e0b', linestyle=':', linewidth=1.8, label='Min Attendance (75%)')

    stat_box = (
        'Pearson r: ' + str(r_val) + '\n' +
        'R-squared: ' + str(corr_info['r_squared']) + '\n' +
        'Correlation: ' + corr_info['interpretation']
    )
    ax.text(0.04, 0.92, stat_box, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='#cbd5e1'))

    ax.set_xlabel('Attendance Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Academic Score / Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'{INSTITUTION} - Attendance vs Academic Performance Correlation', fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='lower right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_performance_trends(df, save_path=None, show_plot=False):
    sorted_df = df.sort_values('Percentage', ascending=False).reset_index(drop=True)
    ranks = np.arange(1, len(sorted_df) + 1)
    percentages = sorted_df['Percentage'].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(ranks, percentages, color='#3b82f6', linewidth=2.5, marker='o', markersize=4, label='Student Percentage')
    ax.fill_between(ranks, percentages, 50, where=(percentages >= 50), color='#3b82f6', alpha=0.15, label='Passing Zone (>=50%)')

    p75 = np.percentile(percentages, 75)
    p50 = np.percentile(percentages, 50)
    p25 = np.percentile(percentages, 25)

    ax.axhline(p75, color='#10b981', linestyle=':', label='75th Percentile (' + str(round(p75, 1)) + '%)')
    ax.axhline(p50, color='#f59e0b', linestyle='--', label='50th Percentile / Median (' + str(round(p50, 1)) + '%)')
    ax.axhline(p25, color='#8b5cf6', linestyle=':', label='25th Percentile (' + str(round(p25, 1)) + '%)')
    ax.axhline(50.0, color='#ef4444', linestyle='-', linewidth=1.5, label='Pass Mark (50%)')

    ax.set_xlabel('Class Rank (Descending)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'{INSTITUTION} - Academic Performance Progression & Percentiles', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlim(1, len(sorted_df))
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_department_comparison(df, save_path=None, show_plot=False):
    col = 'Branch' if 'Branch' in df.columns else 'Department'
    branches = sorted(df[col].unique())
    data_by_branch = [df[df[col] == b]['Percentage'].to_numpy(dtype=float) for b in branches]

    fig, ax = plt.subplots(figsize=(11, 6))

    box = ax.boxplot(
        data_by_branch,
        patch_artist=True,
        tick_labels=[b.replace('Engineering', 'Eng.').replace('and', '&') for b in branches],
        medianprops=dict(color='black', linewidth=2),
        whiskerprops=dict(color='#555', linewidth=1.5),
        capprops=dict(color='#555', linewidth=1.5)
    )

    colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4']
    for patch, color in zip(box['boxes'], colors[:len(branches)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    ax.axhline(50.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Pass Mark (50%)')

    ax.set_ylabel('Percentage Score (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'{INSTITUTION} - Branch-Wise Performance Comparison', fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='lower right', frameon=True)
    ax.grid(axis='y', linestyle=':', alpha=0.7)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def generate_comprehensive_dashboard(df, save_path=None, show_plot=False):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    plt.suptitle(f'{INSTITUTION} - {DEPARTMENT}\nSTUDENT PERFORMANCE ANALYTICS DASHBOARD', fontsize=16, fontweight='bold', y=0.98)

    # 1. Top-Left: Subject Means & Highest (Bar Chart)
    sub_stats = compute_subject_statistics(df)
    sub_keys = list(sub_stats.keys())
    clean_subs = [s.replace('_', '\n') for s in sub_keys]
    sub_means = [sub_stats[s]['mean'] for s in sub_keys]
    sub_maxs = [sub_stats[s]['max'] for s in sub_keys]

    x = np.arange(len(sub_keys))
    w = 0.35
    axes[0, 0].bar(x - w/2, sub_means, w, label='Subject Average', color='#3b82f6', alpha=0.85)
    axes[0, 0].bar(x + w/2, sub_maxs, w, label='Subject Max', color='#10b981', alpha=0.85)
    axes[0, 0].axhline(40.0, color='#f59e0b', linestyle='--', label='Pass Mark (40)')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(clean_subs, fontsize=9, fontweight='bold')
    axes[0, 0].set_ylabel('Marks', fontweight='bold')
    axes[0, 0].set_title('Subject-Wise Average & Highest Marks', fontsize=12, fontweight='bold')
    axes[0, 0].legend(loc='upper right', fontsize=8)
    axes[0, 0].grid(axis='y', linestyle=':', alpha=0.7)

    # 2. Top-Right: Grade Distribution (Donut Chart)
    grade_dist = compute_grade_distribution(df)
    g_labels = []
    g_sizes = []
    g_colors = []
    for g, d in grade_dist.items():
        if d['count'] > 0:
            g_labels.append(g + ' (' + str(d['count']) + ')')
            g_sizes.append(d['count'])
            g_colors.append(GRADE_COLORS.get(g, '#999999'))

    axes[0, 1].pie(
        g_sizes, labels=g_labels, autopct='%1.0f%%', startangle=140,
        colors=g_colors, pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor='white')
    )
    axes[0, 1].set_title('Grade Distribution', fontsize=12, fontweight='bold')

    # 3. Bottom-Left: Attendance vs Performance (Scatter & Regression)
    att = df['Attendance'].to_numpy(dtype=float)
    pct = df['Percentage'].to_numpy(dtype=float)
    corr_info = compute_attendance_correlation(df)
    pass_m = df['Status'].to_numpy(dtype=str) == 'Pass'

    axes[1, 0].scatter(att[pass_m], pct[pass_m], color='#10b981', alpha=0.75, s=50, label='Pass')
    axes[1, 0].scatter(att[~pass_m], pct[~pass_m], color='#ef4444', alpha=0.85, s=60, marker='X', label='Fail')
    x_line = np.linspace(att.min() - 2, att.max() + 2, 50)
    axes[1, 0].plot(x_line, corr_info['slope'] * x_line + corr_info['intercept'], color='#3b82f6', linestyle='--', label='r = ' + str(corr_info['r']))
    axes[1, 0].set_xlabel('Attendance (%)', fontweight='bold')
    axes[1, 0].set_ylabel('Overall Percentage (%)', fontweight='bold')
    axes[1, 0].set_title('Attendance vs Performance (Linear Regression)', fontsize=12, fontweight='bold')
    axes[1, 0].legend(loc='lower right', fontsize=8)
    axes[1, 0].grid(True, linestyle=':', alpha=0.6)

    # 4. Bottom-Right: Score Distribution & Normal Fit (Histogram)
    axes[1, 1].hist(pct, bins=10, density=True, color='#1e3a8a', edgecolor='white', alpha=0.75, label='Frequency')
    mean_pct = float(np.mean(pct))
    std_pct = float(np.std(pct))
    if std_pct > 0:
        xc = np.linspace(pct.min() - 5, pct.max() + 5, 100)
        yc = (1.0 / (std_pct * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xc - mean_pct) / std_pct) ** 2)
        axes[1, 1].plot(xc, yc, '#ef4444', linewidth=2, label='Normal Fit')
    axes[1, 1].axvline(mean_pct, color='#ef4444', linestyle='--', label='Mean (' + str(round(mean_pct, 1)) + '%)')
    axes[1, 1].set_xlabel('Percentage Score (%)', fontweight='bold')
    axes[1, 1].set_ylabel('Density', fontweight='bold')
    axes[1, 1].set_title('Class Marks Distribution (Histogram & Gaussian Fit)', fontsize=12, fontweight='bold')
    axes[1, 1].legend(loc='upper left', fontsize=8)
    axes[1, 1].grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def save_all_visualizations(df, output_dir=None):
    if output_dir is None:
        output_dir = REPORTS_DIR
    os.makedirs(output_dir, exist_ok=True)

    generated_files = []

    p1 = os.path.join(output_dir, '01_subject_averages.png')
    plot_subject_averages(df, save_path=p1)
    generated_files.append(p1)

    p2 = os.path.join(output_dir, '02_grade_distribution.png')
    plot_grade_distribution(df, save_path=p2)
    generated_files.append(p2)

    p3 = os.path.join(output_dir, '03_score_distribution.png')
    plot_score_distribution(df, save_path=p3)
    generated_files.append(p3)

    p4 = os.path.join(output_dir, '04_attendance_correlation.png')
    plot_attendance_vs_performance(df, save_path=p4)
    generated_files.append(p4)

    p5 = os.path.join(output_dir, '05_performance_trends.png')
    plot_performance_trends(df, save_path=p5)
    generated_files.append(p5)

    p6 = os.path.join(output_dir, '06_department_comparison.png')
    plot_department_comparison(df, save_path=p6)
    generated_files.append(p6)

    p7 = os.path.join(output_dir, '07_comprehensive_dashboard.png')
    generate_comprehensive_dashboard(df, save_path=p7)
    generated_files.append(p7)

    return generated_files


# ==============================================================================
# INDIVIDUAL STUDENT VISUAL ANALYTICS SUITE (PERSONALIZED MATPLOTLIB CHARTS)
# ==============================================================================

def get_student_charts_list(student_id):
    clean_id = str(student_id).strip().upper()
    return [
        {
            'id': 1,
            'filename': '01_subject_mastery.png',
            'name': 'Subject Mastery vs Class Benchmark',
            'type': 'Comparative Bar Chart',
            'description': 'Individual subject marks directly compared with cohort average benchmark & passing cutoff'
        },
        {
            'id': 2,
            'filename': '02_cohort_position.png',
            'name': 'Cohort Standing & Gaussian Distribution',
            'type': 'Gaussian Fit & Percentile Marker',
            'description': 'Pinpoints exact student percentile rank on the university cohort normal distribution bell curve'
        },
        {
            'id': 3,
            'filename': '03_attendance_regression.png',
            'name': 'Attendance vs Performance Risk Coordinate',
            'type': 'Regression Model & Individual Coordinate',
            'description': 'Student position mapped onto the linear regression model with attendance threshold boundaries'
        },
        {
            'id': 4,
            'filename': '04_semester_trajectory.png',
            'name': 'Semester SGPA Progression Trajectory',
            'type': 'Longitudinal Trend Line',
            'description': 'Multi-semester academic trajectory tracking SGPA evolution across Semesters 1, 2, 3, and 4'
        },
        {
            'id': 5,
            'filename': '05_competency_radar.png',
            'name': 'Multi-Subject Competency Profile',
            'type': 'Polar Radar Chart',
            'description': 'Radial skill competency footprint comparing individual strengths vs cohort averages'
        },
        {
            'id': 6,
            'filename': '06_comprehensive_dashboard.png',
            'name': 'Personalized Executive Academic Dashboard',
            'type': '4-in-1 Individual Multi-Panel Dashboard',
            'description': 'Comprehensive student scorecard combining subject mastery, trajectory, regression, and cohort standing'
        }
    ]


def plot_student_subject_mastery(df, student_id, save_path=None, show_plot=False):
    card = get_student_rank_card(df, student_id)
    if not card or not card.get('subject_comparisons'):
        return None

    subjects = list(card['subject_comparisons'].keys())
    clean_names = [s.replace('_', ' ') for s in subjects]
    student_scores = [card['subject_comparisons'][s]['score'] for s in subjects]
    class_means = [card['subject_comparisons'][s]['class_mean'] for s in subjects]
    differences = [card['subject_comparisons'][s]['difference'] for s in subjects]

    x = np.arange(len(subjects))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10.5, 6))

    bar_colors = ['#10b981' if diff >= 0 else '#3b82f6' for diff in differences]
    rects1 = ax.bar(x - width/2, student_scores, width, label=f"Student Marks: {card['name']}", color=bar_colors, alpha=0.9, edgecolor='#0f172a', linewidth=0.5)
    rects2 = ax.bar(x + width/2, class_means, width, label='Cohort Average Benchmark', color='#94a3b8', alpha=0.8, edgecolor='#0f172a', linewidth=0.5)

    ax.axhline(PASS_MARK_PER_SUBJECT, color='#f59e0b', linestyle='--', linewidth=1.8, label=f'Pass Cutoff ({int(PASS_MARK_PER_SUBJECT)})')

    ax.set_ylabel('Marks Obtained (out of 100)', fontsize=11, fontweight='bold')
    ax.set_title(f"{INSTITUTION} - Individual Subject Mastery vs Cohort Benchmark\nStudent: {card['name']} (Roll: {card['student_id']}) • Branch: {card['branch']}", fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(clean_names, fontsize=9.5, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    ax.grid(axis='y', linestyle=':', alpha=0.7)

    # Annotate Student Bars
    for idx, rect in enumerate(rects1):
        h = rect.get_height()
        diff = differences[idx]
        diff_str = f"+{diff:.1f}" if diff >= 0 else f"{diff:.1f}"
        diff_color = '#047857' if diff >= 0 else '#b91c1c'
        ax.annotate(f"{h:.1f}\n({diff_str})",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=diff_color)

    # Annotate Mean Bars
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color='#475569')

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_student_cohort_position(df, student_id, save_path=None, show_plot=False):
    card = get_student_rank_card(df, student_id)
    if not card:
        return None

    percentages = df['Percentage'].to_numpy(dtype=float)
    s_pct = float(card['percentage'])
    mean_val = float(np.mean(percentages))
    std_val = float(np.std(percentages))
    median_val = float(np.median(percentages))

    fig, ax = plt.subplots(figsize=(10.5, 6))

    # Cohort frequency histogram
    n, bins, patches = ax.hist(percentages, bins=14, density=True, color='#cbd5e1', edgecolor='white', alpha=0.65, label='Cohort Frequency')

    # Gaussian bell curve
    x_curve = np.linspace(min(percentages) - 5, max(percentages) + 5, 200)
    if std_val > 0:
        y_curve = (1.0 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - mean_val) / std_val) ** 2)
        ax.plot(x_curve, y_curve, color='#3b82f6', linewidth=2.2, label=f'Cohort Normal Distribution (μ={mean_val:.1f}, σ={std_val:.1f})')

        # Shading percentile up to student's score
        x_fill = x_curve[x_curve <= s_pct]
        y_fill = y_curve[x_curve <= s_pct]
        ax.fill_between(x_fill, y_fill, color='#10b981', alpha=0.25, label=f"Percentile Shading (Top {100 - card['percentile']:.1f}%)")

    ax.axvline(mean_val, color='#64748b', linestyle='--', linewidth=1.5, label=f'Cohort Mean ({mean_val:.1f}%)')
    ax.axvline(median_val, color='#8b5cf6', linestyle=':', linewidth=1.5, label=f'Cohort Median ({median_val:.1f}%)')
    ax.axvline(s_pct, color='#ea580c', linestyle='-', linewidth=2.8, label=f"Student Score: {s_pct:.2f}%")

    y_max = ax.get_ylim()[1]
    callout_text = (
        f">> YOU ARE HERE <<\n"
        f"{card['name']} ({card['student_id']})\n"
        f"Score: {s_pct:.2f}%\n"
        f"Class Rank: #{card['class_rank']} of {card['total_students']}\n"
        f"Standing: Top {100 - card['percentile']:.1f}% ({card['grade']} Grade)"
    )

    offset_x = 5 if s_pct < mean_val else -22
    ax.annotate(callout_text,
                xy=(s_pct, y_max * 0.70),
                xytext=(s_pct + offset_x, y_max * 0.75),
                arrowprops=dict(facecolor='#ea580c', edgecolor='#0f172a', width=1.8, headwidth=7, shrink=0.08),
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#fffbeb', edgecolor='#ea580c', linewidth=1.8),
                fontsize=9.5, fontweight='bold', color='#0f172a')

    ax.set_xlabel('Overall Percentage Score (%)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=11, fontweight='bold')
    ax.set_title(f"{INSTITUTION} - Class Marks Distribution & Individual Student Standing\nStudent: {card['name']} (Roll: {card['student_id']})", fontsize=12, fontweight='bold', pad=15)
    ax.legend(loc='upper left', frameon=True, fontsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_student_attendance_regression(df, student_id, save_path=None, show_plot=False):
    card = get_student_rank_card(df, student_id)
    if not card:
        return None

    att = df['Attendance'].to_numpy(dtype=float)
    pct = df['Percentage'].to_numpy(dtype=float)
    corr_info = compute_attendance_correlation(df)

    s_att = float(card['attendance'])
    s_pct = float(card['percentage'])

    fig, ax = plt.subplots(figsize=(10.5, 6))

    # All other cohort students in subtle gray
    ax.scatter(att, pct, color='#94a3b8', alpha=0.35, s=35, label='Cohort Students (500)', edgecolors='none')

    # Regression Line
    x_vals = np.linspace(att.min() - 2, att.max() + 2, 100)
    y_vals = corr_info['slope'] * x_vals + corr_info['intercept']
    ax.plot(x_vals, y_vals, color='#3b82f6', linestyle='--', linewidth=2.2, label=f"Trendline: {corr_info['equation']} (r={corr_info['r']})")

    ax.axvline(MIN_ATTENDANCE_REQUIRED, color='#ef4444', linestyle=':', linewidth=1.8, label=f'Min Required Attendance ({int(MIN_ATTENDANCE_REQUIRED)}%)')

    # Target Student as glowing gold star
    ax.scatter([s_att], [s_pct], color='#f59e0b', s=350, marker='*', edgecolor='#0f172a', linewidth=1.5, zorder=10, label=f"Student Position: {card['name']}")

    quadrant = "Exemplary (High Attendance & Score)" if s_att >= 75 and s_pct >= 75 else ("At-Risk" if s_att < 75 else "Moderate")
    callout = (
        f"[STUDENT] {card['name']} ({card['student_id']})\n"
        f"Attendance: {s_att:.1f}%\n"
        f"Score: {s_pct:.2f}%\n"
        f"Zone: {quadrant}"
    )
    offset_x = -14 if s_att > 75 else 6
    offset_y = 8 if s_pct < 85 else -14
    ax.annotate(callout,
                xy=(s_att, s_pct),
                xytext=(s_att + offset_x, s_pct + offset_y),
                arrowprops=dict(facecolor='#f59e0b', edgecolor='#0f172a', width=1.8, headwidth=7, shrink=0.08),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#f59e0b', linewidth=1.8),
                fontsize=9, fontweight='bold', color='#0f172a')

    ax.set_xlabel('Attendance Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Academic Score / Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_title(f"{INSTITUTION} - Attendance vs Academic Score & Individual Student Coordinate\nStudent: {card['name']} (Roll: {card['student_id']})", fontsize=12, fontweight='bold', pad=15)
    ax.legend(loc='lower right', frameon=True, fontsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_student_semester_trajectory(df, student_id, save_path=None, show_plot=False):
    import portal_manager
    card = get_student_rank_card(df, student_id)
    if not card:
        return None

    profile = portal_manager.get_student_complete_profile(student_id)
    ledgers = profile.get('semesters_ledger', [])

    if not ledgers:
        sem_labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
        p_val = card['percentage'] / 10.0
        sgpas = [max(5.0, round(p_val - 0.2, 2)), max(5.0, round(p_val - 0.1, 2)), max(5.0, round(p_val, 2)), max(5.0, round(p_val + 0.1, 2))]
    else:
        sem_labels = [s.get('semester_title', f"Sem {i+1}").split('(')[0].strip() for i, s in enumerate(ledgers)]
        sgpas = [float(s.get('sgpa', 8.0)) for s in ledgers]

    cgpa = profile.get('overall_cgpa', round(float(np.mean(sgpas)), 2))

    fig, ax = plt.subplots(figsize=(10.5, 6))
    x = np.arange(len(sem_labels))

    ax.plot(x, sgpas, color='#0284c7', linewidth=2.8, marker='o', markersize=9, markerfacecolor='#0284c7', markeredgecolor='white', markeredgewidth=2, label='Semester SGPA')
    ax.fill_between(x, sgpas, y2=max(0, min(sgpas) - 0.5), color='#0284c7', alpha=0.15)

    ax.axhline(cgpa, color='#10b981', linestyle='--', linewidth=2, label=f'Cumulative CGPA ({cgpa})')
    ax.axhline(10.0, color='#f59e0b', linestyle=':', linewidth=1.5, label='Outstanding Target (10.0)')

    ax.set_ylabel('Grade Point Average (SGPA / CGPA on 10.0 Scale)', fontsize=10.5, fontweight='bold')
    ax.set_title(f"{INSTITUTION} - Semester-by-Semester SGPA Progression Trajectory\nStudent: {card['name']} (Roll: {card['student_id']}) • Overall CGPA: {cgpa}", fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(sem_labels, fontsize=10, fontweight='bold')
    ax.set_ylim(max(0, min(sgpas) - 1.0), 10.5)
    ax.legend(loc='lower right', frameon=True, fontsize=9)
    ax.grid(True, linestyle=':', alpha=0.6)

    for i, txt in enumerate(sgpas):
        ax.annotate(f"{txt:.2f} SGPA",
                    xy=(x[i], sgpas[i]),
                    xytext=(0, 8), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0369a1')

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_student_competency_radar(df, student_id, save_path=None, show_plot=False):
    card = get_student_rank_card(df, student_id)
    if not card or not card.get('subject_comparisons'):
        return None

    subjects = list(card['subject_comparisons'].keys())
    clean_labels = [s.replace('_', ' ') for s in subjects]
    scores = [float(card['subject_comparisons'][s]['score']) for s in subjects]
    means = [float(card['subject_comparisons'][s]['class_mean']) for s in subjects]

    num_vars = len(subjects)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Close polygons
    scores += scores[:1]
    means += means[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8.5, 7.5), subplot_kw=dict(polar=True))

    ax.plot(angles, scores, color='#0284c7', linewidth=2.5, linestyle='solid', label=f"Student Score: {card['name']}")
    ax.fill(angles, scores, color='#0284c7', alpha=0.35)

    ax.plot(angles, means, color='#10b981', linewidth=2, linestyle='dashed', label='Cohort Average Benchmark')
    ax.fill(angles, means, color='#10b981', alpha=0.15)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(clean_labels, fontsize=9.5, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.set_rlabel_position(30)
    ax.tick_params(colors='#475569')

    plt.title(f"{INSTITUTION} - Multi-Dimensional Subject Competency Radar\nStudent: {card['name']} (Roll: {card['student_id']})", fontsize=12, fontweight='bold', pad=25)
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=9)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def plot_student_comprehensive_dashboard(df, student_id, save_path=None, show_plot=False):
    import portal_manager
    card = get_student_rank_card(df, student_id)
    if not card:
        return None

    profile = portal_manager.get_student_complete_profile(student_id)
    ledgers = profile.get('semesters_ledger', [])

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))

    # 1. Top-Left: Subject Mastery Comparison (Bar Chart)
    subjects = list(card['subject_comparisons'].keys())
    clean_names = [s.replace('_', ' ') for s in subjects]
    student_scores = [card['subject_comparisons'][s]['score'] for s in subjects]
    class_means = [card['subject_comparisons'][s]['class_mean'] for s in subjects]

    x = np.arange(len(subjects))
    w = 0.35
    axes[0, 0].bar(x - w/2, student_scores, w, label='Student Score', color='#0284c7', alpha=0.9)
    axes[0, 0].bar(x + w/2, class_means, w, label='Class Average', color='#94a3b8', alpha=0.8)
    axes[0, 0].axhline(PASS_MARK_PER_SUBJECT, color='#f59e0b', linestyle='--', label='Pass Mark (40)')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(clean_names, fontsize=8.5, fontweight='bold')
    axes[0, 0].set_ylabel('Marks', fontweight='bold')
    axes[0, 0].set_title('Subject Mastery vs Class Benchmark', fontsize=11, fontweight='bold')
    axes[0, 0].legend(loc='upper right', fontsize=8)
    axes[0, 0].grid(axis='y', linestyle=':', alpha=0.6)

    # 2. Top-Right: Semester SGPA Progression
    if ledgers:
        sem_labels = [s.get('semester_title', f"Sem {i+1}").split('(')[0].strip() for i, s in enumerate(ledgers)]
        sgpas = [float(s.get('sgpa', 8.0)) for s in ledgers]
    else:
        sem_labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
        p_val = card['percentage'] / 10.0
        sgpas = [max(5.0, round(p_val - 0.2, 2)), max(5.0, round(p_val - 0.1, 2)), max(5.0, round(p_val, 2)), max(5.0, round(p_val + 0.1, 2))]
    cgpa = profile.get('overall_cgpa', round(float(np.mean(sgpas)), 2))

    x_sem = np.arange(len(sem_labels))
    axes[0, 1].plot(x_sem, sgpas, color='#10b981', linewidth=2.5, marker='o', label='Semester SGPA')
    axes[0, 1].axhline(cgpa, color='#0284c7', linestyle='--', label=f'CGPA ({cgpa})')
    axes[0, 1].set_xticks(x_sem)
    axes[0, 1].set_xticklabels(sem_labels, fontsize=8.5, fontweight='bold')
    axes[0, 1].set_ylabel('SGPA (on 10.0 scale)', fontweight='bold')
    axes[0, 1].set_title('Semester SGPA Academic Trajectory', fontsize=11, fontweight='bold')
    axes[0, 1].legend(loc='lower right', fontsize=8)
    axes[0, 1].grid(True, linestyle=':', alpha=0.6)

    # 3. Bottom-Left: Attendance vs Performance Linear Regression Coordinate
    att = df['Attendance'].to_numpy(dtype=float)
    pct = df['Percentage'].to_numpy(dtype=float)
    corr_info = compute_attendance_correlation(df)
    axes[1, 0].scatter(att, pct, color='#cbd5e1', alpha=0.4, s=25, label='Cohort (500)')
    x_line = np.linspace(att.min() - 2, att.max() + 2, 50)
    axes[1, 0].plot(x_line, corr_info['slope'] * x_line + corr_info['intercept'], color='#3b82f6', linestyle='--', label=f"Trendline (r={corr_info['r']})")
    axes[1, 0].axvline(MIN_ATTENDANCE_REQUIRED, color='#ef4444', linestyle=':', label='Min Att (75%)')
    axes[1, 0].scatter([card['attendance']], [card['percentage']], color='#f59e0b', s=250, marker='*', edgecolor='#0f172a', zorder=10, label=f"Student ({card['attendance']}%, {card['percentage']}%)")
    axes[1, 0].set_xlabel('Attendance (%)', fontweight='bold')
    axes[1, 0].set_ylabel('Percentage (%)', fontweight='bold')
    axes[1, 0].set_title('Attendance vs Performance Coordinate', fontsize=11, fontweight='bold')
    axes[1, 0].legend(loc='lower right', fontsize=8)
    axes[1, 0].grid(True, linestyle=':', alpha=0.6)

    # 4. Bottom-Right: Cohort Bell Curve & Standing
    mean_val = float(np.mean(pct))
    std_val = float(np.std(pct))
    axes[1, 1].hist(pct, bins=12, density=True, color='#e2e8f0', edgecolor='white', alpha=0.7)
    if std_val > 0:
        xc = np.linspace(pct.min() - 5, pct.max() + 5, 100)
        yc = (1.0 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xc - mean_val) / std_val) ** 2)
        axes[1, 1].plot(xc, yc, color='#3b82f6', linewidth=2, label='Normal Fit')
    axes[1, 1].axvline(card['percentage'], color='#ea580c', linewidth=2.5, linestyle='-', label=f"Student ({card['percentage']}%)")
    axes[1, 1].axvline(mean_val, color='#64748b', linestyle='--', label=f"Class Mean ({mean_val:.1f}%)")
    axes[1, 1].set_xlabel('Percentage (%)', fontweight='bold')
    axes[1, 1].set_ylabel('Density', fontweight='bold')
    axes[1, 1].set_title(f"Class Standing: Rank #{card['class_rank']} (Top {100-card['percentile']:.1f}%)", fontsize=11, fontweight='bold')
    axes[1, 1].legend(loc='upper left', fontsize=8)
    axes[1, 1].grid(True, linestyle=':', alpha=0.6)

    master_title = (
        f"{INSTITUTION} - INDIVIDUAL STUDENT PERFORMANCE ANALYTICS DASHBOARD\n"
        f"Student: {card['name']} | Roll No: {card['student_id']} | Branch: {card['branch']} | CGPA: {cgpa} | Attendance: {card['attendance']}% | Rank: #{card['class_rank']}"
    )
    fig.suptitle(master_title, fontsize=12.5, fontweight='bold', color='#0f2b5c', y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show_plot:
        plt.show()
    plt.close()
    return save_path


def generate_student_visual_analytics(df, student_id, output_dir=None):
    clean_id = str(student_id).strip().upper()
    if output_dir is None:
        output_dir = os.path.join(REPORTS_DIR, 'students', clean_id)
    os.makedirs(output_dir, exist_ok=True)

    charts_info = get_student_charts_list(clean_id)

    plot_student_subject_mastery(df, clean_id, save_path=os.path.join(output_dir, '01_subject_mastery.png'))
    plot_student_cohort_position(df, clean_id, save_path=os.path.join(output_dir, '02_cohort_position.png'))
    plot_student_attendance_regression(df, clean_id, save_path=os.path.join(output_dir, '03_attendance_regression.png'))
    plot_student_semester_trajectory(df, clean_id, save_path=os.path.join(output_dir, '04_semester_trajectory.png'))
    plot_student_competency_radar(df, clean_id, save_path=os.path.join(output_dir, '05_competency_radar.png'))
    plot_student_comprehensive_dashboard(df, clean_id, save_path=os.path.join(output_dir, '06_comprehensive_dashboard.png'))

    return charts_info

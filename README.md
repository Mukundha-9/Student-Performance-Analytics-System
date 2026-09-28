# Student Performance Analytics System
### Data-Driven Analysis of Student Academic Performance
**Department of Computer Science & Engineering • Aditya University**  
*Course:* Data Analysis Essentials (DAE)

---

### 🌐 Live Interactive Portal (Direct Web Link)
[![Live Portal](https://img.shields.io/badge/Live%20Demo-Open%20Portal-success?style=for-the-badge&logo=googlechrome)](https://providing-apparel-decreased-bennett.trycloudflare.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Mukundha-9/Student-Performance-Analytics-System)

👉 **Direct Live URL:** [**https://providing-apparel-decreased-bennett.trycloudflare.com**](https://providing-apparel-decreased-bennett.trycloudflare.com)  
*(Opens directly in any browser on mobile, tablet, or desktop without installing anything)*

#### 🔑 Quick Demo Credentials:
- **Student Portal:** `25B11CS380` / `aditya@123`
- **Faculty Portal:** `FAC_CS_101` / `faculty@123`
- **Admin Portal:** `admin` / `admin@123`

---

## ?? Project Team Members

| Name | Roll Number / Student ID | Role in Project |
| :--- | :--- | :--- |
| **KALYANAM MUKUNDHA** | `25B11CS380` | Team Lead & Backend Developer |
| **TADICHERLA SAI ABHIRAM** | `25B11CS932` | Data Analyst & NumPy Specialist |
| **KOVVURI SAMEER REDDY** | `25B11CS490` | Data Engineer & Pandas Specialist |
| **SHAIK SAJID** | `25B11CS891` | Frontend UI & Visualization Specialist |

---

## ?? Project Abstract & Overview

The **Student Performance Analytics System** is an automated data analysis and web application project designed to evaluate, analyze, and visualize the academic performance of engineering students using **Python 3.x**, **NumPy**, **Pandas**, and **Matplotlib**, coupled with a responsive **HTML5/CSS3/JavaScript** frontend dashboard.

The system imports raw student data from a structured CSV file containing attendance, branch, semester, and marks obtained across 5 core academic subjects. It implements:
1. **Pandas** for structured data handling, cleaning, missing value imputation, duplicate removal, search, and dynamic filtering.
2. **NumPy** for numerical and statistical operations including Class Average ($\mu$), Standard Deviation ($\sigma$), Variance ($\sigma^2$), Quartiles ($Q_1, Q_2, Q_3$, IQR), Range, Z-Scores, and Attendance vs. Score Correlation ($r, R^2$, Linear Regression $y = mx + c$).
3. **Matplotlib** for generating 7 publication-quality visual plots and multi-panel executive dashboards.
4. **HTML5, CSS3, JavaScript & Flask** for a single-page web dashboard with interactive Chart.js charts, real-time CRUD management, student report card generator, and instant report export.

---

## ??? 5-Stage Processing Pipeline

```
+--------------+     +--------------+     +--------------+     +--------------+     +----------------------+
  Input CSV    -->  Data Cleaning -->   NumPy Math   --> Matplotlib &   -->  Actionable Insights  
(~100-500 rec)     (Pandas CRUD)      (, s, IQR, r)     Web Chart.js       (Web UI & Report Card)
+--------------+     +--------------+     +--------------+     +--------------+     +----------------------+
```

1. **Input Stage:** CSV dataset containing Student ID, Name, Branch, Semester, Attendance (%), and 5 core subject marks (0-100 scale).
2. **Data Cleaning & Management:** Pandas handles missing values, removes duplicates, validates mark bounds (0-100) and attendance (0-100%).
3. **Statistical Computations:** NumPy vector calculations for central tendency, dispersion, quartiles, percentiles, correlation, and regression.
4. **Data Visualization:** Matplotlib generates high-res figures; Chart.js provides dynamic frontend charts.
5. **Insights & Action:** Interactive Web Dashboard, Top 10 Honor Roll, At-Risk Early Warning alerts (<75% attendance), and Official Student Grade Sheets.

---

## ?? Academic Grading Scale (Aditya University Standard)

| Grade | Score Range (%) | Grade Point | Academic Classification | Status |
| :---: | :---: | :---: | :--- | :---: |
| **A+** | 90  100 | 10.0 | Outstanding | Pass |
| **A** | 80  89 | 9.0 | Excellent | Pass |
| **B** | 70  79 | 8.0 | Good | Pass |
| **C** | 60  69 | 7.0 | Average | Pass |
| **D** | 50  59 | 6.0 | Below Average | Pass |
| **F** | < 50 (or sub < 40) | 0.0 | Fail | Fail |

---

## ?? Matplotlib Visualization Suite

The system automatically generates and saves the following 7 high-resolution (300 DPI) plots in `reports/`:
1. `01_subject_averages.png`: Grouped Bar Chart comparing Subject Minimum, Mean, and Maximum marks.
2. `02_grade_distribution.png`: Academic Grade Distribution Donut/Pie Chart with pass rate callout.
3. `03_score_distribution.png`: Marks Distribution Histogram with Gaussian Normal Distribution bell curve.
4. `04_attendance_correlation.png`: Attendance vs. Academic Score Scatter Plot with linear regression best-fit line ($y = mx + c$) and Pearson correlation coefficient ($r$).
5. `05_performance_trends.png`: Academic Performance Progression Line Chart across cohort ranks with 25th, 50th, and 75th percentile bands.
6. `06_department_comparison.png`: Branch-Wise Performance Box-and-Whisker Plot.
7. `07_comprehensive_dashboard.png`: 4-in-1 Executive Analytics Dashboard.

---

## ?? How to Run the Project

### 1. Prerequisites & Dependencies
Ensure Python 3.x is installed, then install requirements:
```bash
pip install -r requirements.txt
```
*(Dependencies: `numpy>=1.24.0`, `pandas>=2.0.0`, `matplotlib>=3.7.0`, `flask>=3.0.0`)*

### 2. Launch the Web Application (HTML/CSS Frontend)
To run the interactive browser dashboard:
```bash
python app.py
```
Open your browser and navigate to:
?? **`http://127.0.0.1:5000`**

### 3. Launch the Interactive Console CLI
To run the menu-driven command line interface:
```bash
python main.py
```

### 4. Run Automated System Tests
To verify all NumPy statistics, Pandas CRUD, and Matplotlib figure generations:
```bash
python test_system.py
```

### 5. Generate Academic Performance Report
To re-generate the analytical report in Markdown and save all chart images:
```bash
python generate_report.py
```

---

## ?? Project Directory Structure

```
student_performance_analysis/

+-- config.py                 # Core configurations & university metadata
+-- sample_data.py            # Dataset generator (100 student records with Aditya Univ IDs)
+-- data_manager.py           # Pandas CRUD, data cleaning & validation engine
+-- analytics.py              # NumPy statistical calculations (, s, quartiles, regression)
+-- visualizer.py             # Matplotlib charts & high-res PNG dashboard generator
+-- generate_report.py        # Academic markdown performance report generator
+-- main.py                   # Interactive Console CLI interface
+-- app.py                    # Flask Web Backend & REST API server
+-- test_system.py            # Automated Unit & Integration test suite
+-- requirements.txt          # Project dependencies
+-- README.md                 # Complete documentation

+-- static/                   # Frontend assets
   +-- css/
      +-- style.css         # Modern, responsive, university-branded CSS styling
   +-- js/
       +-- app.js            # Dynamic dashboard interactions, AJAX, Chart.js & modals

+-- templates/
   +-- index.html            # Single-Page Application (SPA) Web Dashboard

+-- data/
   +-- students_data.csv     # Student database (CSV format)

+-- reports/                  # Exported charts (PNG) and academic report (MD)
    +-- 01_subject_averages.png
    +-- 02_grade_distribution.png
    +-- 03_score_distribution.png
    +-- 04_attendance_correlation.png
    +-- 05_performance_trends.png
    +-- 06_department_comparison.png
    +-- 07_comprehensive_dashboard.png
    +-- academic_performance_report.md
```

---

## ?? Key Highlights & DAE Curriculum Alignment

- **Pandas Data Management:** Demonstrates efficient CSV loading, boolean indexing, duplicate detection, missing value handling, grouping, and multi-criteria querying.
- **NumPy Numerical Suite:** Demonstrates vectorized operations without slow Python loops, array manipulation, percentile segmentation, correlation matrix computation, and linear algebra regression.
- **Matplotlib Visualization:** Generates publication-ready figures with custom color themes, data labels, annotations, and statistical overlays.
- **Modern Web Interface:** Clean HTML5/CSS3/JavaScript dashboard with glassmorphism design, real-time search, interactive charts, and printable report cards.

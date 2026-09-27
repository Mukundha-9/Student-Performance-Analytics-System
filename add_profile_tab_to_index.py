# add_profile_tab_to_index.py
import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Enhanced Student Attendance Tab with Interactive Simulator Slider & Radial Gauge
enhanced_attendance_tab = """
                <!-- TAB: Student Subject-Wise Attendance, 75% Rule & Interactive Simulator -->
                <section class="tab-content" id="student-attendance-tab">
                    <!-- Top Attendance KPI Summary -->
                    <div class="kpi-grid mb-3">
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-blue"><i class="fa-solid fa-clipboard-user"></i></div>
                            <div class="kpi-data">
                                <span>Overall Attendance</span>
                                <h3 id="att-overall-pct">98.0%</h3>
                                <small id="att-overall-status" class="text-success"><i class="fa-solid fa-circle-check"></i> Eligible for Exams (>=75%)</small>
                            </div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-emerald"><i class="fa-solid fa-calendar-check"></i></div>
                            <div class="kpi-data">
                                <span>Attended / Conducted</span>
                                <h3 id="att-total-counts">217 / 221</h3>
                                <small id="att-absent-count" class="text-muted">4 Classes Absent</small>
                            </div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-purple"><i class="fa-solid fa-calculator"></i></div>
                            <div class="kpi-data">
                                <span>Bunk / Recovery Margin</span>
                                <h3 id="att-margin-stat" style="color:var(--primary-light);">68 Classes</h3>
                                <small id="att-margin-desc" class="text-success">Safe Missable Margin</small>
                            </div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-amber"><i class="fa-solid fa-triangle-exclamation"></i></div>
                            <div class="kpi-data">
                                <span>Missed Periods (Recent)</span>
                                <h3 id="att-recent-absences-count">2 Periods</h3>
                                <small class="text-warning">Past 5 Academic Days</small>
                            </div>
                        </div>
                    </div>

                    <!-- Interactive Live Bunk & Catch-Up Simulator Desk -->
                    <div class="panel-card mb-3" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.2) 0%, rgba(15, 23, 42, 0.6) 100%); border-left: 5px solid var(--primary);">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-sliders text-primary"></i> Interactive Period Bunk & Catch-Up Simulator</h3>
                                <p class="text-muted" style="font-size:12.5px;">Drag slider to forecast your new attendance % if you miss or attend upcoming class periods</p>
                            </div>
                            <button class="btn btn-sm btn-outline" onclick="resetBunkSlider()"><i class="fa-solid fa-rotate-left"></i> Reset</button>
                        </div>
                        <div class="grid-2-columns" style="align-items:center;">
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-weight:700;">
                                    <span style="color:#f87171;"><i class="fa-solid fa-circle-minus"></i> Miss Classes (Bunk)</span>
                                    <span id="slider-change-label" style="color:var(--primary-light); font-size:15px;">No Change (0 Classes)</span>
                                    <span style="color:#34d399;"><i class="fa-solid fa-circle-plus"></i> Attend Extra Classes</span>
                                </div>
                                <input type="range" id="bunk-simulator-range" min="-15" max="15" value="0" step="1" style="width:100%; cursor:pointer; accent-color:#3b82f6;">
                                <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-muted); margin-top:4px;">
                                    <span>-15 Missed</span>
                                    <span>Current Standing</span>
                                    <span>+15 Attended</span>
                                </div>
                            </div>
                            <div class="bunk-sim-result-box" style="background:var(--bg-main); padding:14px 18px; border-radius:8px; border:1px solid var(--border-color); text-align:center;">
                                <span style="font-size:11.5px; color:var(--text-muted); text-transform:uppercase; font-weight:700;">Simulated Attendance Forecast</span>
                                <h2 id="sim-projected-pct" style="font-size:28px; font-weight:900; margin:4px 0; color:#10b981;">98.0%</h2>
                                <span id="sim-status-badge" class="badge badge-success" style="font-size:12px;"><i class="fa-solid fa-circle-check"></i> Eligible for Semester Exams</span>
                            </div>
                        </div>
                    </div>

                    <!-- Subject-Wise Attendance Breakdown & 75% Rule Planner -->
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-book-open-reader text-primary"></i> Subject-Wise Attendance & 75% Mandatory Examination Rule</h3>
                                <p class="text-muted" style="font-size:12.5px;">University Regulation: Minimum 75.0% attendance in each individual subject is strictly required to appear for Semester Examinations.</p>
                            </div>
                            <span class="badge badge-info" style="font-size:12px;"><i class="fa-solid fa-shield-halved"></i> 75% Examination Criterion</span>
                        </div>
                        <div class="subject-attendance-grid" id="student-subject-attendance-cards">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>

                    <!-- Period-by-Period Daily Attendance Tracker & 4-Day Back Log -->
                    <div class="grid-2-columns">
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-clock-rotate-left text-primary"></i> Class-Wise Period Attendance Diary</h3>
                                    <p class="text-muted" style="font-size:12px;">Period-by-period tracking for Today and previous 4 academic days</p>
                                </div>
                            </div>
                            
                            <!-- Day Selector Buttons -->
                            <div class="att-day-selector mb-3" id="att-day-selector-btns">
                                <!-- Populated dynamically via JS -->
                            </div>

                            <div class="table-responsive">
                                <table class="data-table table-sm" id="att-period-diary-table">
                                    <thead>
                                        <tr>
                                            <th>Period & Time</th>
                                            <th>Subject Taught</th>
                                            <th>Faculty & Venue</th>
                                            <th>Attendance Status</th>
                                        </tr>
                                    </thead>
                                    <tbody id="att-period-diary-tbody"></tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Period Absence Alerts & Notification Feed -->
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-bell text-danger"></i> Period Absence Alerts & Immediate Warnings</h3>
                                    <p class="text-muted" style="font-size:12px;">Instant notifications for individual missed class periods</p>
                                </div>
                            </div>
                            <div class="absence-alerts-feed" id="student-absence-alerts-list">
                                <!-- Populated dynamically via JS -->
                            </div>
                        </div>
                    </div>
                </section>
"""

# Replace existing attendance section
html = re.sub(r'<!-- TAB: Student Subject-Wise Attendance & Smart Calculator -->[\s\S]*?<!-- TAB: Student Notifications & Circulars Hub -->', enhanced_attendance_tab + '\n                <!-- TAB: Student Notifications & Circulars Hub -->', html)

# New Student Profile & Multi-Semester Marks Ledger Tab
student_profile_tab_html = """
                <!-- TAB: Student Official Profile & Multi-Semester Academic Ledger -->
                <section class="tab-content" id="student-profile-tab">
                    <!-- Profile Hero Banner Card -->
                    <div class="profile-hero-card mb-3">
                        <div class="profile-hero-avatar">
                            <i class="fa-solid fa-user-graduate"></i>
                        </div>
                        <div class="profile-hero-info">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                                <div>
                                    <h2 id="prof-student-name">Kalyanam Mukundha</h2>
                                    <p class="profile-hero-sub" id="prof-student-meta">Roll No: 25B11CS380 • Computer Science & Engineering • Section A</p>
                                </div>
                                <div style="display:flex; gap:8px;">
                                    <button class="btn btn-primary" onclick="printOfficialTranscript()"><i class="fa-solid fa-print"></i> Print Official Consolidated Transcript</button>
                                </div>
                            </div>
                            <div class="profile-badges-row mt-2">
                                <span class="badge badge-primary" id="prof-academic-year">Batch 2024 - 2028</span>
                                <span class="badge badge-info" id="prof-admission-type">Convener Quota (EAPCET)</span>
                                <span class="badge badge-success" id="prof-cgpa-badge">Cumulative CGPA: 9.27 / 10.0</span>
                                <span class="badge badge-warning" id="prof-mentor-badge">Proctor: Dr. A. K. Sharma</span>
                            </div>
                        </div>
                    </div>

                    <!-- Personal, Family & Contact Credentials Grid -->
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-address-card text-primary"></i> Personal, Family & Contact Information</h3>
                            <span class="badge badge-info"><i class="fa-solid fa-shield-halved"></i> Verified University Records</span>
                        </div>
                        <div class="profile-details-grid">
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-user"></i> Student Full Name</span>
                                <strong class="prof-val" id="prof-val-name">Kalyanam Mukundha</strong>
                            </div>
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-id-badge"></i> University Roll Number</span>
                                <strong class="prof-val" id="prof-val-roll">25B11CS380</strong>
                            </div>
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-user-tie"></i> Father's Name</span>
                                <strong class="prof-val" id="prof-val-father">Kalyanam Venkata Rao</strong>
                            </div>
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-person-dress"></i> Mother's Name</span>
                                <strong class="prof-val" id="prof-val-mother">Kalyanam Lakshmi</strong>
                            </div>

                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-mobile-screen-button text-primary"></i> Student Mobile Number</span>
                                <strong class="prof-val" id="prof-val-student-phone">+91 98480 12345</strong>
                            </div>
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-phone text-success"></i> Father's Mobile Number</span>
                                <strong class="prof-val" id="prof-val-father-phone">+91 94400 54321</strong>
                            </div>
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-phone text-purple"></i> Mother's Mobile Number</span>
                                <strong class="prof-val" id="prof-val-mother-phone">+91 99890 98765</strong>
                            </div>
                            <div class="prof-detail-box">
                                <span class="prof-label"><i class="fa-solid fa-droplet text-danger"></i> Blood Group & DOB</span>
                                <strong class="prof-val" id="prof-val-blood-dob">O+ve • 14-Aug-2005</strong>
                            </div>

                            <div class="prof-detail-box" style="grid-column: span 2;">
                                <span class="prof-label"><i class="fa-solid fa-envelope-open text-primary"></i> Official College Email</span>
                                <strong class="prof-val" id="prof-val-college-email">25b11cs380@aditya.ac.in</strong>
                            </div>
                            <div class="prof-detail-box" style="grid-column: span 2;">
                                <span class="prof-label"><i class="fa-solid fa-envelope text-warning"></i> Personal Email Address</span>
                                <strong class="prof-val" id="prof-val-personal-email">mukundha.kalyanam@gmail.com</strong>
                            </div>
                            <div class="prof-detail-box" style="grid-column: 1 / -1;">
                                <span class="prof-label"><i class="fa-solid fa-map-location-dot text-danger"></i> Permanent Residential Address</span>
                                <strong class="prof-val" id="prof-val-address">Surampalem, ADB Road, Gandepalli Mandal, Kakinada Dist - 533437, Andhra Pradesh</strong>
                            </div>
                        </div>
                    </div>

                    <!-- Prior Academic Qualifications (SSC & Intermediate) -->
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-award text-warning"></i> Prior Academic Qualifications & Entrance Rank</h3>
                        </div>
                        <div class="grid-2-columns">
                            <!-- 10th Standard / SSC -->
                            <div class="prior-academic-box">
                                <div class="prior-header">
                                    <div class="prior-icon bg-blue"><i class="fa-solid fa-school"></i></div>
                                    <div>
                                        <h4>Secondary School Certificate (SSC / 10th)</h4>
                                        <p id="prof-ssc-board">BSEAP • Passed 2022</p>
                                    </div>
                                </div>
                                <div class="prior-scores-grid mt-3">
                                    <div><small>School Name</small><strong id="prof-ssc-school">Aditya High School</strong></div>
                                    <div><small>Hall Ticket No</small><strong id="prof-ssc-ht">22894105</strong></div>
                                    <div><small>Marks Secured</small><strong id="prof-ssc-marks">580 / 600</strong></div>
                                    <div><small>Percentage & GPA</small><strong id="prof-ssc-pct" class="text-success">96.67% (10.0 GPA)</strong></div>
                                </div>
                            </div>

                            <!-- 12th Standard / Intermediate -->
                            <div class="prior-academic-box">
                                <div class="prior-header">
                                    <div class="prior-icon bg-emerald"><i class="fa-solid fa-building-columns"></i></div>
                                    <div>
                                        <h4>Intermediate Education (12th / +2)</h4>
                                        <p id="prof-inter-board">BIEAP • Passed 2024 • MPC Group</p>
                                    </div>
                                </div>
                                <div class="prior-scores-grid mt-3">
                                    <div><small>Junior College</small><strong id="prof-inter-college">Aditya Junior College</strong></div>
                                    <div><small>EAPCET Merit Rank</small><strong id="prof-inter-rank" style="color:var(--primary-light);">Rank 3,420</strong></div>
                                    <div><small>Marks Secured</small><strong id="prof-inter-marks">982 / 1000</strong></div>
                                    <div><small>Percentage & Class</small><strong id="prof-inter-pct" class="text-success">98.20% (Distinction)</strong></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Multi-Semester Comprehensive Academic Performance Ledger -->
                    <div class="panel-card">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-table-list text-primary"></i> Multi-Semester Academic Performance & Internal/External Ledger</h3>
                                <p class="text-muted" style="font-size:12.5px;">Complete historical examination scores from 1st Semester Mid & Final Exams up to Current Semester</p>
                            </div>
                            <span class="badge badge-success" style="font-size:13px;" id="prof-overall-cgpa-pill">Overall CGPA: 9.27</span>
                        </div>

                        <!-- Semester Tab Selector Pills -->
                        <div class="sem-tabs-bar mb-3" id="prof-sem-tabs-container">
                            <button class="sem-tab-btn active" data-sem="0">Semester 1</button>
                            <button class="sem-tab-btn" data-sem="1">Semester 2</button>
                            <button class="sem-tab-btn" data-sem="2">Semester 3</button>
                            <button class="sem-tab-btn" data-sem="3">Semester 4 (Current)</button>
                        </div>

                        <div class="table-responsive">
                            <table class="data-table" id="prof-semester-marks-table">
                                <thead>
                                    <tr>
                                        <th>Course Code</th>
                                        <th>Subject Name</th>
                                        <th>Credits</th>
                                        <th>Mid-1 (30M)</th>
                                        <th>Mid-2 (30M)</th>
                                        <th>Internal Avg (30M)</th>
                                        <th>External Exam (70M)</th>
                                        <th>Total (100M)</th>
                                        <th>Grade</th>
                                        <th>Grade Points</th>
                                        <th>Result</th>
                                    </tr>
                                </thead>
                                <tbody id="prof-semester-marks-tbody"></tbody>
                            </table>
                        </div>

                        <div class="sem-summary-footer mt-3" id="prof-sem-footer-box">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>
                </section>
"""

# Insert student-profile-tab right before <!-- TAB: Student Timetable -->
if 'id="student-profile-tab"' not in html:
    html = html.replace('<!-- TAB: Student Timetable -->', student_profile_tab_html + '\n                <!-- TAB: Student Timetable -->')
    print("Added student-profile-tab to index.html")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully injected enhanced Attendance Tab & Student Profile Tab into index.html")

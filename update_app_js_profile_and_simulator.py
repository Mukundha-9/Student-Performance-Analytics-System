# update_app_js_profile_and_simulator.py
import re

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update Student Sidebar Navigation
old_student_menu = """    if (role === 'student') {
        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-attendance-tab', icon: 'fa-clipboard-check', label: 'Subject Attendance & Calculator' },
            { id: 'student-notifications-tab', icon: 'fa-bell', label: 'Notifications & Circulars' },
            { id: 'student-timetable-tab', icon: 'fa-calendar-days', label: 'Class Timetable' },
            { id: 'student-faculty-tab', icon: 'fa-chalkboard-user', label: 'Enrolled Faculty & Mentor' },
            { id: 'student-fees-tab', icon: 'fa-credit-card', label: 'Fee Payments & Receipts' },
            { id: 'student-hallticket-tab', icon: 'fa-ticket', label: 'Digital Hall Ticket' },
            { id: 'ai-advisor-tab', icon: 'fa-brain', label: 'AI Study Tutor' },
            { id: 'simulator-tab', icon: 'fa-sliders', label: 'What-If Grade Simulator' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Visual Analytics' },
            { id: 'report-tab', icon: 'fa-file-lines', label: 'Performance Report' }
        ];"""

new_student_menu = """    if (role === 'student') {
        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-profile-tab', icon: 'fa-id-card', label: 'My Official Profile & Ledgers' },
            { id: 'student-attendance-tab', icon: 'fa-clipboard-check', label: 'Subject Attendance & Calculator' },
            { id: 'student-notifications-tab', icon: 'fa-bell', label: 'Notifications & Circulars' },
            { id: 'student-timetable-tab', icon: 'fa-calendar-days', label: 'Class Timetable' },
            { id: 'student-faculty-tab', icon: 'fa-chalkboard-user', label: 'Enrolled Faculty & Mentor' },
            { id: 'student-fees-tab', icon: 'fa-credit-card', label: 'Fee Payments & Receipts' },
            { id: 'student-hallticket-tab', icon: 'fa-ticket', label: 'Digital Hall Ticket' },
            { id: 'ai-advisor-tab', icon: 'fa-brain', label: 'AI Study Tutor' },
            { id: 'simulator-tab', icon: 'fa-sliders', label: 'What-If Grade Simulator' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Visual Analytics' },
            { id: 'report-tab', icon: 'fa-file-lines', label: 'Performance Report' }
        ];"""

if old_student_menu in js:
    js = js.replace(old_student_menu, new_student_menu)
    print("Updated student menu with profile tab.")

# 2. Hook switchTab for Profile
old_switch = "if (tabId === 'student-attendance-tab') loadStudentDetailedAttendance(currentUser.id);"
new_switch = "if (tabId === 'student-attendance-tab') loadStudentDetailedAttendance(currentUser.id);\n    if (tabId === 'student-profile-tab') loadStudentProfile(currentUser.id);"

if old_switch in js:
    js = js.replace(old_switch, new_switch)
    print("Hooked switchTab for student-profile-tab.")

# 3. Add Profile and Attendance Simulator Logic
profile_and_simulator_js = """

// ==============================================================================
// 11. STUDENT OFFICIAL PROFILE & MULTI-SEMESTER LEDGER JS
// ==============================================================================

let cachedStudentProfile = null;

async function loadStudentProfile(studentId) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        const res = await fetch(`/api/student/profile/${sId}`);
        const p = await res.json();
        cachedStudentProfile = p;

        // 1. Hero Info
        document.getElementById('prof-student-name').innerText = p.name;
        document.getElementById('prof-student-meta').innerText = `Roll No: ${p.roll_number} • ${p.branch} • ${p.section}`;
        document.getElementById('prof-academic-year').innerText = p.academic_year;
        document.getElementById('prof-admission-type').innerText = p.admission_category;
        document.getElementById('prof-cgpa-badge').innerText = `Cumulative CGPA: ${p.overall_cgpa} / 10.0`;
        document.getElementById('prof-mentor-badge').innerText = `Proctor: ${p.mentor_name}`;
        document.getElementById('prof-overall-cgpa-pill').innerText = `Overall CGPA: ${p.overall_cgpa} (${p.overall_percentage}%)`;

        // 2. Personal & Contact Details
        document.getElementById('prof-val-name').innerText = p.name;
        document.getElementById('prof-val-roll').innerText = p.roll_number;
        document.getElementById('prof-val-father').innerText = p.father_name;
        document.getElementById('prof-val-mother').innerText = p.mother_name;
        document.getElementById('prof-val-student-phone').innerText = p.student_mobile;
        document.getElementById('prof-val-father-phone').innerText = p.father_mobile;
        document.getElementById('prof-val-mother-phone').innerText = p.mother_mobile;
        document.getElementById('prof-val-blood-dob').innerText = `${p.blood_group} • ${p.dob}`;
        document.getElementById('prof-val-college-email').innerText = p.college_email;
        document.getElementById('prof-val-personal-email').innerText = p.personal_email;
        document.getElementById('prof-val-address').innerText = p.address;

        // 3. Prior Academics
        const ssc = p.prior_academics?.ssc || {};
        document.getElementById('prof-ssc-board').innerText = `${ssc.board} • Passed ${ssc.year_of_passing}`;
        document.getElementById('prof-ssc-school').innerText = ssc.school_name;
        document.getElementById('prof-ssc-ht').innerText = ssc.hall_ticket_no;
        document.getElementById('prof-ssc-marks').innerText = `${ssc.marks_secured} / ${ssc.max_marks}`;
        document.getElementById('prof-ssc-pct').innerText = `${ssc.percentage}% (${ssc.cgpa} GPA)`;

        const inter = p.prior_academics?.intermediate || {};
        document.getElementById('prof-inter-board').innerText = `${inter.board} • Passed ${inter.year_of_passing} • ${inter.group}`;
        document.getElementById('prof-inter-college').innerText = inter.college_name;
        document.getElementById('prof-inter-rank').innerText = inter.eapcet_rank;
        document.getElementById('prof-inter-marks').innerText = `${inter.marks_secured} / ${inter.max_marks}`;
        document.getElementById('prof-inter-pct').innerText = `${inter.percentage}% (${inter.division})`;

        // 4. Multi-Semester Ledger Tabs
        initSemesterLedgerTabs(p.semesters_ledger || []);

    } catch(e) {}
}

function initSemesterLedgerTabs(semesters) {
    const tabsContainer = document.getElementById('prof-sem-tabs-container');
    if (!tabsContainer || semesters.length === 0) return;

    tabsContainer.innerHTML = '';
    semesters.forEach((sem, idx) => {
        const btn = document.createElement('button');
        btn.className = `sem-tab-btn ${idx === semesters.length - 1 ? 'active' : ''}`;
        btn.innerText = sem.semester_title.split(' (')[0];
        btn.onclick = () => {
            document.querySelectorAll('.sem-tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderSemesterMarksTable(sem);
        };
        tabsContainer.appendChild(btn);
    });

    renderSemesterMarksTable(semesters[semesters.length - 1]);
}

function renderSemesterMarksTable(sem) {
    const tbody = document.getElementById('prof-semester-marks-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    (sem.subjects || []).forEach(sub => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><code>${sub.course_code}</code></td>
            <td><strong>${sub.subject_name}</strong></td>
            <td>${sub.credits}</td>
            <td>${sub.mid1_marks} / 30</td>
            <td>${sub.mid2_marks} / 30</td>
            <td><strong style="color:var(--primary-light);">${sub.internal_avg}</strong></td>
            <td><strong style="color:#60a5fa;">${sub.external_marks}</strong></td>
            <td><strong style="color:#34d399; font-size:14px;">${sub.total_marks} / 100</strong></td>
            <td><span class="grade-badge grade-${sub.grade_letter.replace('+', '-plus')}">${sub.grade_letter}</span></td>
            <td><strong>${sub.grade_points}</strong></td>
            <td><span class="badge badge-pass">${sub.status}</span></td>
        `;
        tbody.appendChild(tr);
    });

    const footer = document.getElementById('prof-sem-footer-box');
    if (footer) {
        footer.innerHTML = `
            <div>
                <strong>${sem.semester_title}</strong>
                <span class="text-muted" style="margin-left:8px;">Total Earned Credits: <strong>${sem.total_credits}</strong></span>
            </div>
            <div>
                <span class="badge badge-success" style="font-size:14px; padding:6px 12px;">Semester SGPA: ${sem.sgpa} / 10.0</span>
                <span class="badge badge-pass" style="font-size:13px; margin-left:8px;">Result: PASS (FIRST CLASS WITH DISTINCTION)</span>
            </div>
        `;
    }
}

function printOfficialTranscript() {
    if (!cachedStudentProfile) {
        showToast('Please wait for profile to load...', 'info');
        return;
    }
    const p = cachedStudentProfile;
    const printWin = window.open('', '_blank');
    
    let allSemTables = '';
    (p.semesters_ledger || []).forEach(sem => {
        let rows = '';
        sem.subjects.forEach(s => {
            rows += `<tr>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; font-family:monospace;">${s.course_code}</td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1;"><strong>${s.subject_name}</strong></td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; text-align:center;">${s.credits}</td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; text-align:center;">${s.internal_avg}</td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; text-align:center;">${s.external_marks}</td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; text-align:center;"><strong>${s.total_marks}</strong></td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; text-align:center;"><strong>${s.grade_letter}</strong></td>
                <td style="padding:6px 8px; border:1px solid #cbd5e1; text-align:center; color:#16a34a; font-weight:bold;">${s.status}</td>
            </tr>`;
        });

        allSemTables += `
            <div style="margin-top:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-weight:bold; font-size:13px;">
                    <span>${sem.semester_title}</span>
                    <span>SGPA: ${sem.sgpa} (Credits: ${sem.total_credits})</span>
                </div>
                <table style="width:100%; border-collapse:collapse; font-size:11.5px;">
                    <thead>
                        <tr style="background:#f1f5f9;">
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">Code</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1; text-align:left;">Course Title</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">Credits</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">Internal (30)</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">External (70)</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">Total (100)</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">Grade</th>
                            <th style="padding:6px 8px; border:1px solid #cbd5e1;">Result</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>
        `;
    });

    printWin.document.write(`
        <html><head><title>Consolidated Academic Transcript - ${p.name} (${p.roll_number})</title>
        <style>body{font-family:'Segoe UI',sans-serif; padding:30px; color:#0f172a; max-width:900px; margin:0 auto;}</style>
        </head><body>
        <div style="text-align:center; border-bottom:2px solid #1e3a8a; padding-bottom:12px;">
            <h1 style="color:#1e3a8a; margin:0; font-size:24px;">ADITYA UNIVERSITY</h1>
            <p style="margin:2px 0; font-size:13px; font-weight:bold; color:#475569;">OFFICE OF CONTROLLER OF EXAMINATIONS</p>
            <h3 style="margin:6px 0 0 0; color:#0f172a; font-size:16px;">CONSOLIDATED CUMULATIVE GRADE TRANSCRIPT</h3>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:16px; font-size:12.5px; background:#f8fafc; padding:12px; border-radius:6px; border:1px solid #e2e8f0;">
            <div><strong>Candidate Name:</strong> ${p.name}</div>
            <div><strong>Roll Number:</strong> ${p.roll_number}</div>
            <div><strong>Father's Name:</strong> ${p.father_name}</div>
            <div><strong>Mother's Name:</strong> ${p.mother_name}</div>
            <div><strong>Branch:</strong> ${p.branch}</div>
            <div><strong>Batch / Period:</strong> ${p.academic_year}</div>
            <div><strong>Overall CGPA:</strong> <span style="color:#16a34a; font-weight:bold; font-size:14px;">${p.overall_cgpa} / 10.0</span></div>
            <div><strong>Overall Percentage:</strong> ${p.overall_percentage}% (${p.grade})</div>
        </div>

        ${allSemTables}

        <div style="display:flex; justify-content:space-between; margin-top:40px; font-size:12px;">
            <div><br><strong>Verified by Dean Academic Audit</strong></div>
            <div style="text-align:center;"><br><strong>Official Seal of University</strong></div>
            <div style="text-align:right;"><br><strong>Controller of Examinations</strong></div>
        </div>
        <script>window.print();</script>
        </body></html>
    `);
    printWin.document.close();
}


// ==============================================================================
// 12. INTERACTIVE LIVE BUNK & CATCH-UP SIMULATOR
// ==============================================================================

function initBunkSimulatorEvents() {
    const slider = document.getElementById('bunk-simulator-range');
    if (!slider) return;

    slider.addEventListener('input', (e) => {
        const delta = parseInt(e.target.value);
        updateBunkSimulation(delta);
    });
}

function updateBunkSimulation(delta) {
    if (!cachedAttendanceData) return;
    const baseAttended = cachedAttendanceData.total_attended || 217;
    const baseConducted = cachedAttendanceData.total_conducted || 221;

    let simAttended = baseAttended;
    let simConducted = baseConducted;

    const label = document.getElementById('slider-change-label');
    if (delta < 0) {
        const missed = Math.abs(delta);
        simConducted = baseConducted + missed;
        label.innerText = `Miss ${missed} Period${missed > 1 ? 's' : ''} (Bunk)`;
        label.style.color = '#f87171';
    } else if (delta > 0) {
        simAttended = baseAttended + delta;
        simConducted = baseConducted + delta;
        label.innerText = `Attend +${delta} Period${delta > 1 ? 's' : ''} Consecutively`;
        label.style.color = '#34d399';
    } else {
        label.innerText = 'Current Standing (0 Periods)';
        label.style.color = 'var(--primary-light)';
    }

    const simPct = Math.min(100.0, Math.max(0.0, ((simAttended / simConducted) * 100.0))).toFixed(1);
    
    const pctDisplay = document.getElementById('sim-projected-pct');
    const badgeDisplay = document.getElementById('sim-status-badge');

    if (pctDisplay) {
        pctDisplay.innerText = `${simPct}%`;
        if (parseFloat(simPct) >= 75.0) {
            pctDisplay.style.color = '#10b981';
            badgeDisplay.className = 'badge badge-success';
            badgeDisplay.innerHTML = '<i class="fa-solid fa-circle-check"></i> Eligible for Semester Examinations';
        } else {
            pctDisplay.style.color = '#ef4444';
            badgeDisplay.className = 'badge badge-danger';
            badgeDisplay.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Warning: Exam Detention Risk (< 75.0%)';
        }
    }
}

function resetBunkSlider() {
    const slider = document.getElementById('bunk-simulator-range');
    if (slider) {
        slider.value = 0;
        updateBunkSimulation(0);
    }
}
"""

js += profile_and_simulator_js

# Hook initBunkSimulatorEvents
js = js.replace("initStudentBookingEvents();", "initStudentBookingEvents();\n    initBunkSimulatorEvents();")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Successfully injected Student Profile and Bunk Simulator logic into static/js/app.js")

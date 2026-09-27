# update_app_js_attendance_and_meetings.py
import re

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update Student Sidebar Navigation
old_student_menu = """    if (role === 'student') {
        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
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
    print("Updated student menu with attendance tab.")

# 2. Hook switchTab for Attendance
old_switch = "if (tabId === 'student-notifications-tab') loadStudentNotifications(currentUser.id);"
new_switch = "if (tabId === 'student-notifications-tab') loadStudentNotifications(currentUser.id);\n    if (tabId === 'student-attendance-tab') loadStudentDetailedAttendance(currentUser.id);"

if old_switch in js:
    js = js.replace(old_switch, new_switch)
    print("Hooked switchTab for student-attendance-tab.")

# 3. Update Proctor Hero Card button to open booking modal
old_btn = "onclick=\"showToast('Mentorship meeting request sent to ' + '${p.name}', 'success')\"><i class=\"fa-solid fa-calendar-check\"></i> Book Meeting"
new_btn = "onclick=\"openModal('modal-request-meeting')\"><i class=\"fa-solid fa-calendar-plus\"></i> Request 1-on-1 Meeting"
if old_btn in js:
    js = js.replace(old_btn, new_btn)
    print("Updated proctor card button to open modal.")

# 4. Add Attendance Logic & Meeting Workflow Functions
attendance_and_booking_js = """

// ==============================================================================
// 9. STUDENT DETAILED SUBJECT ATTENDANCE & PERIOD LOGS JS
// ==============================================================================

let cachedAttendanceData = null;

async function loadStudentDetailedAttendance(studentId) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        const res = await fetch(`/api/student/detailed-attendance/${sId}`);
        const data = await res.json();
        cachedAttendanceData = data;

        // 1. Overall Stats
        const pctEl = document.getElementById('att-overall-pct');
        if (pctEl) pctEl.innerText = `${data.overall_percentage}%`;

        const statusEl = document.getElementById('att-overall-status');
        if (statusEl) {
            if (data.is_overall_eligible) {
                statusEl.className = 'text-success';
                statusEl.innerHTML = '<i class="fa-solid fa-circle-check"></i> Eligible for Exams (>=75.0%)';
            } else {
                statusEl.className = 'text-danger';
                statusEl.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Exam Detention Risk (<75.0%)';
            }
        }

        const countEl = document.getElementById('att-total-counts');
        if (countEl) countEl.innerText = `${data.total_attended} / ${data.total_conducted}`;

        const absEl = document.getElementById('att-absent-count');
        if (absEl) absEl.innerText = `${data.total_absent} Classes Absent`;

        const marginStat = document.getElementById('att-margin-stat');
        const marginDesc = document.getElementById('att-margin-desc');
        if (marginStat && marginDesc) {
            if (data.is_overall_eligible) {
                const safeCount = Math.floor((data.total_attended - 0.75 * data.total_conducted) / 0.75);
                marginStat.innerText = `${safeCount} Classes`;
                marginStat.style.color = '#10b981';
                marginDesc.innerText = 'Safe Missable Allowance';
                marginDesc.className = 'text-success';
            } else {
                const recCount = Math.ceil((0.75 * data.total_conducted - data.total_attended) / 0.25);
                marginStat.innerText = `${recCount} Classes`;
                marginStat.style.color = '#ef4444';
                marginDesc.innerText = 'Must Attend Consecutively';
                marginDesc.className = 'text-danger';
            }
        }

        const recentAbsCount = document.getElementById('att-recent-absences-count');
        if (recentAbsCount) {
            recentAbsCount.innerText = `${(data.absence_alerts || []).length} Periods`;
        }

        // 2. Subject Cards Grid with 75% Marker
        const cardsContainer = document.getElementById('student-subject-attendance-cards');
        if (cardsContainer && data.subjects) {
            cardsContainer.innerHTML = '';
            data.subjects.forEach(sub => {
                const card = document.createElement('div');
                card.className = 'subject-att-card';
                card.innerHTML = `
                    <div class="subject-att-header">
                        <div>
                            <h4>${sub.subject_name}</h4>
                            <div class="subject-att-faculty"><i class="fa-solid fa-chalkboard-user"></i> ${sub.faculty}</div>
                        </div>
                        <span class="badge ${sub.status_class}">${sub.status_tag}</span>
                    </div>

                    <div class="subject-att-pct-display">
                        <h3 style="color:${sub.is_eligible ? '#10b981' : '#ef4444'};">${sub.percentage}%</h3>
                        <span>(${sub.attended} Attended / ${sub.conducted} Total)</span>
                    </div>

                    <!-- 75% Rule Progress Bar -->
                    <div class="att-progress-container">
                        <div class="att-progress-track">
                            <div class="att-progress-fill ${sub.is_eligible ? 'fill-safe' : 'fill-risk'}" style="width: ${Math.min(100, sub.percentage)}%;"></div>
                            <div class="att-75-marker"></div>
                        </div>
                        <div class="att-75-marker-label">75% Min</div>
                    </div>

                    <div class="att-calculator-tag ${sub.is_eligible ? 'tag-safe' : 'tag-risk'}">
                        <i class="fa-solid ${sub.is_eligible ? 'fa-circle-check' : 'fa-triangle-exclamation'}"></i>
                        <span>${sub.calc_message}</span>
                    </div>
                `;
                cardsContainer.appendChild(card);
            });
        }

        // 3. Render Period Diary Day Selector & Diary Table
        renderPeriodDiaryDays(data.daily_period_logs || []);

        // 4. Render Absence Alerts Feed
        const alertsContainer = document.getElementById('student-absence-alerts-list');
        if (alertsContainer) {
            alertsContainer.innerHTML = '';
            const alerts = data.absence_alerts || [];
            if (alerts.length === 0) {
                alertsContainer.innerHTML = '<div class="text-center text-muted p-4"><i class="fa-solid fa-circle-check text-success" style="font-size:24px;"></i><p class="mt-2">No period absences recorded in recent days. 100% Attendance!</p></div>';
            } else {
                alerts.forEach(al => {
                    const item = document.createElement('div');
                    item.className = 'absence-alert-card';
                    item.innerHTML = `
                        <h5><i class="fa-solid fa-triangle-exclamation"></i> ${al.subject} • ${al.period}</h5>
                        <p style="font-size:12px; color:var(--text-primary);">${al.alert_text}</p>
                        <div class="absence-alert-meta">
                            <span><i class="fa-solid fa-calendar"></i> ${al.date} (${al.day})</span>
                            <span><i class="fa-solid fa-door-open"></i> ${al.room}</span>
                        </div>
                    `;
                    alertsContainer.appendChild(item);
                });
            }
        }

    } catch(e) {}
}

function renderPeriodDiaryDays(dailyLogs) {
    const btnContainer = document.getElementById('att-day-selector-btns');
    if (!btnContainer || dailyLogs.length === 0) return;

    btnContainer.innerHTML = '';
    dailyLogs.forEach((dayLog, idx) => {
        const btn = document.createElement('button');
        btn.className = `att-day-btn ${idx === 0 ? 'active' : ''}`;
        btn.innerText = dayLog.date_label.split(' (')[0];
        btn.onclick = () => {
            document.querySelectorAll('.att-day-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderPeriodDiaryTable(dayLog.periods);
        };
        btnContainer.appendChild(btn);
    });

    renderPeriodDiaryTable(dailyLogs[0].periods);
}

function renderPeriodDiaryTable(periods) {
    const tbody = document.getElementById('att-period-diary-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    periods.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>Period ${p.period}</strong><br><small style="color:var(--text-muted);"><i class="fa-solid fa-clock"></i> ${p.time}</small></td>
            <td><strong>${p.subject}</strong></td>
            <td>${p.faculty}<br><small style="color:var(--text-muted);"><i class="fa-solid fa-location-dot"></i> ${p.room}</small></td>
            <td><span class="badge ${p.badge_class}"><i class="fa-solid ${p.status === 'Present' ? 'fa-circle-check' : 'fa-circle-xmark'}"></i> ${p.status}</span></td>
        `;
        tbody.appendChild(tr);
    });
}


// ==============================================================================
// 10. STUDENT MEETING BOOKING & FACULTY APPROVAL LOGIC
// ==============================================================================

function initStudentBookingEvents() {
    document.getElementById('student-book-meeting-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            student_id: currentUser?.id || '25B11CS380',
            faculty_id: '50101',
            date: document.getElementById('book-meet-date').value,
            time_slot: document.getElementById('book-meet-slot').value,
            purpose: document.getElementById('book-meet-purpose').value,
            notes: document.getElementById('book-meet-notes').value
        };

        try {
            const res = await fetch('/api/student/request-meeting', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            showToast(data.message, 'success');
            closeModal('modal-request-meeting');
            document.getElementById('student-book-meeting-form').reset();
            loadStudentProctorDesk(currentUser?.id);
            loadStudentNotifications(currentUser?.id);
        } catch(e) {
            showToast('Error booking meeting request', 'error');
        }
    });
}

// Faculty load pending student meeting requests
async function loadFacultyPendingMeetings(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/proctor/meetings/${fId}`);
        const data = await res.json();
        const allMeetings = data.meetings || [];

        const pendingList = allMeetings.filter(m => m.status === 'Pending Faculty Approval');
        const confirmedList = allMeetings.filter(m => m.status !== 'Pending Faculty Approval');

        const badge = document.getElementById('pending-meet-badge');
        if (badge) badge.innerText = `${pendingList.length} Pending Approval`;

        const pendingTbody = document.getElementById('faculty-pending-meetings-tbody');
        if (pendingTbody) {
            pendingTbody.innerHTML = '';
            if (pendingList.length === 0) {
                pendingTbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted p-3">No pending meeting requests from mentees at this time.</td></tr>';
            } else {
                pendingList.forEach(m => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${m.student_name}</strong><br><code>${m.student_id}</code></td>
                        <td><strong>${m.date}</strong><br><small style="color:var(--text-muted);">${m.time_slot}</small></td>
                        <td><strong>${m.purpose}</strong></td>
                        <td style="font-size:11.5px; color:var(--text-secondary); max-width:200px;">${m.notes || 'No specific notes.'}</td>
                        <td>
                            <div style="display:flex; gap:6px;">
                                <button class="btn btn-sm btn-primary" onclick="facultyRespondMeeting('${m.meeting_id}', 'accept')">
                                    <i class="fa-solid fa-check"></i> Accept & Confirm Slot
                                </button>
                                <button class="btn btn-sm btn-outline" onclick="facultyRespondMeeting('${m.meeting_id}', 'decline')">
                                    <i class="fa-solid fa-xmark"></i> Decline
                                </button>
                            </div>
                        </td>
                    `;
                    pendingTbody.appendChild(tr);
                });
            }
        }

        // Render Confirmed Meetings Table
        const confirmedTbody = document.getElementById('proctor-meetings-table')?.querySelector('tbody');
        if (confirmedTbody) {
            confirmedTbody.innerHTML = '';
            confirmedList.forEach(m => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${m.student_name}</strong><br><code>${m.student_id}</code></td>
                    <td><i class="fa-solid fa-calendar text-primary"></i> ${m.date}<br><small><i class="fa-solid fa-clock text-warning"></i> ${m.time_slot}</small></td>
                    <td><strong>${m.purpose}</strong><br><small style="color:var(--text-muted);"><i class="fa-solid fa-location-dot"></i> ${m.venue}</small></td>
                    <td><span class="badge ${m.status.includes('Confirmed') ? 'badge-success' : 'badge-danger'}">${m.status}</span></td>
                `;
                confirmedTbody.appendChild(tr);
            });
        }

    } catch(e) {}
}

async function facultyRespondMeeting(meetingId, action) {
    const fId = currentUser?.id || '50101';
    let confirmedSlot = null;
    let venue = 'Ramanujan Block - Room 402 (Faculty Cabin)';

    if (action === 'accept') {
        confirmedSlot = prompt("Confirm / Adjust Meeting Time Slot for Student:", "03:30 PM - 04:00 PM");
        if (confirmedSlot === null) return;
    }

    try {
        const res = await fetch('/api/faculty/respond-meeting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                faculty_id: fId,
                meeting_id: meetingId,
                action: action,
                confirmed_time: confirmedSlot || '03:30 PM - 04:00 PM',
                venue: venue,
                remarks: action === 'accept' ? 'Slot confirmed by faculty mentor.' : 'Declined due to academic scheduling conflict.'
            })
        });
        const data = await res.json();
        showToast(data.message, 'success');
        loadFacultyPendingMeetings(fId);
    } catch(e) {
        showToast('Error responding to meeting', 'error');
    }
}
"""

js += attendance_and_booking_js

# Hook initStudentBookingEvents
js = js.replace("initNotificationFilterEvents();", "initNotificationFilterEvents();\n    initStudentBookingEvents();")

# Hook faculty proctor meeting loader to also load pending requests
js = js.replace("loadFacultyProctorMeetings(facId);", "loadFacultyProctorMeetings(facId);\n    loadFacultyPendingMeetings(facId);")
js = js.replace("loadFacultyProctorMeetings(facultyId);", "loadFacultyProctorMeetings(facultyId);\n    loadFacultyPendingMeetings(facultyId);")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Successfully injected Subject Attendance & Meeting Booking logic into static/js/app.js")

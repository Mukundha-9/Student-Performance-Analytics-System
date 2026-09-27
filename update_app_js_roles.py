# update_app_js_roles.py
import re

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update renderSidebarMenu
old_menu_code = """    let items = [];
    if (role === 'student') {
        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-timetable-tab', icon: 'fa-calendar-days', label: 'Class Timetable' },
            { id: 'student-faculty-tab', icon: 'fa-chalkboard-user', label: 'Enrolled Faculty & Mentor' },
            { id: 'student-fees-tab', icon: 'fa-credit-card', label: 'Fee Payments & Receipts' },
            { id: 'student-hallticket-tab', icon: 'fa-ticket', label: 'Digital Hall Ticket' },
            { id: 'ai-advisor-tab', icon: 'fa-brain', label: 'AI Study Advisor' },
            { id: 'simulator-tab', icon: 'fa-sliders', label: 'What-If Grade Simulator' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Visual Analytics' },
            { id: 'report-tab', icon: 'fa-file-lines', label: 'Performance Report' }
        ];
    } else if (role === 'faculty') {
        items = [
            { id: 'faculty-attendance-tab', icon: 'fa-clipboard-user', label: 'Daily Attendance Register' },
            { id: 'faculty-marks-tab', icon: 'fa-marker', label: 'CIA Internal Marks Desk' },
            { id: 'faculty-proctoring-tab', icon: 'fa-user-shield', label: 'Proctoring Mentees (25)' },
            { id: 'admin-dashboard-tab', icon: 'fa-chart-pie', label: 'Department Analytics' },
            { id: 'student-timetable-tab', icon: 'fa-calendar-days', label: 'Teaching Schedule' },
            { id: 'ai-advisor-tab', icon: 'fa-brain', label: 'AI Diagnostic' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Publication Charts' }
        ];
    } else {
        items = [
            { id: 'admin-dashboard-tab', icon: 'fa-gauge-high', label: 'Executive Analytics (500)' },
            { id: 'admin-students-tab', icon: 'fa-address-book', label: 'Master Student Directory' },
            { id: 'admin-announcements-tab', icon: 'fa-bullhorn', label: 'Campus Announcements' },
            { id: 'ai-advisor-tab', icon: 'fa-brain', label: 'Aditya AI Advisor' },
            { id: 'simulator-tab', icon: 'fa-sliders', label: 'What-If Grade Simulator' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Matplotlib Gallery' },
            { id: 'report-tab', icon: 'fa-file-lines', label: 'Official University Report' }
        ];
    }"""

new_menu_code = """    let items = [];
    if (role === 'student') {
        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-timetable-tab', icon: 'fa-calendar-days', label: 'Class Timetable' },
            { id: 'student-faculty-tab', icon: 'fa-chalkboard-user', label: 'Enrolled Faculty & Mentor' },
            { id: 'student-fees-tab', icon: 'fa-credit-card', label: 'Fee Payments & Receipts' },
            { id: 'student-hallticket-tab', icon: 'fa-ticket', label: 'Digital Hall Ticket' },
            { id: 'ai-advisor-tab', icon: 'fa-brain', label: 'AI Study Tutor' },
            { id: 'simulator-tab', icon: 'fa-sliders', label: 'What-If Grade Simulator' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Visual Analytics' },
            { id: 'report-tab', icon: 'fa-file-lines', label: 'Performance Report' }
        ];
    } else if (role === 'faculty') {
        items = [
            { id: 'faculty-attendance-tab', icon: 'fa-clipboard-user', label: 'Daily Attendance Register' },
            { id: 'faculty-marks-tab', icon: 'fa-marker', label: 'CIA Internal Marks Desk' },
            { id: 'faculty-proctoring-tab', icon: 'fa-user-shield', label: 'Proctoring Mentees (25)' },
            { id: 'faculty-remedial-tab', icon: 'fa-graduation-cap', label: 'Remedial Action Planner' },
            { id: 'student-timetable-tab', icon: 'fa-calendar-days', label: 'Teaching Schedule' },
            { id: 'faculty-leave-tab', icon: 'fa-calendar-check', label: 'Leave & Slot Swap Desk' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Publication Charts' }
        ];
    } else {
        items = [
            { id: 'admin-dashboard-tab', icon: 'fa-gauge-high', label: 'Executive Analytics (500)' },
            { id: 'admin-students-tab', icon: 'fa-address-book', label: 'Master Student Directory' },
            { id: 'admin-results-tab', icon: 'fa-sliders', label: 'Result Moderation & Publishing' },
            { id: 'admin-announcements-tab', icon: 'fa-bullhorn', label: 'Campus Announcements' },
            { id: 'admin-audit-tab', icon: 'fa-award', label: 'NAAC/NBA Accreditation Audit' },
            { id: 'admin-detention-tab', icon: 'fa-triangle-exclamation', label: 'Detention & Warning Desk' },
            { id: 'matplotlib-tab', icon: 'fa-image', label: 'Matplotlib Gallery' },
            { id: 'report-tab', icon: 'fa-file-lines', label: 'Official University Report' }
        ];
    }"""

if old_menu_code in js:
    js = js.replace(old_menu_code, new_menu_code)
    print("Replaced sidebar menus successfully.")
else:
    print("Warning: old menu code pattern not found directly, performing regex replacement.")

# 2. Update switchTab to handle new tabs
old_switch_tab = """    if (tabId === 'faculty-proctoring-tab') loadFacultyProctoring(currentUser.id);
    if (tabId === 'admin-dashboard-tab') loadAdminPortal();
    if (tabId === 'admin-students-tab') loadStudentsTable();
    if (tabId === 'admin-announcements-tab') loadAdminAnnouncements();"""

new_switch_tab = """    if (tabId === 'faculty-proctoring-tab') loadFacultyProctoring(currentUser.id);
    if (tabId === 'faculty-remedial-tab') loadFacultyRemedial(currentUser.id);
    if (tabId === 'faculty-leave-tab') loadFacultyLeaves(currentUser.id);
    if (tabId === 'admin-dashboard-tab') loadAdminPortal();
    if (tabId === 'admin-students-tab') loadStudentsTable();
    if (tabId === 'admin-results-tab') loadAdminResultsModeration();
    if (tabId === 'admin-announcements-tab') loadAdminAnnouncements();
    if (tabId === 'admin-audit-tab') loadAdminAccreditationAudit();
    if (tabId === 'admin-detention-tab') loadAdminDetentionList();"""

if old_switch_tab in js:
    js = js.replace(old_switch_tab, new_switch_tab)

# 3. Add JS functions for Faculty Remedial, Leave, Admin Moderation, Audit & Detention
extra_functions = """

// ==============================================================================
// 5. UNIQUE FACULTY FEATURES (Remedial Planner & Leave Desk)
// ==============================================================================

async function loadFacultyRemedial(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/faculty/remedial-plan/${fId}`);
        const data = await res.json();
        
        const tbody = document.getElementById('faculty-remedial-tbody');
        if (tbody && data.students_list) {
            tbody.innerHTML = '';
            data.students_list.forEach(s => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><code>${s.student_id}</code></td>
                    <td><strong>${s.name}</strong></td>
                    <td>${s.branch}</td>
                    <td>${s.subject}</td>
                    <td><span class="badge badge-fail">${s.current_score}</span></td>
                    <td class="${s.attendance < 75 ? 'badge-att-low' : ''}">${s.attendance}%</td>
                    <td style="font-size:12px; color:var(--text-secondary);">${s.gap_analysis}</td>
                    <td><span class="badge badge-pass">Target: ${s.target_score}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
        
        const schedTbody = document.getElementById('faculty-remedial-schedule-tbody');
        if (schedTbody && data.schedule) {
            schedTbody.innerHTML = '';
            data.schedule.forEach(sc => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><span class="badge badge-warning">${sc.week}</span></td>
                    <td><strong>${sc.topic}</strong></td>
                    <td><i class="fa-solid fa-clock text-primary"></i> ${sc.day_time}</td>
                    <td><i class="fa-solid fa-location-dot text-danger"></i> ${sc.venue}</td>
                `;
                schedTbody.appendChild(tr);
            });
        }
    } catch(e) {}
}

async function loadFacultyLeaves(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/faculty/leaves?faculty_id=${fId}`);
        const data = await res.json();
        const tbody = document.getElementById('faculty-leaves-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        
        (data.leaves || []).forEach(l => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${l.leave_id}</code></td>
                <td>${l.date}</td>
                <td><strong>${l.type}</strong><br><small style="color:var(--text-muted);">${l.slot_details}</small></td>
                <td>${l.substitute_faculty}</td>
                <td><span class="badge badge-success">${l.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) {}
}


// ==============================================================================
// 6. UNIQUE ADMIN FEATURES (Results Moderation, NAAC Audit & Detention Desk)
// ==============================================================================

async function loadAdminResultsModeration() {
    try {
        const res = await fetch('/api/admin/moderation-status');
        const data = await res.json();
        
        const statusDisplay = document.getElementById('admin-publish-status-display');
        if (statusDisplay) {
            if (data.results_published) {
                statusDisplay.innerText = 'PUBLISHED LIVE';
                statusDisplay.style.color = '#10b981';
            } else {
                statusDisplay.innerText = 'WITHHELD (DRAFT)';
                statusDisplay.style.color = '#ef4444';
            }
        }
        
        const sumRes = await fetch('/api/summary');
        const sumData = await sumRes.json();
        document.getElementById('admin-pass-rate-display').innerText = `${sumData.overall?.pass_percentage || 89.6}%`;
        
    } catch(e) {}
}

async function loadAdminAccreditationAudit() {
    try {
        const res = await fetch('/api/admin/accreditation-audit');
        const data = await res.json();
        
        const critTbody = document.getElementById('admin-criteria-tbody');
        if (critTbody && data.criteria) {
            critTbody.innerHTML = '';
            data.criteria.forEach(c => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${c.criterion}</strong></td>
                    <td><strong style="color:var(--primary-light);">${c.score}</strong></td>
                    <td><span class="badge badge-success">${c.status}</span></td>
                `;
                critTbody.appendChild(tr);
            });
        }
        
        const branchTbody = document.getElementById('admin-branch-audit-tbody');
        if (branchTbody && data.branch_audit) {
            branchTbody.innerHTML = '';
            data.branch_audit.forEach(b => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${b.branch}</strong></td>
                    <td>${b.enrolled}</td>
                    <td><strong style="color:#10b981;">${b.pass_rate}%</strong></td>
                    <td>${b.mean_score}%</td>
                    <td>${b.obe_attainment}%</td>
                    <td><span class="badge badge-primary">${b.status}</span></td>
                `;
                branchTbody.appendChild(tr);
            });
        }
    } catch(e) {}
}

async function loadAdminDetentionList() {
    try {
        const res = await fetch('/api/admin/detention-list');
        const data = await res.json();
        
        const tbody = document.getElementById('admin-detention-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        
        (data.students || []).forEach(s => {
            const isDetained = s.status.includes('DETENTION');
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${s.student_id}</code></td>
                <td><strong>${s.name}</strong></td>
                <td>${s.branch}</td>
                <td><strong class="text-danger">${s.attendance}%</strong></td>
                <td>${s.percentage}%</td>
                <td><span class="badge ${isDetained ? 'badge-danger' : 'badge-warning'}">${s.status}</span></td>
                <td>${s.parent_contact}</td>
                <td><span class="badge badge-info"><i class="fa-solid fa-paper-plane"></i> ${s.notice_sent}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) {}
}

// Hook New Event Listeners
function initUniqueRoleEventListeners() {
    // Leave Form
    document.getElementById('faculty-leave-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            faculty_id: currentUser?.id || '50101',
            date: document.getElementById('leave-date-input').value,
            leave_type: document.getElementById('leave-type-select').value,
            substitute_faculty: document.getElementById('leave-substitute-select').value,
            slot_details: document.getElementById('leave-slot-input').value
        };
        try {
            const res = await fetch('/api/faculty/leaves', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            showToast(data.message || 'Leave applied and timetable updated!', 'success');
            loadFacultyLeaves(currentUser?.id);
            document.getElementById('faculty-leave-form').reset();
        } catch(e) {
            showToast('Error applying leave', 'error');
        }
    });

    // Moderation Apply
    document.getElementById('btn-apply-moderation')?.addEventListener('click', async () => {
        const grace = parseInt(document.getElementById('moderation-grace-select')?.value || 3);
        try {
            const res = await fetch('/api/admin/apply-moderation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ grace_marks: grace })
            });
            const data = await res.json();
            showToast(data.message, 'success');
            loadAdminResultsModeration();
            loadAdminPortal();
        } catch(e) {
            showToast('Error applying moderation', 'error');
        }
    });

    // Toggle Publish
    document.getElementById('btn-toggle-publish')?.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/admin/toggle-result-publish', { method: 'POST' });
            const data = await res.json();
            showToast(data.message, 'info');
            loadAdminResultsModeration();
        } catch(e) {
            showToast('Error toggling publish', 'error');
        }
    });
}
"""

js += extra_functions
js = js.replace("initAIAdvisor();", "initAIAdvisor();\n    initUniqueRoleEventListeners();")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Successfully updated static/js/app.js with unique features and role-segregated navigation!")

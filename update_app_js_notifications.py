# update_app_js_notifications.py
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update Student Sidebar Items
old_student_menu = """    if (role === 'student') {
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
        ];"""

new_student_menu = """    if (role === 'student') {
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

if old_student_menu in js:
    js = js.replace(old_student_menu, new_student_menu)
    print("Updated student sidebar menu.")

# 2. Hook switchTab
old_switch = "if (tabId === 'student-faculty-tab') loadStudentFaculties(currentUser.id);"
new_switch = "if (tabId === 'student-faculty-tab') loadStudentFaculties(currentUser.id);\n    if (tabId === 'student-notifications-tab') loadStudentNotifications(currentUser.id);"

if old_switch in js:
    js = js.replace(old_switch, new_switch)
    print("Hooked switchTab for student notifications.")

# 3. Add Student Notifications JavaScript Logic
notif_logic = """

// ==============================================================================
// 8. UNIFIED STUDENT NOTIFICATIONS & CIRCULARS HUB
// ==============================================================================

let cachedStudentNotifs = [];

async function loadStudentNotifications(studentId) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        const [annRes, taskRes, meetRes] = await Promise.all([
            fetch('/api/announcements'),
            fetch(`/api/student/proctor-tasks/${sId}`),
            fetch(`/api/student/proctor-meetings/${sId}`)
        ]);

        const annData = await annRes.json();
        const taskData = await taskRes.json();
        const meetData = await meetRes.json();

        let allNotifs = [];

        // 1. Admin Announcements & Circulars
        (annData.announcements || []).forEach(a => {
            allNotifs.push({
                id: a.id,
                type: 'admin',
                badge: a.category || 'Official Circular',
                badgeClass: a.category === 'Exam' ? 'badge-primary' : (a.category === 'Urgent' ? 'badge-danger' : 'badge-info'),
                issuer: '<i class="fa-solid fa-landmark text-primary"></i> University Administration',
                title: a.title,
                body: a.content,
                date: a.date,
                is_completed: true,
                borderClass: 'border-admin',
                actionable: false
            });
        });

        // 2. Faculty Proctor Assigned Forms & Tasks
        (taskData.tasks || []).forEach(t => {
            allNotifs.push({
                id: t.task_id,
                type: 'proctor-task',
                badge: t.category,
                badgeClass: t.is_completed ? 'badge-success' : 'badge-warning',
                issuer: '<i class="fa-solid fa-user-shield text-warning"></i> Faculty Proctor (Dr. A. K. Sharma)',
                title: t.title,
                body: t.description,
                date: `Deadline: ${t.deadline}`,
                is_completed: t.is_completed,
                borderClass: t.is_completed ? 'border-task completed' : 'border-task',
                actionable: !t.is_completed,
                task_id: t.task_id
            });
        });

        // 3. Proctor Scheduled Meetings
        (meetData.meetings || []).forEach(m => {
            allNotifs.push({
                id: m.meeting_id,
                type: 'proctor-meeting',
                badge: '1-on-1 Proctor Meeting',
                badgeClass: 'badge-purple',
                issuer: '<i class="fa-solid fa-calendar-check text-purple"></i> Faculty Proctor Desk',
                title: `Scheduled Meeting: ${m.purpose}`,
                body: `Venue: <strong>${m.venue}</strong>. Scheduled on <strong>${m.date}</strong> (${m.time_slot}). Status: <span class="badge badge-success">${m.status}</span>`,
                date: `${m.date} (${m.time_slot})`,
                is_completed: true,
                borderClass: 'border-meeting',
                actionable: false
            });
        });

        cachedStudentNotifs = allNotifs;

        // Update counts
        const countAll = allNotifs.length;
        const countAdmin = allNotifs.filter(n => n.type === 'admin').length;
        const countProctor = allNotifs.filter(n => n.type === 'proctor-task').length;
        const countMeeting = allNotifs.filter(n => n.type === 'proctor-meeting').length;

        if (document.getElementById('notif-count-all')) document.getElementById('notif-count-all').innerText = countAll;
        if (document.getElementById('notif-count-admin')) document.getElementById('notif-count-admin').innerText = countAdmin;
        if (document.getElementById('notif-count-proctor')) document.getElementById('notif-count-proctor').innerText = countProctor;
        if (document.getElementById('notif-count-meeting')) document.getElementById('notif-count-meeting').innerText = countMeeting;

        renderFilteredNotifications('all');

    } catch(e) {}
}

function renderFilteredNotifications(filter) {
    const container = document.getElementById('student-notifications-stream');
    if (!container) return;
    container.innerHTML = '';

    const list = filter === 'all' ? cachedStudentNotifs : cachedStudentNotifs.filter(n => n.type === filter);

    if (list.length === 0) {
        container.innerHTML = '<div class="text-center text-muted p-4">No notifications in this category.</div>';
        return;
    }

    list.forEach(n => {
        const card = document.createElement('div');
        card.className = `notif-stream-card ${n.borderClass}`;
        card.innerHTML = `
            <div class="notif-card-header">
                <h4>${n.title}</h4>
                <div class="notif-card-meta">
                    <span class="badge ${n.badgeClass}">${n.badge}</span>
                    <span><i class="fa-solid fa-clock"></i> ${n.date}</span>
                </div>
            </div>
            <div class="notif-card-body">${n.body}</div>
            <div class="notif-card-footer">
                <div style="font-size:12px; color:var(--text-secondary);">${n.issuer}</div>
                <div>
                    ${n.actionable ? `
                        <button class="btn btn-sm btn-primary" onclick="submitNotificationTask('${n.task_id}', '${n.title}')">
                            <i class="fa-solid fa-check-to-slot"></i> Complete & Submit Form
                        </button>
                    ` : (n.type === 'proctor-task' ? '<span class="badge badge-success"><i class="fa-solid fa-circle-check"></i> Form Submitted</span>' : '')}
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

async function submitNotificationTask(taskId, taskTitle) {
    await submitStudentProctorTask(taskId, taskTitle);
    loadStudentNotifications(currentUser?.id);
}

function initNotificationFilterEvents() {
    document.querySelectorAll('.notif-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.notif-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.getAttribute('data-filter');
            renderFilteredNotifications(filter);
        });
    });
}
"""

js += notif_logic

# Hook initNotificationFilterEvents
js = js.replace("initProctorFormEvents();", "initProctorFormEvents();\n    initNotificationFilterEvents();")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Successfully updated static/js/app.js with complete Student Notifications Hub!")

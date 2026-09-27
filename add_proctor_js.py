# add_proctor_js.py
import re

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

proctor_js = """

// ==============================================================================
// 7. COMPREHENSIVE PROCTORING & TASK COMPLIANCE SYSTEM JS
// ==============================================================================

function initProctorSubNavigation() {
    document.querySelectorAll('.proctor-sub-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.proctor-sub-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.proctor-sub-view').forEach(v => {
                v.classList.remove('active');
                v.style.display = 'none';
            });

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            const targetView = document.getElementById(targetId);
            if (targetView) {
                targetView.classList.add('active');
                targetView.style.display = 'block';
            }

            const facId = currentUser?.id || '50101';
            if (targetId === 'proctor-meetings-view') loadFacultyProctorMeetings(facId);
            if (targetId === 'proctor-tasks-view') loadFacultyProctorTasks(facId);
            if (targetId === 'proctor-ptm-view') loadFacultyParentInteractions(facId);
        });
    });
}

// 1. Load Proctor Locked Meetings
async function loadFacultyProctorMeetings(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/proctor/meetings/${fId}`);
        const data = await res.json();
        const tbody = document.getElementById('proctor-meetings-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        (data.meetings || []).forEach(m => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${m.student_name}</strong><br><code>${m.student_id}</code></td>
                <td><i class="fa-solid fa-calendar text-primary"></i> ${m.date}<br><small><i class="fa-solid fa-clock text-warning"></i> ${m.time_slot}</small></td>
                <td><strong>${m.purpose}</strong><br><small style="color:var(--text-muted);"><i class="fa-solid fa-location-dot"></i> ${m.venue}</small></td>
                <td><span class="badge badge-success"><i class="fa-solid fa-lock"></i> ${m.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) {}
}

// 2. Load Proctor Tasks & Forms Compliance Tracker
async function loadFacultyProctorTasks(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/proctor/tasks/${fId}`);
        const data = await res.json();
        const container = document.getElementById('proctor-tasks-tracking-container');
        if (!container) return;
        container.innerHTML = '';

        (data.tasks || []).forEach(t => {
            let doneChips = t.completed_students.map(s => `<span class="mentee-chip-done"><i class="fa-solid fa-check"></i> ${s.name} (${s.student_id})</span>`).join('');
            if (!doneChips) doneChips = '<span class="text-muted" style="font-size:11.5px;">No submissions yet.</span>';

            let pendingChips = t.pending_students.map(s => `<span class="mentee-chip-pending"><i class="fa-solid fa-clock"></i> ${s.name} (${s.student_id})</span>`).join('');
            if (!pendingChips) pendingChips = '<span class="text-success" style="font-size:11.5px;"><i class="fa-solid fa-circle-check"></i> 100% Completed!</span>';

            const card = document.createElement('div');
            card.className = 'proctor-task-card';
            card.innerHTML = `
                <div class="proctor-task-header">
                    <div>
                        <h4><i class="fa-solid fa-file-signature text-primary"></i> ${t.title}</h4>
                        <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
                            <span class="badge badge-primary">${t.category}</span> • Deadline: <strong>${t.deadline}</strong>
                        </div>
                    </div>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span class="badge ${t.pending_count === 0 ? 'badge-success' : 'badge-warning'}" style="font-size:12.5px;">
                            ${t.completed_count} / ${t.total_assigned} Completed (${t.completion_rate}%)
                        </span>
                        <button class="btn btn-sm btn-outline" onclick="sendMenteeReminder('${t.task_id}', ${t.pending_count})">
                            <i class="fa-solid fa-paper-plane text-warning"></i> Send Reminder (${t.pending_count})
                        </button>
                    </div>
                </div>
                <p style="font-size:12.5px; color:var(--text-secondary); margin:6px 0;">${t.description}</p>
                <div class="task-progress-bar-wrap">
                    <div class="task-progress-bar-fill" style="width:${t.completion_rate}%;"></div>
                </div>

                <div class="task-mentees-breakdown-grid">
                    <div class="mentees-bucket-box">
                        <div class="mentees-bucket-title" style="color:#34d399;">
                            <span><i class="fa-solid fa-circle-check"></i> Completed Mentees (${t.completed_count})</span>
                        </div>
                        <div class="mentee-chips-wrap">${doneChips}</div>
                    </div>
                    <div class="mentees-bucket-box">
                        <div class="mentees-bucket-title" style="color:#f87171;">
                            <span><i class="fa-solid fa-triangle-exclamation"></i> Pending Action (${t.pending_count})</span>
                        </div>
                        <div class="mentee-chips-wrap">${pendingChips}</div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch(e) {}
}

function sendMenteeReminder(taskId, pendingCount) {
    if (pendingCount === 0) {
        showToast('All mentees have completed this task!', 'success');
        return;
    }
    showToast(`High-priority notification alert dispatched to ${pendingCount} pending mentees!`, 'success');
}

// 3. Load Bi-Weekly Parent Interaction Diary
async function loadFacultyParentInteractions(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/proctor/parent-interactions/${fId}`);
        const data = await res.json();
        const tbody = document.getElementById('proctor-ptm-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        (data.interactions || []).forEach(p => {
            const isCompleted = p.status === 'Completed';
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <strong>${p.student_name}</strong> <code>(${p.student_id})</code><br>
                    <small style="color:var(--text-muted);"><i class="fa-solid fa-user-tie"></i> ${p.parent_name} • ${p.parent_phone}</small>
                </td>
                <td><span class="badge badge-info">${p.scheduled_slot}</span><br><small><i class="fa-solid fa-calendar"></i> ${p.call_date}</small></td>
                <td>
                    <div style="font-size:12px; color:var(--text-primary); font-weight:600;">${p.discussion_points}</div>
                    <div style="font-size:11px; color:#34d399; margin-top:2px;"><i class="fa-solid fa-comment-dots"></i> ${p.parent_feedback}</div>
                </td>
                <td><span class="badge ${isCompleted ? 'badge-success' : 'badge-warning'}">${p.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) {}
}

// 4. Student Side: Load Meetings & Assigned Forms
async function loadStudentProctorDesk(studentId) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        // Meetings
        const mRes = await fetch(`/api/student/proctor-meetings/${sId}`);
        const mData = await mRes.json();
        const mTbody = document.getElementById('student-meetings-table');
        if (mTbody) {
            const meetings = mData.meetings || [];
            if (meetings.length > 0) {
                mTbody.innerHTML = `
                    <thead><tr><th>Date & Time</th><th>Purpose</th><th>Venue</th><th>Status</th></tr></thead>
                    <tbody>${meetings.map(m => `
                        <tr>
                            <td><strong>${m.date}</strong><br><small><i class="fa-solid fa-clock text-warning"></i> ${m.time_slot}</small></td>
                            <td><strong>${m.purpose}</strong></td>
                            <td><i class="fa-solid fa-location-dot text-danger"></i> ${m.venue}</td>
                            <td><span class="badge badge-success"><i class="fa-solid fa-lock"></i> ${m.status}</span></td>
                        </tr>
                    `).join('')}</tbody>
                `;
            } else {
                mTbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted p-3">No upcoming proctor meetings scheduled.</td></tr>';
            }
        }

        // Tasks / University Forms
        const tRes = await fetch(`/api/student/proctor-tasks/${sId}`);
        const tData = await tRes.json();
        const tList = document.getElementById('student-tasks-list');
        if (tList) {
            tList.innerHTML = '';
            (tData.tasks || []).forEach(t => {
                const card = document.createElement('div');
                card.className = `student-task-card ${t.is_completed ? 'completed' : ''}`;
                card.innerHTML = `
                    <div class="student-task-info" style="flex:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span class="badge badge-primary">${t.category}</span>
                            <span class="badge ${t.is_completed ? 'badge-success' : 'badge-danger'}">${t.status}</span>
                        </div>
                        <h4>${t.title}</h4>
                        <p>${t.description}</p>
                        <small style="color:var(--text-muted);"><i class="fa-solid fa-hourglass-half text-warning"></i> Deadline: <strong>${t.deadline}</strong></small>
                    </div>
                    <div>
                        ${t.is_completed 
                            ? '<span class="badge badge-success" style="padding:8px 12px;"><i class="fa-solid fa-circle-check"></i> Form Submitted</span>' 
                            : `<button class="btn btn-primary" onclick="submitStudentProctorTask('${t.task_id}', '${t.title}')"><i class="fa-solid fa-check-to-slot"></i> Complete & Submit Form</button>`
                        }
                    </div>
                `;
                tList.appendChild(card);
            });
        }
    } catch(e) {}
}

async function submitStudentProctorTask(taskId, taskTitle) {
    const sId = currentUser?.id || '25B11CS380';
    try {
        const res = await fetch('/api/student/complete-task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: sId, task_id: taskId, submission_notes: 'Online verification submitted by candidate.' })
        });
        const data = await res.json();
        showToast(data.message, 'success');
        loadStudentProctorDesk(sId);
    } catch(e) {
        showToast('Error submitting form', 'error');
    }
}

// 5. Populate Proctor Dropdowns & Wire Forms
async function populateProctorStudentDropdowns(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/faculty/dashboard/${fId}`);
        const data = await res.json();
        const proctees = data.proctees || [];

        const meetSel = document.getElementById('meet-student-select');
        const ptmSel = document.getElementById('ptm-student-select');

        if (meetSel && proctees.length > 0) {
            meetSel.innerHTML = proctees.map(p => `<option value="${p.student_id}">${p.name} (${p.student_id}) - ${p.branch}</option>`).join('');
        }
        if (ptmSel && proctees.length > 0) {
            ptmSel.innerHTML = proctees.map(p => `<option value="${p.student_id}" data-name="${p.name}">${p.name} (${p.student_id})</option>`).join('');
        }
    } catch(e) {}
}

function initProctorFormEvents() {
    // Schedule Meeting Form
    document.getElementById('proctor-meeting-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            faculty_id: currentUser?.id || '50101',
            student_id: document.getElementById('meet-student-select').value,
            date: document.getElementById('meet-date-input').value,
            time_slot: document.getElementById('meet-time-input').value,
            purpose: document.getElementById('meet-purpose-input').value,
            venue: document.getElementById('meet-venue-input').value
        };
        try {
            const res = await fetch('/api/proctor/schedule-meeting', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            showToast(data.message, 'success');
            loadFacultyProctorMeetings(currentUser?.id);
            document.getElementById('proctor-meeting-form').reset();
        } catch(e) {
            showToast('Error scheduling meeting', 'error');
        }
    });

    // Create Proctor Task / University Form
    document.getElementById('proctor-task-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            faculty_id: currentUser?.id || '50101',
            title: document.getElementById('task-title-input').value,
            category: document.getElementById('task-category-select').value,
            deadline: document.getElementById('task-deadline-input').value,
            description: document.getElementById('task-desc-input').value
        };
        try {
            const res = await fetch('/api/proctor/create-task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            showToast(data.message, 'success');
            loadFacultyProctorTasks(currentUser?.id);
            document.getElementById('proctor-task-form').reset();
        } catch(e) {
            showToast('Error creating task', 'error');
        }
    });

    // Log Parent Call Form
    document.getElementById('proctor-parent-call-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            faculty_id: currentUser?.id || '50101',
            student_id: document.getElementById('ptm-student-select').value,
            parent_name: document.getElementById('ptm-parent-input').value,
            scheduled_slot: document.getElementById('ptm-slot-select').value,
            call_date: new Date().toISOString().split('T')[0],
            discussion_topic: document.getElementById('ptm-topic-input').value,
            parent_feedback: document.getElementById('ptm-feedback-input').value
        };
        try {
            const res = await fetch('/api/proctor/log-parent-call', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            showToast(data.message, 'success');
            loadFacultyParentInteractions(currentUser?.id);
            document.getElementById('proctor-parent-call-form').reset();
        } catch(e) {
            showToast('Error logging parent call', 'error');
        }
    });
}
"""

js += proctor_js

# Hook into initialization
js = js.replace("initUniqueRoleEventListeners();", "initUniqueRoleEventListeners();\n    initProctorSubNavigation();\n    initProctorFormEvents();")

# Hook into student faculty loader
js = js.replace("loadStudentFaculties(currentUser.id);", "loadStudentFaculties(currentUser.id);\n    loadStudentProctorDesk(currentUser.id);")

# Hook into faculty proctoring loader
js = js.replace("loadFacultyProctoring(facultyId);", "loadFacultyProctoring(facultyId);\n    populateProctorStudentDropdowns(facultyId);\n    loadFacultyProctorMeetings(facultyId);\n    loadFacultyProctorTasks(facultyId);\n    loadFacultyParentInteractions(facultyId);")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Successfully injected Advanced Proctoring & Task Compliance JavaScript into static/js/app.js")

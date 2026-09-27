# update_app_js_assignments.py
import re

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Hide top logout button for student in setPortalRole
old_set_role = """    if (role === 'student') {
        topHeading.innerHTML = '🎓 STUDENT PORTAL';
        topSub.innerText = currentUser.branch || 'Department of Computer Science & Engineering';
        badgeRole.innerText = `🎓 Student (${effectiveId})`;
        badgeAvatar.innerHTML = '<i class="fa-solid fa-user-graduate"></i>';
    }"""

new_set_role = """    // User requirement: Hide sign out button at the top for student login
    const topLogout = document.getElementById('btn-top-logout');
    if (topLogout) {
        topLogout.style.display = (role === 'student') ? 'none' : 'inline-flex';
    }

    if (role === 'student') {
        topHeading.innerHTML = '🎓 STUDENT PORTAL';
        topSub.innerText = currentUser.branch || 'Department of Computer Science & Engineering';
        badgeRole.innerText = `🎓 Student (${effectiveId})`;
        badgeAvatar.innerHTML = '<i class="fa-solid fa-user-graduate"></i>';
    }"""

if old_set_role in js:
    js = js.replace(old_set_role, new_set_role)
    print("Added top logout hiding for student in setPortalRole")

# 2. Add Assignments Tab to renderSidebarMenu for student and faculty
old_student_menu = """        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-profile-tab', icon: 'fa-id-card', label: 'My Official Profile & Ledgers' },
            { id: 'student-attendance-tab', icon: 'fa-clipboard-check', label: 'Subject Attendance & Calculator' },"""

new_student_menu = """        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-profile-tab', icon: 'fa-id-card', label: 'My Official Profile & Ledgers' },
            { id: 'student-attendance-tab', icon: 'fa-clipboard-check', label: 'Subject Attendance & Calculator' },
            { id: 'student-assignments-tab', icon: 'fa-file-arrow-up', label: 'Assignments & Projects' },"""

if old_student_menu in js:
    js = js.replace(old_student_menu, new_student_menu)
    print("Added student-assignments-tab to student menu items")

# 3. Add tab switches to switchTab
old_switch_tab = "    if (tabId === 'student-attendance-tab') loadStudentDetailedAttendance(currentUser.id);"
new_switch_tab = """    if (tabId === 'student-attendance-tab') loadStudentDetailedAttendance(currentUser.id);
    if (tabId === 'student-assignments-tab') loadStudentAssignments(currentUser.id);
    if (tabId === 'faculty-assignments-tab') loadFacultyAssignments(currentUser.id);"""

if old_switch_tab in js and "loadStudentAssignments" not in js:
    js = js.replace(old_switch_tab, new_switch_tab)
    print("Added loadStudentAssignments to switchTab")

# 4. Add the Complete Student & Faculty Assignments Controller Functions
assignments_js = """

// ==============================================================================
// 14. ASSIGNMENTS SUBMISSION & CORRESPONDENT FACULTY ROUTING ENGINE
// ==============================================================================

let currentSelectedFile = null;
let currentAvailableAssignments = [];

async function loadStudentAssignments(studentId) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        const res = await fetch(`/api/student/assignments/${sId}`);
        const data = await res.json();
        if (!data) return;

        currentAvailableAssignments = data.available || [];
        const submissions = data.submissions || [];

        // Stats
        document.getElementById('stat-active-assignments').innerText = data.total_active || currentAvailableAssignments.length;
        document.getElementById('stat-submitted-assignments').innerText = data.total_submitted || submissions.length;
        document.getElementById('badge-total-submissions').innerText = `${submissions.length} Submissions Documented`;

        // Populate Select Dropdown
        const taskSelect = document.getElementById('asg-select-task');
        if (taskSelect) {
            taskSelect.innerHTML = currentAvailableAssignments.map((a, idx) => 
                `<option value="${a.id}" ${idx === 0 ? 'selected' : ''}>[${a.course_code}] ${a.subject} - ${a.title} (Due: ${a.due_date})</option>`
            ).join('');

            updateCorrespondentFacultyBanner();
            taskSelect.onchange = updateCorrespondentFacultyBanner;
        }

        // Populate Deadlines
        const deadlinesList = document.getElementById('asg-deadlines-container');
        if (deadlinesList) {
            deadlinesList.innerHTML = currentAvailableAssignments.map(a => `
                <div class="asg-item-card">
                    <div class="asg-item-info">
                        <h5>${a.subject}: ${a.title}</h5>
                        <p><i class="fa-solid fa-chalkboard-user text-primary"></i> Correspondent: <strong>${a.correspondent_faculty_name}</strong> (${a.department})</p>
                        <div class="asg-meta-row">
                            <span><i class="fa-solid fa-calendar-day text-warning"></i> Due: <strong>${a.due_date}</strong></span>
                            <span><i class="fa-solid fa-award text-success"></i> Max Marks: <strong>${a.max_marks}M</strong></span>
                            <span><i class="fa-solid fa-file text-info"></i> ${a.accepted_formats}</span>
                        </div>
                    </div>
                    <button class="btn btn-sm btn-outline-primary" onclick="selectAssignmentForSubmission('${a.id}')">
                        <i class="fa-solid fa-upload"></i> Select
                    </button>
                </div>
            `).join('');
        }

        // Populate Submissions Table
        const tbody = document.getElementById('student-submissions-tbody');
        if (tbody) {
            if (submissions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted p-4"><i class="fa-solid fa-file-circle-xmark fa-2x mb-2"></i><br>No assignment submissions recorded yet.</td></tr>';
            } else {
                tbody.innerHTML = submissions.map(s => {
                    const isGraded = s.status === 'Graded';
                    const statusBadge = isGraded 
                        ? '<span class="badge badge-success"><i class="fa-solid fa-check-circle"></i> Graded & Verified</span>'
                        : '<span class="badge badge-warning"><i class="fa-solid fa-clock"></i> Submitted - Under Review</span>';
                    
                    const isPdf = (s.file_format || '').toLowerCase().includes('pdf') || (s.filename || '').endsWith('.pdf');
                    const fileIcon = isPdf ? 'fa-file-pdf text-danger' : 'fa-file-word text-primary';

                    return `
                        <tr>
                            <td>
                                <strong>${s.subject}</strong><br>
                                <span style="font-size:12px; color:var(--text-secondary);">${s.title}</span>
                            </td>
                            <td>
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <div style="width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg,#1e3a8a,#3b82f6); color:#fff; display:flex; align-items:center; justify-content:center; font-size:12px;">
                                        <i class="fa-solid fa-user-tie"></i>
                                    </div>
                                    <div>
                                        <strong>${s.correspondent_faculty_name}</strong><br>
                                        <small class="text-muted">Faculty ID: ${s.correspondent_faculty_id}</small>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <i class="fa-solid ${fileIcon} fa-lg"></i>
                                    <div>
                                        <strong>${s.filename}</strong><br>
                                        <small class="text-muted">${s.file_size || 'Document'}</small>
                                    </div>
                                </div>
                            </td>
                            <td><span style="font-size:12px;">${s.submitted_at}</span></td>
                            <td>${statusBadge}</td>
                            <td>
                                <strong style="font-size:13.5px; color:${isGraded ? '#10b981' : '#f59e0b'};">
                                    ${s.marks || 'Pending'}
                                </strong>
                            </td>
                            <td>
                                <span style="font-size:12px; color:var(--text-secondary);">${s.faculty_remarks || 'Awaiting professor review.'}</span>
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }

        initAssignmentDropzone();
    } catch (e) {
        console.error('Error loading assignments:', e);
    }
}

function updateCorrespondentFacultyBanner() {
    const taskSelect = document.getElementById('asg-select-task');
    if (!taskSelect) return;
    const selectedId = taskSelect.value;
    const asg = currentAvailableAssignments.find(a => a.id === selectedId);
    if (asg) {
        document.getElementById('asg-fac-name').innerText = `${asg.correspondent_faculty_name} (${asg.correspondent_faculty_id})`;
        document.getElementById('asg-fac-dept').innerText = asg.department;
        const titleInput = document.getElementById('asg-title-input');
        if (titleInput && !titleInput.value) {
            titleInput.value = asg.title;
        }
    }
}

function selectAssignmentForSubmission(asgId) {
    const taskSelect = document.getElementById('asg-select-task');
    if (taskSelect) {
        taskSelect.value = asgId;
        updateCorrespondentFacultyBanner();
        document.getElementById('form-submit-assignment')?.scrollIntoView({ behavior: 'smooth' });
    }
}

function initAssignmentDropzone() {
    const dropzone = document.getElementById('asg-dropzone');
    const fileInput = document.getElementById('asg-file-input');
    const prompt = document.getElementById('dropzone-prompt');
    const preview = document.getElementById('dropzone-file-preview');
    const removeBtn = document.getElementById('btn-remove-selected-file');
    const form = document.getElementById('form-submit-assignment');

    if (!dropzone || !fileInput) return;

    dropzone.onclick = (e) => {
        if (e.target.closest('#btn-remove-selected-file')) return;
        fileInput.click();
    };

    dropzone.ondragover = (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-over');
    };
    dropzone.ondragleave = () => {
        dropzone.classList.remove('drag-over');
    };
    dropzone.ondrop = (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    };

    fileInput.onchange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    };

    removeBtn.onclick = (e) => {
        e.stopPropagation();
        currentSelectedFile = null;
        fileInput.value = '';
        preview.style.display = 'none';
        prompt.style.display = 'block';
    };

    function handleFileSelection(file) {
        const validExtensions = ['.pdf', '.doc', '.docx'];
        const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        if (!validExtensions.includes(ext)) {
            showToast('Invalid file format. Please attach a PDF or Word document (.pdf, .doc, .docx).', 'warning');
            return;
        }

        if (file.size > 25 * 1024 * 1024) {
            showToast('File size exceeds the 25MB limit.', 'danger');
            return;
        }

        currentSelectedFile = file;

        const sizeFormatted = file.size > 1024 * 1024 
            ? (file.size / (1024 * 1024)).toFixed(1) + ' MB'
            : (file.size / 1024).toFixed(0) + ' KB';

        document.getElementById('asg-preview-filename').innerText = file.name;
        document.getElementById('asg-preview-filesize').innerText = sizeFormatted;

        const iconContainer = document.getElementById('asg-file-type-icon');
        if (ext === '.pdf') {
            iconContainer.innerHTML = '<i class="fa-solid fa-file-pdf text-danger"></i>';
        } else {
            iconContainer.innerHTML = '<i class="fa-solid fa-file-word text-primary"></i>';
        }

        prompt.style.display = 'none';
        preview.style.display = 'flex';
    }

    form.onsubmit = async (e) => {
        e.preventDefault();
        const taskSelect = document.getElementById('asg-select-task');
        const titleInput = document.getElementById('asg-title-input');
        const notesInput = document.getElementById('asg-notes-input');
        const btn = document.getElementById('btn-submit-asg');

        if (!currentSelectedFile) {
            showToast('Please attach your assignment PDF or Word document before submitting.', 'warning');
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting to Faculty...';

        try {
            // Read as base64
            const reader = new FileReader();
            reader.onload = async () => {
                const base64Data = reader.result;
                const sizeFormatted = currentSelectedFile.size > 1024 * 1024 
                    ? (currentSelectedFile.size / (1024 * 1024)).toFixed(1) + ' MB'
                    : (currentSelectedFile.size / 1024).toFixed(0) + ' KB';

                const payload = {
                    student_id: currentUser?.id || '25B11CS380',
                    assignment_id: taskSelect.value,
                    title: titleInput.value.trim(),
                    notes: notesInput.value.trim(),
                    filename: currentSelectedFile.name,
                    file_size: sizeFormatted,
                    file_base64: base64Data
                };

                const res = await fetch('/api/student/submit-assignment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const resData = await res.json();

                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> <span>Submit Document to Correspondent Faculty</span>';

                if (resData.success) {
                    showToast('Assignment successfully submitted to correspondent faculty!', 'success');
                    // Reset inputs
                    titleInput.value = '';
                    notesInput.value = '';
                    currentSelectedFile = null;
                    fileInput.value = '';
                    preview.style.display = 'none';
                    prompt.style.display = 'block';
                    // Reload table
                    loadStudentAssignments(currentUser?.id);
                } else {
                    showToast(resData.message || 'Error submitting assignment.', 'danger');
                }
            };
            reader.readAsDataURL(currentSelectedFile);
        } catch (err) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> <span>Submit Document to Correspondent Faculty</span>';
            showToast('Submission error. Please try again.', 'danger');
        }
    };
}

async function loadFacultyAssignments(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/faculty/assignments/${fId}`);
        const data = await res.json();
        const submissions = data.submissions || [];
        
        const countBadge = document.getElementById('badge-fac-asg-count');
        if (countBadge) countBadge.innerText = `${submissions.length} Submissions`;

        const tbody = document.getElementById('faculty-assignments-tbody');
        if (tbody) {
            if (submissions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted p-4">No student submissions received for your courses yet.</td></tr>';
            } else {
                tbody.innerHTML = submissions.map(s => `
                    <tr>
                        <td>
                            <strong>${s.student_name}</strong><br>
                            <span class="badge badge-info" style="font-size:11px;">${s.student_id}</span>
                        </td>
                        <td>
                            <strong>${s.subject}</strong><br>
                            <small class="text-muted">${s.title}</small>
                        </td>
                        <td>
                            <div style="display:flex; align-items:center; gap:6px;">
                                <i class="fa-solid ${(s.file_format || '').toLowerCase().includes('pdf') ? 'fa-file-pdf text-danger' : 'fa-file-word text-primary'}"></i>
                                <span>${s.filename}</span>
                                <small class="text-muted">(${s.file_size})</small>
                            </div>
                        </td>
                        <td><small>${s.submitted_at}</small></td>
                        <td>
                            <span class="badge ${s.status === 'Graded' ? 'badge-success' : 'badge-warning'}">
                                ${s.status}
                            </span>
                        </td>
                        <td><strong>${s.marks || 'Pending'}</strong></td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="openFacultyGradeModal('${s.id}', '${s.student_name}', '${s.title}')">
                                <i class="fa-solid fa-marker"></i> Grade
                            </button>
                        </td>
                    </tr>
                `).join('');
            }
        }
    } catch (e) {
        console.error('Error loading faculty assignments:', e);
    }
}

function openFacultyGradeModal(subId, studentName, title) {
    const marks = prompt(`Enter CIA Marks awarded to ${studentName} for "${title}" (e.g. 28/30):`, "25/30");
    if (marks === null) return;
    const remarks = prompt("Enter evaluation remarks / feedback for the student:", "Well structured and thoroughly documented.");
    if (remarks === null) return;

    fetch('/api/faculty/grade-assignment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            faculty_id: currentUser?.id || '50101',
            submission_id: subId,
            marks: marks,
            remarks: remarks
        })
    }).then(res => res.json()).then(data => {
        if (data.success) {
            showToast('Assignment graded and student notified successfully!', 'success');
            loadFacultyAssignments(currentUser?.id);
        } else {
            showToast('Error saving grade.', 'danger');
        }
    });
}
"""

if "loadStudentAssignments" not in js:
    js += assignments_js
    print("Injected Assignments JavaScript logic into static/js/app.js")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updated static/js/app.js successfully!")

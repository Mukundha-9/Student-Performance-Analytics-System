# update_app_js_clean_assignments.py
import re

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Enforce permanent Light Mode in initTheme()
old_init_theme_full = """function initTheme() {
    const savedTheme = localStorage.getItem('aditya-theme') || 'dark';
    applyTheme(savedTheme, false);

    const toggleBtns = [
        document.getElementById('theme-toggle-btn'),
        document.getElementById('login-theme-toggle-btn')
    ];

    toggleBtns.forEach(btn => {
        btn?.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme, true);
        });
    });
}"""

new_init_theme_full = """function initTheme() {
    // Permanent Light Mode as requested by user
    applyTheme('light', false);
    localStorage.setItem('aditya-theme', 'light');
}"""

if old_init_theme_full in js:
    js = js.replace(old_init_theme_full, new_init_theme_full)
    print("Replaced initTheme to enforce permanent light mode")

# Also update DOMContentLoaded to initialize motion cursor
if "initMotionCursor();" not in js:
    js = js.replace("initPortalLogout();", "initPortalLogout();\n    initMotionCursor();")
    print("Added initMotionCursor to startup")

# 2. Replace the old Section 14 (assignments logic) with our refined, intuitive cards-based engine
old_sec14_pos = js.find("// 14. ASSIGNMENTS SUBMISSION & CORRESPONDENT FACULTY ROUTING ENGINE")
if old_sec14_pos != -1:
    js = js[:old_sec14_pos]
    print("Trimmed old assignments implementation")

clean_assignments_and_cursor_js = """// 14. ASSIGNMENTS SUBMISSION & CORRESPONDENT FACULTY ROUTING ENGINE
// ==============================================================================

let currentAvailableAssignments = [];
let currentSubmissionsList = [];
let currentModalSelectedFile = null;
let currentFilterMode = 'all';

// --- A. Interactive Motionable Cursor Engine ---
function initMotionCursor() {
    const dot = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    if (!dot || !ring || window.matchMedia('(pointer: coarse)').matches) return;

    let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
    let ringX = mouseX, ringY = mouseY;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
    });

    function loopRing() {
        ringX += (mouseX - ringX) * 0.18;
        ringY += (mouseY - ringY) * 0.18;
        ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;
        requestAnimationFrame(loopRing);
    }
    requestAnimationFrame(loopRing);

    // Dynamic Hover expansion for interactive UI elements
    document.addEventListener('mouseover', (e) => {
        const interactive = e.target.closest('button, a, input, select, textarea, .nav-item, .panel-card, .asg-clean-card, .quick-chip, .role-tab, .asg-filter-pill');
        if (interactive) {
            document.body.classList.add('cursor-hover');
        }
    });

    document.addEventListener('mouseout', (e) => {
        const interactive = e.target.closest('button, a, input, select, textarea, .nav-item, .panel-card, .asg-clean-card, .quick-chip, .role-tab, .asg-filter-pill');
        if (interactive) {
            document.body.classList.remove('cursor-hover');
        }
    });

    document.addEventListener('mousedown', () => document.body.classList.add('cursor-click'));
    document.addEventListener('mouseup', () => document.body.classList.remove('cursor-click'));
}

// --- B. Student Assignments Hub Controller ---
async function loadStudentAssignments(studentId) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        const res = await fetch(`/api/student/assignments/${sId}`);
        const data = await res.json();
        if (!data) return;

        currentAvailableAssignments = data.available || [];
        currentSubmissionsList = data.submissions || [];

        // Count pending vs completed
        const submittedAssignmentIds = currentSubmissionsList.map(s => s.assignment_id);
        const pendingCount = currentAvailableAssignments.filter(a => !submittedAssignmentIds.includes(a.id)).length;
        const completedCount = currentSubmissionsList.length;

        // Update Stat Counters
        const elActive = document.getElementById('stat-active-assignments');
        const elPending = document.getElementById('stat-pending-assignments');
        const elSubmitted = document.getElementById('stat-submitted-assignments');
        const elBadge = document.getElementById('badge-total-submissions');

        if (elActive) elActive.innerText = currentAvailableAssignments.length;
        if (elPending) elPending.innerText = pendingCount;
        if (elSubmitted) elSubmitted.innerText = completedCount;
        if (elBadge) elBadge.innerText = `${completedCount} Submissions Documented`;

        // Update Pill Counts
        const pAll = document.getElementById('pill-count-all');
        const pPend = document.getElementById('pill-count-pending');
        const pComp = document.getElementById('pill-count-completed');
        if (pAll) pAll.innerText = currentAvailableAssignments.length;
        if (pPend) pPend.innerText = pendingCount;
        if (pComp) pComp.innerText = completedCount;

        // Render Visual Cards Grid
        renderAssignmentsCards();

        // Render Submissions Table
        renderSubmissionsTable();

        // Initialize Modal Dropzone
        initModalDropzone();
    } catch (e) {
        console.error('Error loading assignments:', e);
    }
}

function filterAssignmentsList(mode) {
    currentFilterMode = mode;
    document.querySelectorAll('.asg-filter-pill').forEach(btn => btn.classList.remove('active'));
    event?.target?.closest('.asg-filter-pill')?.classList.add('active');
    renderAssignmentsCards();
}

function renderAssignmentsCards() {
    const grid = document.getElementById('asg-cards-grid');
    if (!grid) return;

    const submittedMap = {};
    currentSubmissionsList.forEach(s => {
        submittedMap[s.assignment_id] = s;
    });

    let displayList = currentAvailableAssignments;
    if (currentFilterMode === 'pending') {
        displayList = currentAvailableAssignments.filter(a => !submittedMap[a.id]);
    } else if (currentFilterMode === 'completed') {
        displayList = currentAvailableAssignments.filter(a => submittedMap[a.id]);
    }

    if (displayList.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1 / -1; padding: 40px; text-align: center; background:#fff; border-radius:12px; border:1px solid #e2e8f0; color:#64748b;"><i class="fa-solid fa-clipboard-check fa-3x mb-3 text-success"></i><h4>No assignments matching this filter</h4><p>Check back later or switch filter to view all course tasks.</p></div>';
        return;
    }

    const subjectColors = {
        'Python Programming': { bg: '#eff6ff', border: '#bfdbfe', text: '#1d4ed8' },
        'Data Structures': { bg: '#faf5ff', border: '#e9d5ff', text: '#7c3aed' },
        'Mathematics': { bg: '#ecfdf5', border: '#a7f3d0', text: '#059669' },
        'Physics': { bg: '#fffbeb', border: '#fde68a', text: '#d97706' },
        'English': { bg: '#fff1f2', border: '#fecdd3', text: '#e11d48' }
    };

    grid.innerHTML = displayList.map(a => {
        const sub = submittedMap[a.id];
        const isSubmitted = !!sub;
        const isGraded = isSubmitted && sub.status === 'Graded';
        
        const colors = subjectColors[a.subject] || { bg: '#f1f5f9', border: '#cbd5e1', text: '#334155' };

        let statusBadgeHtml = '';
        let actionBtnHtml = '';

        if (!isSubmitted) {
            statusBadgeHtml = '<span class="badge badge-warning" style="font-size:11.5px;"><i class="fa-solid fa-clock"></i> Pending Submission</span>';
            actionBtnHtml = `<button class="btn btn-primary" onclick="openAssignmentModal('${a.id}')"><i class="fa-solid fa-cloud-arrow-up"></i> Submit Assignment</button>`;
        } else if (isGraded) {
            statusBadgeHtml = `<span class="badge badge-success" style="font-size:11.5px;"><i class="fa-solid fa-circle-check"></i> Graded: ${sub.marks}</span>`;
            actionBtnHtml = `<button class="btn btn-outline-primary" onclick="scrollToSubmissions()"><i class="fa-solid fa-eye"></i> View Feedback & Document</button>`;
        } else {
            statusBadgeHtml = '<span class="badge badge-info" style="font-size:11.5px;"><i class="fa-solid fa-spinner fa-spin"></i> Submitted (Under Review)</span>';
            actionBtnHtml = `<button class="btn btn-outline-primary" onclick="scrollToSubmissions()"><i class="fa-solid fa-file-lines"></i> View Submission</button>`;
        }

        return `
            <div class="asg-clean-card">
                <div>
                    <div class="asg-card-top-row">
                        <span class="asg-course-badge" style="background:${colors.bg}; border:1px solid ${colors.border}; color:${colors.text};">
                            ${a.course_code} • ${a.subject}
                        </span>
                        <span class="badge badge-primary" style="font-size:11px;">
                            ${a.max_marks} Marks
                        </span>
                    </div>

                    <h4 class="asg-card-title">${a.title}</h4>
                    <p class="asg-card-instructions">${a.instructions}</p>

                    <div class="asg-fac-card-strip">
                        <div class="asg-fac-mini-avatar">
                            <i class="fa-solid fa-user-tie"></i>
                        </div>
                        <div class="asg-fac-mini-meta">
                            <small>Correspondent Faculty</small>
                            <h6>${a.correspondent_faculty_name} (${a.correspondent_faculty_id})</h6>
                        </div>
                    </div>
                </div>

                <div>
                    <div class="asg-card-meta-bar">
                        <span><i class="fa-solid fa-calendar-day text-warning"></i> Due: <strong>${a.due_date}</strong></span>
                        ${statusBadgeHtml}
                    </div>

                    <div class="asg-card-actions">
                        ${actionBtnHtml}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function renderSubmissionsTable() {
    const tbody = document.getElementById('student-submissions-tbody');
    if (!tbody) return;

    if (currentSubmissionsList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted p-4"><i class="fa-solid fa-file-circle-xmark fa-2x mb-2"></i><br>No assignment submissions recorded yet.</td></tr>';
        return;
    }

    tbody.innerHTML = currentSubmissionsList.map(s => {
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
                    <span style="font-size:12px; color:#475569;">${s.title}</span>
                </td>
                <td>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg,#1e3a8a,#2563eb); color:#fff; display:flex; align-items:center; justify-content:center; font-size:12px;">
                            <i class="fa-solid fa-user-tie"></i>
                        </div>
                        <div>
                            <strong>${s.correspondent_faculty_name}</strong><br>
                            <small class="text-muted">ID: ${s.correspondent_faculty_id}</small>
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
                <td><span style="font-size:12px; color:#334155;">${s.submitted_at}</span></td>
                <td>${statusBadge}</td>
                <td>
                    <strong style="font-size:14px; color:${isGraded ? '#059669' : '#d97706'};">
                        ${s.marks || 'Pending'}
                    </strong>
                </td>
                <td>
                    <span style="font-size:12px; color:#334155;">${s.faculty_remarks || 'Document routed to professor. Review in progress.'}</span>
                </td>
            </tr>
        `;
    }).join('');
}

function scrollToSubmissions() {
    document.getElementById('student-submissions-table')?.scrollIntoView({ behavior: 'smooth' });
}

function openAssignmentModal(asgId) {
    const asg = currentAvailableAssignments.find(a => a.id === asgId);
    if (!asg) return;

    document.getElementById('modal-asg-id-val').value = asg.id;
    document.getElementById('modal-asg-fac-name').innerText = `${asg.correspondent_faculty_name} (${asg.correspondent_faculty_id})`;
    document.getElementById('modal-asg-fac-dept').innerText = asg.department;
    document.getElementById('modal-asg-subject-val').innerText = `${asg.course_code} • ${asg.subject}`;
    document.getElementById('modal-asg-maxmarks-val').innerText = `${asg.max_marks} Marks`;
    document.getElementById('modal-asg-due-val').innerText = asg.due_date;
    document.getElementById('modal-asg-title-input').value = asg.title;
    document.getElementById('modal-asg-notes-input').value = '';

    // Clear file selection
    currentModalSelectedFile = null;
    const fileInput = document.getElementById('modal-asg-file-input');
    if (fileInput) fileInput.value = '';
    const prompt = document.getElementById('modal-dropzone-prompt');
    const preview = document.getElementById('modal-dropzone-file-preview');
    if (prompt) prompt.style.display = 'block';
    if (preview) preview.style.display = 'none';

    openModal('modal-submit-assignment');
}

function initModalDropzone() {
    const dropzone = document.getElementById('modal-asg-dropzone');
    const fileInput = document.getElementById('modal-asg-file-input');
    const prompt = document.getElementById('modal-dropzone-prompt');
    const preview = document.getElementById('modal-dropzone-file-preview');
    const removeBtn = document.getElementById('modal-btn-remove-selected-file');
    const form = document.getElementById('form-modal-submit-asg');

    if (!dropzone || !fileInput || !form) return;

    dropzone.onclick = (e) => {
        if (e.target.closest('#modal-btn-remove-selected-file')) return;
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
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    };

    fileInput.onchange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleSelectedFile(e.target.files[0]);
        }
    };

    removeBtn.onclick = (e) => {
        e.stopPropagation();
        currentModalSelectedFile = null;
        fileInput.value = '';
        preview.style.display = 'none';
        prompt.style.display = 'block';
    };

    function handleSelectedFile(file) {
        const validExtensions = ['.pdf', '.doc', '.docx'];
        const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        if (!validExtensions.includes(ext)) {
            showToast('Invalid format. Please attach a PDF or Word document (.pdf, .doc, .docx).', 'warning');
            return;
        }

        if (file.size > 25 * 1024 * 1024) {
            showToast('File size exceeds the 25MB limit.', 'danger');
            return;
        }

        currentModalSelectedFile = file;

        const sizeFormatted = file.size > 1024 * 1024 
            ? (file.size / (1024 * 1024)).toFixed(1) + ' MB'
            : (file.size / 1024).toFixed(0) + ' KB';

        document.getElementById('modal-asg-preview-filename').innerText = file.name;
        document.getElementById('modal-asg-preview-filesize').innerText = sizeFormatted;

        const iconContainer = document.getElementById('modal-asg-file-type-icon');
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
        const asgId = document.getElementById('modal-asg-id-val').value;
        const titleInput = document.getElementById('modal-asg-title-input');
        const notesInput = document.getElementById('modal-asg-notes-input');
        const btn = document.getElementById('btn-modal-submit-asg');

        if (!currentModalSelectedFile) {
            showToast('Please attach your assignment PDF or Word document before submitting.', 'warning');
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting to Faculty...';

        try {
            const reader = new FileReader();
            reader.onload = async () => {
                const base64Data = reader.result;
                const sizeFormatted = currentModalSelectedFile.size > 1024 * 1024 
                    ? (currentModalSelectedFile.size / (1024 * 1024)).toFixed(1) + ' MB'
                    : (currentModalSelectedFile.size / 1024).toFixed(0) + ' KB';

                const payload = {
                    student_id: currentUser?.id || '25B11CS380',
                    assignment_id: asgId,
                    title: titleInput.value.trim(),
                    notes: notesInput.value.trim(),
                    filename: currentModalSelectedFile.name,
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
                btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> <span>Submit Document to Faculty</span>';

                if (resData.success) {
                    closeModal('modal-submit-assignment');
                    showToast('Assignment successfully submitted to correspondent faculty!', 'success');
                    loadStudentAssignments(currentUser?.id);
                } else {
                    showToast(resData.message || 'Error submitting assignment.', 'danger');
                }
            };
            reader.readAsDataURL(currentModalSelectedFile);
        } catch (err) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> <span>Submit Document to Faculty</span>';
            showToast('Submission error. Please try again.', 'danger');
        }
    };
}
"""

js += "\n" + clean_assignments_and_cursor_js

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Injected clean assignments and motion cursor engine into static/js/app.js")

/**
 * Aditya University - Student Performance Analytics & Multi-Portal System
 * Dedicated Ultra-Modern Login Gateway & Role Portals (Student, Faculty, Admin)
 */

// Application State
let activeLoginRole = 'student'; // 'student' | 'faculty' | 'admin'
let currentRole = null;
let currentUser = null;
let currentTab = 'student-overview-tab';
let currentPage = 1;
let totalPages = 50;
let currentSort = { field: 'Percentage', order: 'desc' };

// Chart.js instances
let chartSubject = null;
let chartGrade = null;
let chartCorr = null;
let chartScoreDist = null;
let chartStudentRadar = null;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLoginGateway();
    initPortalLogout();
    initMotionCursor();
    initStudentPortalEvents();
    initFacultyPortalEvents();
    initAdminPortalEvents();
    initModals();
    initFiltersAndPagination();
    initSimulator();
    initAIAdvisor();
    initUniqueRoleEventListeners();
    initProctorSubNavigation();
    initProctorFormEvents();
    initNotificationFilterEvents();
    initStudentBookingEvents();
    initBunkSimulatorEvents();
    initMobileNavigationDrawer();

    // Check if user was already logged in (optional persistence)
    const savedUser = localStorage.getItem('aditya-user');
    const savedRole = localStorage.getItem('aditya-role');
    if (savedUser && savedRole) {
        try {
            currentUser = JSON.parse(savedUser);
            currentRole = savedRole;
            enterPortalDashboard(savedRole, currentUser);
        } catch (e) {
            renderLoginQuickChips('student');
        }
    } else {
        renderLoginQuickChips('student');
    }

    loadMatplotlibGallery();
    loadAcademicReport();
});

// Theme Switcher (Available ONLY on Main Three Login Page)
function initTheme() {
    const savedLoginTheme = localStorage.getItem('aditya-login-theme') || 'light';
    applyTheme(savedLoginTheme, false);
}

function applyTheme(theme, showNotice = true) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('aditya-login-theme', theme);

    // Update Login Screen Theme Toggle Button
    const loginIcon = document.getElementById('login-theme-icon');
    const loginLabel = document.getElementById('login-theme-label');
    if (loginIcon) loginIcon.className = theme === 'light' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
    if (loginLabel) loginLabel.innerText = theme === 'light' ? 'Dark Mode' : 'Light Mode';

    if (showNotice) {
        showToast(`Login screen switched to ${theme.toUpperCase()} theme`, 'info');
    }
}

function refreshChartsTheme() {
    if (currentRole === 'admin') {
        loadAdminPortal();
    } else if (currentRole === 'student') {
        if (currentTab === 'student-overview-tab') loadStudentOverview(currentUser?.id);
    }
}

// ==============================================================================
// 1. DEDICATED LOGIN GATEWAY LOGIC
// ==============================================================================

function initLoginGateway() {
    const tabs = document.querySelectorAll('.role-tab');
    const idLabel = document.getElementById('login-id-label');
    const userInput = document.getElementById('login-username');
    const pwInput = document.getElementById('login-password');
    const userIcon = document.getElementById('login-user-icon');
    const togglePwBtn = document.getElementById('btn-toggle-password');
    const eyeIcon = document.getElementById('eye-icon');
    const form = document.getElementById('main-login-form');

    // Role Tab Switching on Login Screen
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            activeLoginRole = tab.getAttribute('data-login-role');

            if (activeLoginRole === 'student') {
                idLabel.innerHTML = '<i class="fa-solid fa-id-card"></i> Student Roll Number (ID)';
                userInput.placeholder = 'e.g. 25B11CS380';
                userInput.value = '25B11CS380';
                userIcon.className = 'fa-solid fa-user-graduate input-icon';
            } else if (activeLoginRole === 'faculty') {
                idLabel.innerHTML = '<i class="fa-solid fa-id-badge"></i> Faculty 5-Digit Number (ID)';
                userInput.placeholder = 'e.g. 50101';
                userInput.value = '50101';
                userIcon.className = 'fa-solid fa-chalkboard-user input-icon';
            } else {
                idLabel.innerHTML = '<i class="fa-solid fa-building-columns"></i> Admin Employee ID';
                userInput.placeholder = 'e.g. 90001 or admin';
                userInput.value = '90001';
                userIcon.className = 'fa-solid fa-user-tie input-icon';
            }

            pwInput.value = 'aditya@123';
            renderLoginQuickChips(activeLoginRole);
        });
    });

    // Password Visibility Toggle
    togglePwBtn?.addEventListener('click', () => {
        if (pwInput.type === 'password') {
            pwInput.type = 'text';
            eyeIcon.className = 'fa-solid fa-eye-slash';
        } else {
            pwInput.type = 'password';
            eyeIcon.className = 'fa-solid fa-eye';
        }
    });

    // Theme Switcher ONLY for Main Three Login Page
    const loginThemeBtn = document.getElementById('btn-login-theme-toggle');
    loginThemeBtn?.addEventListener('click', () => {
        const curTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const nextTheme = curTheme === 'light' ? 'dark' : 'light';
        applyTheme(nextTheme, true);
    });

    // Login Form Submit Handler
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = userInput.value.trim();
        const password = pwInput.value.trim();

        if (!username) {
            showToast('Please enter your Login ID', 'error');
            return;
        }

        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role: activeLoginRole, username, password })
            });
            const data = await res.json();
            if (data.success) {
                currentUser = data.user;
                currentRole = activeLoginRole;
                localStorage.setItem('aditya-user', JSON.stringify(currentUser));
                localStorage.setItem('aditya-role', currentRole);
                showToast(`Access Granted! ${data.message}`, 'success');
                enterPortalDashboard(currentRole, currentUser);
            } else {
                showToast(data.message || 'Invalid Login ID or Password (Default: aditya@123)', 'error');
            }
        } catch (err) {
            showToast('Network error connecting to university server', 'error');
        }
    });
}

function renderLoginQuickChips(role) {
    const container = document.getElementById('quick-chips-container');
    const userInput = document.getElementById('login-username');
    const pwInput = document.getElementById('login-password');
    if (!container) return;

    container.innerHTML = '';
    let chips = [];

    if (role === 'student') {
        container.style.gridTemplateColumns = 'repeat(4, 1fr)';
        chips = [
            { id: '25B11CS380', label: 'Mukundha' },
            { id: '25B11CS932', label: 'Sai Abhiram' },
            { id: '25B11CS490', label: 'Sameer' },
            { id: '25B11CS891', label: 'Sajid' }
        ];
    } else if (role === 'faculty') {
        container.style.gridTemplateColumns = 'repeat(3, 1fr)';
        chips = [
            { id: '50101', label: '50101 (Dr. Sharma)' },
            { id: '50102', label: '50102 (Prof. Priya)' },
            { id: '50103', label: '50103 (Dr. Venkatesh)' }
        ];
    } else {
        container.style.gridTemplateColumns = 'repeat(2, 1fr)';
        chips = [
            { id: '90001', label: '90001 (Registrar)' },
            { id: 'admin', label: 'admin (Controller)' }
        ];
    }

    chips.forEach(c => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'quick-chip';
        btn.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>${c.label}</span>`;
        btn.title = `Click to load ${c.label} (${c.id})`;
        btn.onclick = () => {
            userInput.value = c.id;
            pwInput.value = 'aditya@123';
            showToast(`Loaded ${c.label} (${c.id})`, 'info');
        };
        container.appendChild(btn);
    });
}

// Enter Portal Dashboard Transition
function enterPortalDashboard(role, user) {
    document.getElementById('login-screen').classList.remove('active');
    document.getElementById('portal-dashboard').style.display = 'flex';
    // Ensure inner dashboards remain exclusively in vibrant light mode
    document.documentElement.setAttribute('data-theme', 'light');
    setPortalRole(role, user.user_id || user.id, user);
}

// Logout & Return to Gateway
function initPortalLogout() {
    const topLogout = document.getElementById('btn-top-logout');
    const sideLogout = document.getElementById('btn-sidebar-logout');

    const handleLogout = () => {
        localStorage.removeItem('aditya-user');
        localStorage.removeItem('aditya-role');
        document.getElementById('portal-dashboard').style.display = 'none';
        document.getElementById('login-screen').classList.add('active');
        // Restore login theme preference on main three login screen
        const savedLoginTheme = localStorage.getItem('aditya-login-theme') || 'light';
        applyTheme(savedLoginTheme, false);
        showToast('Signed out of university portal', 'info');
    };

    topLogout?.addEventListener('click', handleLogout);
    sideLogout?.addEventListener('click', handleLogout);
}
// Set Portal Role & Render Navigation
function setPortalRole(role, userId, userProfile = null) {
    currentRole = role;
    if (userProfile) {
        currentUser = userProfile;
        currentUser.id = userProfile.id || userProfile.user_id || userId;
    } else {
        if (!currentUser) currentUser = {};
        currentUser.id = userId;
    }

    const effectiveId = currentUser.id || userId;

    // Update Topbar
    const topHeading = document.getElementById('top-portal-heading');
    const topSub = document.getElementById('top-portal-sub');
    const navUser = document.getElementById('nav-session-user');
    const badgeName = document.getElementById('badge-user-name');
    const badgeRole = document.getElementById('badge-user-role');
    const badgeAvatar = document.getElementById('badge-avatar');

    // Top sign out completely removed for all roles

    if (role === 'student') {
        topHeading.innerHTML = '🎓 STUDENT PORTAL';
        topSub.innerText = currentUser.branch || 'Department of Computer Science & Engineering';
        badgeRole.innerText = `🎓 Student (${effectiveId})`;
        badgeAvatar.innerHTML = '<i class="fa-solid fa-user-graduate"></i>';
    } else if (role === 'faculty') {
        topHeading.innerHTML = '👨‍🏫 FACULTY PORTAL';
        topSub.innerText = currentUser.department || 'Academic Department';
        badgeRole.innerText = `👨‍🏫 Faculty (${effectiveId})`;
        badgeAvatar.innerHTML = '<i class="fa-solid fa-chalkboard-user"></i>';
    } else {
        topHeading.innerHTML = '🏛️ UNIVERSITY ADMIN PORTAL';
        topSub.innerText = 'Office of Academic Controller & Registrar';
        badgeRole.innerText = '🏛️ University Admin';
        badgeAvatar.innerHTML = '<i class="fa-solid fa-building-columns"></i>';
    }

    badgeName.innerText = currentUser.name || 'User';
    navUser.innerText = effectiveId;

    renderSidebarMenu(role);

    // Default Tab per role
    if (role === 'student') {
        switchTab('student-overview-tab');
        loadStudentPortal(effectiveId);
    } else if (role === 'faculty') {
        switchTab('faculty-attendance-tab');
        loadFacultyPortal(effectiveId);
    } else {
        switchTab('admin-dashboard-tab');
        loadAdminPortal();
    }
}

// Render Role-Specific Sidebar Navigation
function renderSidebarMenu(role) {
    const menu = document.getElementById('sidebar-navigation-menu');
    if (!menu) return;
    menu.innerHTML = '';

    let items = [];
    if (role === 'student') {
        items = [
            { id: 'student-overview-tab', icon: 'fa-gauge-high', label: 'My Academic Overview' },
            { id: 'student-profile-tab', icon: 'fa-id-card', label: 'My Official Profile & Ledgers' },
            { id: 'student-attendance-tab', icon: 'fa-clipboard-check', label: 'Subject Attendance & Calculator' },
            { id: 'student-assignments-tab', icon: 'fa-file-arrow-up', label: 'Assignments & Projects' },
            { id: 'student-notifications-tab', icon: 'fa-bell', label: 'Notifications & Circulars' },
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
            { id: 'faculty-assignments-tab', icon: 'fa-file-circle-check', label: 'Coursework Submissions' },
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
    }

    items.forEach((item, idx) => {
        const a = document.createElement('a');
        a.className = `nav-item ${idx === 0 ? 'active' : ''}`;
        a.setAttribute('data-tab', item.id);
        a.href = `#${item.id}`;
        a.innerHTML = `<i class="fa-solid ${item.icon}"></i> <span>${item.label}</span>`;
        a.addEventListener('click', (e) => {
            e.preventDefault();
            switchTab(item.id);
        });
        menu.appendChild(a);
    });
}

function switchTab(tabId) {
    currentTab = tabId;
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));

    const activeNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
    const activeSection = document.getElementById(tabId);

    if (activeNav) activeNav.classList.add('active');
    if (activeSection) activeSection.classList.add('active');

    if (tabId === 'student-overview-tab') loadStudentPortal(currentUser.id);
    if (tabId === 'student-timetable-tab') loadStudentTimetable(currentUser.id);
    if (tabId === 'student-faculty-tab') loadStudentFaculties(currentUser.id);
    if (tabId === 'student-notifications-tab') loadStudentNotifications(currentUser.id);
    if (tabId === 'student-attendance-tab') loadStudentDetailedAttendance(currentUser.id);
    if (tabId === 'student-assignments-tab') loadStudentAssignments(currentUser.id);
    if (tabId === 'faculty-assignments-tab') loadFacultyAssignments(currentUser.id);
    if (tabId === 'student-profile-tab') loadStudentProfile(currentUser.id);
    if (currentUser && currentUser.id && (tabId === 'student-faculty-tab' || tabId === 'student-overview-tab')) loadStudentProctorDesk(currentUser.id);
    if (tabId === 'student-fees-tab') loadStudentFees(currentUser.id);
    if (tabId === 'student-hallticket-tab') loadStudentHallTicket(currentUser.id);
    if (tabId === 'faculty-attendance-tab') loadFacultyRoster();
    if (tabId === 'faculty-marks-tab') loadFacultyMarksRoster();
    if (tabId === 'faculty-proctoring-tab') loadFacultyProctoring(currentUser.id);
    if (tabId === 'faculty-remedial-tab') loadFacultyRemedial(currentUser.id);
    if (tabId === 'faculty-leave-tab') loadFacultyLeaves(currentUser.id);
    if (tabId === 'admin-dashboard-tab') loadAdminPortal();
    if (tabId === 'admin-students-tab') loadStudentsTable();
    if (tabId === 'admin-results-tab') loadAdminResultsModeration();
    if (tabId === 'admin-announcements-tab') loadAdminAnnouncements();
    if (tabId === 'admin-audit-tab') loadAdminAccreditationAudit();
    if (tabId === 'admin-detention-tab') loadAdminDetentionList();
    if (tabId === 'ai-advisor-tab') loadCohortAI();
    if (tabId === 'simulator-tab') runSimulation();
    if (tabId === 'matplotlib-tab') loadMatplotlibGallery();
    if (tabId === 'report-tab') loadAcademicReport();
}

// Student Portal Loaders
async function loadStudentPortal(studentId) {
    try {
        const res = await fetch(`/api/student/${studentId}`);
        const card = await res.json();
        if (!card || card.error) return;

        document.getElementById('hero-branch-badge').innerText = card.branch;
        document.getElementById('hero-student-name').innerText = `Welcome, ${card.name}`;
        document.getElementById('hero-student-sub').innerText = `Roll No: ${card.student_id} • ${card.semester || 'Semester 4'} • Aditya University`;
        document.getElementById('hero-score-val').innerText = `${card.percentage}%`;
        document.getElementById('hero-rank-val').innerText = `#${card.class_rank}`;
        document.getElementById('hero-att-val').innerText = `${card.attendance}%`;

        const tbody = document.getElementById('student-marks-tbody');
        if (tbody) {
            tbody.innerHTML = '';
            for (const [sub, comp] of Object.entries(card.subject_comparisons || {})) {
                const tr = document.createElement('tr');
                const diffColor = comp.difference >= 0 ? '#10b981' : '#ef4444';
                const diffSign = comp.difference >= 0 ? '+' : '';
                tr.innerHTML = `
                    <td><strong>${sub.replace('_', ' ')}</strong></td>
                    <td><strong>${comp.score}</strong> / 100</td>
                    <td>${comp.class_mean}</td>
                    <td><code>Z = ${comp.z_score}</code> <small style="color:${diffColor};">(${diffSign}${comp.difference})</small></td>
                    <td><span class="badge ${comp.status === 'Pass' ? 'badge-pass' : 'badge-fail'}">${comp.status}</span></td>
                `;
                tbody.appendChild(tr);
            }
        }

        renderStudentRadarChart(card);
    } catch (e) {}
}

function renderStudentRadarChart(card) {
    const ctx = document.getElementById('chart-student-radar');
    if (!ctx) return;

    const subjects = Object.keys(card.subject_comparisons || {});
    const labels = subjects.map(s => s.replace('_', ' '));
    const scores = subjects.map(s => card.subject_comparisons[s].score);
    const means = subjects.map(s => card.subject_comparisons[s].class_mean);

    if (chartStudentRadar) chartStudentRadar.destroy();

    chartStudentRadar = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: card.name,
                    data: scores,
                    backgroundColor: 'rgba(59, 130, 246, 0.35)',
                    borderColor: '#3b82f6',
                    pointBackgroundColor: '#3b82f6',
                    borderWidth: 2
                },
                {
                    label: 'Cohort Average Benchmark',
                    data: means,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: '#10b981',
                    pointBackgroundColor: '#10b981',
                    borderWidth: 1.5,
                    borderDash: [4, 4]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.08)' },
                    pointLabels: { color: '#94a3b8', font: { size: 11, weight: 'bold' } },
                    suggestedMin: 30,
                    suggestedMax: 100,
                    ticks: { backdropColor: 'transparent', color: '#94a3b8' }
                }
            },
            plugins: { legend: { position: 'top', labels: { color: '#94a3b8' } } }
        }
    });
}

// Student Timetable
async function loadStudentTimetable(studentId) {
    try {
        const res = await fetch(`/api/student/timetable/${studentId}`);
        const data = await res.json();
        const schedule = data.full_schedule || {};
        const container = document.getElementById('timetable-cards-container');
        if (!container) return;

        function renderDay(dayName) {
            const classes = schedule[dayName] || [];
            container.innerHTML = '';
            classes.forEach(c => {
                const isCurrent = (dayName === data.today && c.period === data.active_period);
                const card = document.createElement('div');
                card.className = `period-card ${isCurrent ? 'active-period' : ''}`;
                card.innerHTML = `
                    <div class="period-time"><span>Period ${c.period}</span><span>${c.time}</span></div>
                    <h4>${c.subject_name}</h4>
                    <div class="period-faculty"><i class="fa-solid fa-chalkboard-user"></i> ${c.faculty}</div>
                    <div class="period-room"><i class="fa-solid fa-location-dot"></i> ${c.room}</div>
                    ${isCurrent ? '<span class="badge badge-danger" style="position:absolute; top:10px; right:10px;">LIVE NOW</span>' : ''}
                `;
                container.appendChild(card);
            });
        }

        renderDay('Monday');
        document.querySelectorAll('.day-btn').forEach(btn => {
            btn.onclick = () => {
                document.querySelectorAll('.day-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderDay(btn.getAttribute('data-day'));
            };
        });
    } catch (e) {}
}

// Student Faculties & Proctor
async function loadStudentFaculties(studentId) {
    try {
        const res = await fetch(`/api/student/faculties/${studentId}`);
        const data = await res.json();

        const p = data.proctor;
        const pContainer = document.getElementById('student-proctor-card');
        if (pContainer && p) {
            pContainer.innerHTML = `
                <div class="proctor-avatar"><i class="fa-solid fa-user-shield"></i></div>
                <div style="flex-grow:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="font-size:17px; color:var(--text-primary);">${p.name}</h4>
                        <span class="badge badge-warning">Assigned Academic Proctor</span>
                    </div>
                    <p style="font-size:13px; color:var(--text-secondary); margin:4px 0;">${p.designation} • ${p.department}</p>
                    <div style="display:flex; gap:16px; flex-wrap:wrap; font-size:12px; color:var(--text-muted); margin-top:8px;">
                        <span><i class="fa-solid fa-envelope text-primary"></i> ${p.email}</span>
                        <span><i class="fa-solid fa-phone text-success"></i> ${p.phone}</span>
                        <span><i class="fa-solid fa-door-open text-warning"></i> ${p.office}</span>
                        <span><i class="fa-solid fa-clock text-info"></i> ${p.office_hours}</span>
                    </div>
                </div>
                <div>
                    <button class="btn btn-primary" onclick="openModal('modal-request-meeting')"><i class="fa-solid fa-calendar-plus"></i> Request 1-on-1 Meeting</button>
                </div>
            `;
        }

        const grid = document.getElementById('student-faculties-grid');
        if (grid && data.enrolled_faculty) {
            grid.innerHTML = '';
            data.enrolled_faculty.forEach(f => {
                const card = document.createElement('div');
                card.className = 'faculty-card';
                card.innerHTML = `
                    <h4>${f.name}</h4>
                    <p>${f.designation}</p>
                    <div style="font-size:12px; color:var(--primary-light); margin-bottom:8px;"><strong>Subjects:</strong> ${f.subjects.join(', ')}</div>
                    <div style="font-size:11.5px; color:var(--text-muted);">
                        <div><i class="fa-solid fa-envelope"></i> ${f.email}</div>
                        <div><i class="fa-solid fa-location-dot"></i> ${f.office}</div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
    } catch (e) {}
}

// Student Fees
async function loadStudentFees(studentId) {
    try {
        const res = await fetch(`/api/student/fees/${studentId}`);
        const data = await res.json();

        document.getElementById('fee-total-display').innerText = `Rs. ${data.total_amount.toLocaleString()}`;
        document.getElementById('fee-paid-display').innerText = `Rs. ${data.amount_paid.toLocaleString()}`;
        document.getElementById('fee-due-display').innerText = `Rs. ${data.due_amount.toLocaleString()}`;

        const dueBadge = document.getElementById('fee-status-badge');
        if (data.due_amount === 0) {
            dueBadge.className = 'badge badge-success';
            dueBadge.innerText = 'No Dues Pending';
        } else {
            dueBadge.className = 'badge badge-danger';
            dueBadge.innerText = `Pending Rs. ${data.due_amount.toLocaleString()}`;
        }

        const tbody = document.getElementById('fee-history-tbody');
        if (tbody && data.payment_history) {
            tbody.innerHTML = '';
            data.payment_history.forEach(tx => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><code>${tx.receipt_no}</code></td>
                    <td>${tx.date}</td>
                    <td><strong>Rs. ${tx.amount.toLocaleString()}</strong></td>
                    <td>${tx.mode}</td>
                    <td><button class="btn btn-sm btn-outline" onclick="printReceipt('${tx.receipt_no}', ${tx.amount}, '${tx.date}', '${tx.mode}')"><i class="fa-solid fa-receipt"></i> Receipt</button></td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {}
}

function initStudentPortalEvents() {
    document.getElementById('fee-payment-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const amt = parseFloat(document.getElementById('pay-amount-input').value);
        const mode = document.querySelector('input[name="paymode"]:checked')?.value || 'UPI';

        try {
            const res = await fetch('/api/student/pay-fee', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ student_id: currentUser.id, amount: amt, mode: mode })
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                loadStudentFees(currentUser.id);
            } else {
                showToast(data.message, 'error');
            }
        } catch (err) {
            showToast('Fee payment failed', 'error');
        }
    });
}

function printReceipt(receiptNo, amount, date, mode) {
    const printWin = window.open('', '', 'width=700,height=500');
    printWin.document.write(`
        <html><head><title>Fee Receipt - Aditya University</title>
        <style>body{font-family:sans-serif; padding:30px; line-height:1.6; color:#0f172a;} .receipt-box{border:2px solid #1e3a8a; padding:24px; border-radius:8px;} h2{color:#1e3a8a; margin:0;} hr{border:0; border-top:1px solid #cbd5e1; margin:16px 0;}</style>
        </head><body>
        <div class="receipt-box">
            <h2>ADITYA UNIVERSITY</h2>
            <h4>OFFICIAL FEE CLEARANCE RECEIPT</h4>
            <hr>
            <p><strong>Receipt Number:</strong> ${receiptNo}</p>
            <p><strong>Student Name:</strong> ${currentUser.name} (${currentUser.id})</p>
            <p><strong>Transaction Date:</strong> ${date}</p>
            <p><strong>Amount Paid:</strong> INR ${amount.toLocaleString()}</p>
            <p><strong>Payment Mode:</strong> ${mode}</p>
            <p><strong>Status:</strong> <span style="color:#16a34a; font-weight:bold;">VERIFIED SUCCESSFUL</span></p>
            <hr>
            <small style="color:#64748b;">This is a computer-generated official receipt issued by the Office of Registrar, Aditya University.</small>
        </div>
        <script>window.print();</script>
        </body></html>
    `);
    printWin.document.close();
}

// Student Hall Ticket
async function loadStudentHallTicket(studentId) {
    try {
        const res = await fetch(`/api/student/hall-ticket/${studentId}`);
        const data = await res.json();
        const container = document.getElementById('hall-ticket-body');
        if (!container) return;

        let examRows = '';
        data.exams.forEach(ex => {
            examRows += `
                <tr>
                    <td><code>${ex.code}</code></td>
                    <td><strong>${ex.subject}</strong></td>
                    <td>${ex.date}</td>
                    <td>${ex.room}</td>
                </tr>
            `;
        });

        container.innerHTML = `
            <div class="ht-header">
                <div class="ht-logo-wrap">
                    <img src="/static/images/aditya_logo.png" alt="Aditya University Logo" class="ht-university-logo">
                </div>
                <h2 class="ht-title"><span style="color:#0f2b5c;">ADITYA</span> <span style="color:#ea580c;">UNIVERSITY</span></h2>
                <h4 class="ht-subtitle">END-SEMESTER EXAMINATION ADMIT CARD (HALL TICKET)</h4>
                <p class="ht-session-info">Academic Year 2025-2026 • Regular Examination Session • Office of the Controller of Examinations</p>
            </div>
            <div class="ht-student-grid">
                <div><strong>Candidate Name:</strong> <span style="font-weight:700; color:#0f2b5c;">${data.name}</span></div>
                <div><strong>Roll Number:</strong> <code style="font-size:13px; font-weight:700; color:#1e3a8a; background:#e0f2fe; padding:2px 8px; border-radius:4px;">${data.student_id}</code></div>
                <div><strong>Branch:</strong> ${data.branch}</div>
                <div><strong>Semester:</strong> ${data.semester}</div>
                <div><strong>Attendance:</strong> <span style="color:#16a34a; font-weight:bold;">${data.attendance}%</span> (${data.attendance_clearance})</div>
                <div><strong>Financial Clearance:</strong> <span style="color:#16a34a; font-weight:bold;">${data.financial_clearance}</span></div>
                <div style="grid-column:1/-1;"><strong>Designated Exam Venue:</strong> ${data.exam_center}</div>
            </div>
            <table class="ht-exams-table">
                <thead>
                    <tr>
                        <th style="width:18%;">Subject Code</th>
                        <th style="width:42%;">Subject Title</th>
                        <th style="width:25%;">Exam Date & Session</th>
                        <th style="width:15%;">Allotted Hall</th>
                    </tr>
                </thead>
                <tbody>${examRows}</tbody>
            </table>
            <div class="ht-footer-row">
                <div class="ht-sig-block">
                    <div class="ht-sig-line"></div>
                    <strong>Candidate Signature</strong>
                </div>
                <div class="ht-qr-block">
                    <i class="fa-solid fa-qrcode"></i><br>
                    <small>Verified QR</small>
                </div>
                <div class="ht-sig-block" style="text-align:right;">
                    <div class="ht-sig-line" style="margin-left:auto;"></div>
                    <strong>Controller of Examinations</strong>
                </div>
            </div>
        `;
    } catch (e) {}
}
// ==============================================================================
// 3. FACULTY PORTAL LOGIC
// ==============================================================================

async function loadFacultyPortal(facultyId) {
    loadFacultyRoster();
    loadFacultyMarksRoster();
    loadFacultyProctoring(facultyId);
    populateProctorStudentDropdowns(facultyId);
    loadFacultyProctorMeetings(facultyId);
    loadFacultyPendingMeetings(facultyId);
    loadFacultyProctorTasks(facultyId);
    loadFacultyParentInteractions(facultyId);
}

async function loadFacultyRoster() {
    const branch = document.getElementById('att-branch-select')?.value || 'Computer Science & Engineering';
    try {
        const res = await fetch(`/api/faculty/roster?branch=${encodeURIComponent(branch)}`);
        const data = await res.json();
        const tbody = document.getElementById('faculty-roster-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const roster = data.roster || [];
        roster.slice(0, 15).forEach(s => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${s.student_id}</code></td>
                <td><strong>${s.name}</strong></td>
                <td><span class="${s.attendance < 75 ? 'badge-att-low' : 'badge-att-ok'}">${s.attendance}%</span></td>
                <td>
                    <select class="form-input att-status-select" data-id="${s.student_id}" style="padding:4px 8px; font-size:12px; width:120px;">
                        <option value="Present" selected>🟢 Present</option>
                        <option value="Absent">🔴 Absent</option>
                        <option value="On Duty">🔵 On Duty</option>
                    </select>
                </td>
                <td><button class="btn btn-sm btn-outline" onclick="toggleAttStatus('${s.student_id}')"><i class="fa-solid fa-arrows-rotate"></i> Toggle</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {}
}

function toggleAttStatus(studentId) {
    const sel = document.querySelector(`.att-status-select[data-id="${studentId}"]`);
    if (sel) {
        sel.value = (sel.value === 'Present') ? 'Absent' : 'Present';
    }
}

async function loadFacultyMarksRoster() {
    const branch = document.getElementById('att-branch-select')?.value || 'Computer Science & Engineering';
    try {
        const res = await fetch(`/api/faculty/roster?branch=${encodeURIComponent(branch)}`);
        const data = await res.json();
        const tbody = document.getElementById('faculty-marks-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const roster = data.roster || [];
        roster.slice(0, 15).forEach(s => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${s.student_id}</code></td>
                <td><strong>${s.name}</strong></td>
                <td>Computer Science & Engineering</td>
                <td><input type="number" class="form-input cia-mark-input" data-id="${s.student_id}" value="85" min="0" max="100" style="width:100px; padding:4px 8px;"></td>
                <td><span class="badge badge-success">Grade A</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {}
}

async function loadFacultyProctoring(facultyId) {
    try {
        const res = await fetch(`/api/faculty/dashboard/${facultyId}`);
        const data = await res.json();

        const badgeAlert = document.getElementById('proctor-alert-count');
        if (badgeAlert) badgeAlert.innerText = `${data.at_risk_proctees_count || 0} Mentees Flagged At-Risk`;

        const tbody = document.getElementById('faculty-proctoring-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const proctees = data.proctees || [];
        proctees.forEach(p => {
            const tr = document.createElement('tr');
            const isRisk = p.is_at_risk;
            const shortBranch = (p.branch || 'CSE')
                .replace('Computer Science & Engineering', 'CSE')
                .replace('Electronics & Communication', 'ECE')
                .replace('Information Technology', 'IT')
                .replace('Electrical & Electronics', 'EEE')
                .replace('Mechanical Engineering', 'MECH')
                .replace('Civil Engineering', 'CIVIL');

            tr.innerHTML = `
                <td><code>${p.student_id}</code></td>
                <td><strong>${p.name}</strong></td>
                <td><span class="badge badge-primary" style="font-size:10.5px;">${shortBranch}</span></td>
                <td class="${p.attendance < 75 ? 'badge-att-low' : 'badge-att-ok'}">${p.attendance}%</td>
                <td><strong>${p.percentage}%</strong></td>
                <td><span class="grade-badge grade-${p.grade.replace('+', '-plus')}">${p.grade}</span></td>
                <td>
                    <span class="badge ${isRisk ? 'badge-danger' : 'badge-success'}" style="font-size:11px; white-space:normal; max-width:180px; display:inline-block; line-height:1.3;">
                        <i class="fa-solid ${isRisk ? 'fa-triangle-exclamation' : 'fa-circle-check'}"></i> 
                        ${isRisk ? p.risk_reasons : 'Normal'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline" style="padding:4px 8px; font-size:11.5px;" onclick="openProctorCounsellingModal('${p.student_id}', '${p.name}')">
                        <i class="fa-solid fa-comment-dots"></i> Log Note
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {}
}

function initFacultyPortalEvents() {
    initFacultyGradeFormEvents();
    document.getElementById('btn-mark-all-present')?.addEventListener('click', () => {
        document.querySelectorAll('.att-status-select').forEach(sel => sel.value = 'Present');
        showToast('All students marked Present', 'info');
    });

    document.getElementById('btn-submit-attendance')?.addEventListener('click', async () => {
        const selects = document.querySelectorAll('.att-status-select');
        const attData = {};
        selects.forEach(sel => {
            attData[sel.getAttribute('data-id')] = sel.value;
        });

        try {
            const res = await fetch('/api/faculty/post-attendance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subject: 'Python_Programming', attendance: attData })
            });
            const data = await res.json();
            showToast(data.message || 'Attendance submitted successfully!', 'success');
        } catch (e) {
            showToast('Failed to submit attendance', 'error');
        }
    });

    document.getElementById('btn-save-cia-marks')?.addEventListener('click', async () => {
        const inputs = document.querySelectorAll('.cia-mark-input');
        const marksData = {};
        inputs.forEach(inp => {
            marksData[inp.getAttribute('data-id')] = inp.value;
        });

        try {
            const res = await fetch('/api/faculty/post-marks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subject: 'Python_Programming', marks: marksData })
            });
            const data = await res.json();
            showToast(data.message || 'CIA marks updated and grades recalculated!', 'success');
        } catch (e) {
            showToast('Failed to save marks', 'error');
        }
    });

    document.getElementById('att-branch-select')?.addEventListener('change', loadFacultyRoster);
}

function openProctorCounsellingModal(studentId, studentName) {
    const notes = prompt(`Log Mentorship / Counselling Record for ${studentName} (${studentId}):\nEnter Action Plan & Advice:`, "Discussed study roadmap, attendance compliance, and remedial tutorial schedule.");
    if (notes) {
        showToast(`Counselling record logged for ${studentName}`, 'success');
    }
}
// ==============================================================================
// 4. ADMIN PORTAL LOGIC
// ==============================================================================

async function loadAdminPortal() {
    try {
        const res = await fetch('/api/summary');
        const data = await res.json();

        const overall = data.overall || {};
        document.getElementById('kpi-total-students').innerText = overall.total_students || 500;
        document.getElementById('kpi-pass-rate').innerText = `${overall.pass_percentage || 0}%`;
        document.getElementById('kpi-pass-count').innerText = `${overall.pass_count || 0} Pass / ${overall.fail_count || 0} Fail`;
        document.getElementById('kpi-class-mean').innerText = `${overall.mean_percentage || 0}%`;
        document.getElementById('kpi-median-score').innerText = `Median: ${overall.median_percentage || 0}%`;
        document.getElementById('kpi-std-dev').innerText = `${overall.std_percentage || 0}%`;
        document.getElementById('kpi-variance').innerText = `Variance: ${overall.var_percentage || 0}`;
        document.getElementById('kpi-avg-attendance').innerText = `${overall.mean_attendance || 0}%`;
        document.getElementById('kpi-low-att-count').innerText = `${data.low_attendance_count || 0} Below 75%`;

        renderSubjectChart(data.subject_stats || {});
        renderGradeChart(data.grade_distribution || {});
        renderCorrelationChart(data.correlation || {});
        renderScoreDistributionChart(overall);

    } catch (e) {}
}

function renderSubjectChart(subjectStats) {
    const ctx = document.getElementById('chart-subject-performance');
    if (!ctx) return;

    const subjects = Object.keys(subjectStats);
    const labels = subjects.map(s => s.replace('_', ' '));
    const means = subjects.map(s => subjectStats[s].mean);
    const highest = subjects.map(s => subjectStats[s].max);

    if (chartSubject) chartSubject.destroy();

    chartSubject = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: 'Subject Average (%)', data: means, backgroundColor: 'rgba(59, 130, 246, 0.85)', borderRadius: 4 },
                { label: 'Highest Score', data: highest, backgroundColor: 'rgba(16, 185, 129, 0.85)', borderRadius: 4 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'top', labels: { color: '#94a3b8' } } },
            scales: {
                y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}

function renderGradeChart(gradeDist) {
    const ctx = document.getElementById('chart-grade-distribution');
    if (!ctx) return;

    const labels = [], counts = [], colors = [];
    const gradeColorMap = { 'A+': '#10b981', 'A': '#3b82f6', 'B': '#6366f1', 'C': '#f59e0b', 'D': '#ec4899', 'F': '#ef4444' };

    for (const [grade, data] of Object.entries(gradeDist)) {
        if (data.count > 0) {
            labels.push(`Grade ${grade}`);
            counts.push(data.count);
            colors.push(gradeColorMap[grade] || '#94a3b8');
        }
    }

    if (chartGrade) chartGrade.destroy();

    chartGrade = new Chart(ctx, {
        type: 'doughnut',
        data: { labels: labels, datasets: [{ data: counts, backgroundColor: colors, borderWidth: 2 }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: { legend: { position: 'right', labels: { color: '#94a3b8' } } }
        }
    });
}

async function renderCorrelationChart(corrData) {
    const ctx = document.getElementById('chart-attendance-correlation');
    if (!ctx) return;

    document.getElementById('corr-badge').innerText = `r = ${corrData.r || 0.0}`;

    try {
        const res = await fetch('/api/students?page_size=100');
        const data = await res.json();
        const records = data.records || [];

        const passPoints = [], failPoints = [];
        records.forEach(r => {
            const pt = { x: r.Attendance, y: r.Percentage, name: r.Name, id: r.Student_ID };
            if (r.Status === 'Pass') passPoints.push(pt);
            else failPoints.push(pt);
        });

        const minX = 40, maxX = 100;
        const slope = corrData.slope || 0, intercept = corrData.intercept || 0;
        const trendLine = [
            { x: minX, y: Math.max(0, Math.min(100, slope * minX + intercept)) },
            { x: maxX, y: Math.max(0, Math.min(100, slope * maxX + intercept)) }
        ];

        if (chartCorr) chartCorr.destroy();

        chartCorr = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    { label: 'Passed Students', data: passPoints, backgroundColor: 'rgba(16, 185, 129, 0.75)', pointRadius: 4 },
                    { label: 'Failed Students', data: failPoints, backgroundColor: 'rgba(239, 68, 68, 0.85)', pointRadius: 5, pointStyle: 'crossRot' },
                    { type: 'line', label: 'Trendline', data: trendLine, borderColor: '#3b82f6', borderWidth: 2, borderDash: [5, 5], pointRadius: 0 }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'top', labels: { color: '#94a3b8' } } },
                scales: {
                    x: { title: { display: true, text: 'Attendance (%)', color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                    y: { title: { display: true, text: 'Percentage (%)', color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    } catch (e) {}
}

function renderScoreDistributionChart(overall) {
    const ctx = document.getElementById('chart-score-distribution');
    if (!ctx) return;

    const bins = ['0-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'];
    const distributionEst = [14, 38, 72, 142, 150, 70, 14];

    if (chartScoreDist) chartScoreDist.destroy();

    chartScoreDist = new Chart(ctx, {
        type: 'bar',
        data: { labels: bins, datasets: [{ label: '500-Cohort Density', data: distributionEst, backgroundColor: 'rgba(99, 102, 241, 0.8)', borderRadius: 4 }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}
// Master Students Table CRUD
async function loadStudentsTable() {
    const query = document.getElementById('search-input')?.value || '';
    const branch = document.getElementById('filter-branch')?.value || 'All';
    const grade = document.getElementById('filter-grade')?.value || 'All';
    const status = document.getElementById('filter-status')?.value || 'All';

    const params = new URLSearchParams({
        page: currentPage,
        page_size: 10,
        sort_by: currentSort.field,
        order: currentSort.order
    });

    if (query) params.append('q', query);
    if (branch !== 'All') params.append('branch', branch);
    if (grade !== 'All') params.append('grade', grade);
    if (status !== 'All') params.append('status', status);

    try {
        const res = await fetch(`/api/students?${params.toString()}`);
        const data = await res.json();

        const tbody = document.getElementById('students-table-body');
        if (!tbody) return;
        tbody.innerHTML = '';

        const records = data.records || [];
        records.forEach(s => {
            const studentId = s.Student_ID || s.Roll_No;
            const branchName = s.Branch || s.Department;
            const statusBadge = s.Status === 'Pass' ? 'badge-pass' : 'badge-fail';
            const attClass = s.Attendance < 75 ? 'badge-att-low' : 'badge-att-ok';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${studentId}</code></td>
                <td><strong>${s.Name}</strong></td>
                <td>${branchName}</td>
                <td>${s.Semester || 'Sem 4'}</td>
                <td class="${attClass}">${s.Attendance}%</td>
                <td>${s.Mathematics}</td>
                <td>${s.Physics}</td>
                <td>${s.Python_Programming}</td>
                <td>${s.Data_Structures}</td>
                <td>${s.English}</td>
                <td><strong>${s.Total_Marks}</strong></td>
                <td><strong>${s.Percentage}%</strong></td>
                <td><span class="grade-badge grade-${s.Grade.replace('+', '-plus')}">${s.Grade}</span></td>
                <td><span class="badge ${statusBadge}">${s.Status}</span></td>
                <td class="text-center">
                    <div class="action-btn-group">
                        <button class="action-icon-btn btn-view" title="View Grade Card" onclick="openStudentReportCard('${studentId}')"><i class="fa-solid fa-award"></i></button>
                        <button class="action-icon-btn btn-cert" title="Print Certificate" onclick="openCertificateModal('${studentId}')"><i class="fa-solid fa-certificate"></i></button>
                        <button class="action-icon-btn btn-delete" title="Delete Student" onclick="deleteStudent('${studentId}')"><i class="fa-solid fa-trash-can"></i></button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });

        totalPages = data.total_pages || 1;
        document.getElementById('total-records-count').innerText = data.total || 500;
        document.getElementById('page-start').innerText = records.length > 0 ? (currentPage - 1) * 10 + 1 : 0;
        document.getElementById('page-end').innerText = Math.min(currentPage * 10, data.total || 500);
        document.getElementById('current-page-display').innerText = `Page ${currentPage} of ${totalPages}`;

        document.getElementById('btn-prev-page').disabled = currentPage <= 1;
        document.getElementById('btn-next-page').disabled = currentPage >= totalPages;

    } catch (err) {}
}

// Announcements
async function loadAdminAnnouncements() {
    try {
        const res = await fetch('/api/admin/announcements');
        const data = await res.json();
        const list = document.getElementById('admin-announcements-list');
        if (!list) return;

        list.innerHTML = '';
        (data.announcements || []).forEach(a => {
            const card = document.createElement('div');
            card.className = `announcement-card cat-${a.category}`;
            card.innerHTML = `
                <div class="ann-card-header">
                    <h4>${a.title}</h4>
                    <span class="badge ${a.badge_class || 'badge-primary'}">${a.category}</span>
                </div>
                <div class="ann-card-meta">
                    <span><i class="fa-solid fa-user"></i> ${a.author}</span>
                    <span><i class="fa-solid fa-calendar"></i> ${a.date}</span>
                    <span><i class="fa-solid fa-users"></i> Target: ${a.target}</span>
                </div>
                <p style="font-size:12.5px; color:var(--text-secondary); line-height:1.5;">${a.content}</p>
            `;
            list.appendChild(card);
        });
    } catch (e) {}
}

function initAdminPortalEvents() {
    document.getElementById('announcement-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            title: document.getElementById('ann-title-input').value.trim(),
            category: document.getElementById('ann-cat-select').value,
            target: document.getElementById('ann-target-select').value,
            content: document.getElementById('ann-content-input').value.trim()
        };

        try {
            const res = await fetch('/api/admin/announcements', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                document.getElementById('announcement-form').reset();
                loadAdminAnnouncements();
            }
        } catch (err) {
            showToast('Error publishing announcement', 'error');
        }
    });
}

// AI Advisor & Simulator
async function loadCohortAI() {
    try {
        const res = await fetch('/api/ai-cohort-insights');
        const data = await res.json();
        const list = document.getElementById('cohort-ai-insights-list');
        if (!list) return;
        list.innerHTML = '';

        const insights = data.executive_insights || [];
        insights.forEach(item => {
            const card = document.createElement('div');
            card.className = 'ai-insight-card';
            card.innerHTML = `
                <div class="ai-icon-box"><i class="fa-solid ${item.icon}"></i></div>
                <div class="ai-card-content">
                    <h4>${item.title}</h4>
                    <p>${item.detail}</p>
                </div>
            `;
            list.appendChild(card);
        });

        runStudentAIDiagnostic(currentUser?.id || '25B11CS380');
    } catch (e) {}
}

function initAIAdvisor() {
    document.getElementById('btn-run-ai-diagnostic')?.addEventListener('click', () => {
        const id = document.getElementById('ai-student-id-input')?.value.trim();
        if (id) runStudentAIDiagnostic(id);
    });
}

async function runStudentAIDiagnostic(studentId) {
    const resultBox = document.getElementById('student-ai-diagnostic-result');
    if (!resultBox) return;
    resultBox.innerHTML = '<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i> Synthesizing Student AI Profile...</div>';

    try {
        const res = await fetch(`/api/ai-insights/${studentId}`);
        const data = await res.json();
        if (data.error) {
            resultBox.innerHTML = `<p class="text-danger p-3">${data.error}</p>`;
            return;
        }

        let strList = data.strengths.map(s => `<li><i class="fa-solid fa-circle-check text-success"></i> ${s}</li>`).join('');
        let weakList = data.areas_for_improvement.map(w => `<li><i class="fa-solid fa-circle-exclamation text-danger"></i> ${w}</li>`).join('');
        let recList = data.actionable_recommendations.map(r => `<li><i class="fa-solid fa-arrow-right text-primary"></i> ${r}</li>`).join('');

        resultBox.innerHTML = `
            <div style="background:var(--bg-main); border:1px solid var(--border-color); border-radius:8px; padding:16px;">
                <h4 style="color:var(--text-primary); margin-bottom:10px;"><i class="fa-solid fa-id-badge text-primary"></i> Learning Trajectory: <strong>${data.learning_trajectory}</strong></h4>
                <div style="font-size:12.5px; color:var(--text-secondary); margin-bottom:14px; background:rgba(59,130,246,0.08); padding:10px; border-radius:6px;">
                    <i class="fa-solid fa-user-clock text-primary"></i> ${data.attendance_impact_analysis}
                </div>
                <h5 style="color:#34d399; font-size:12.5px; margin-bottom:6px;"><i class="fa-solid fa-award"></i> Core Strengths:</h5>
                <ul class="math-list" style="margin-bottom:14px; list-style:none;">${strList}</ul>
                <h5 style="color:#f87171; font-size:12.5px; margin-bottom:6px;"><i class="fa-solid fa-bullseye"></i> Areas for Targeted Growth:</h5>
                <ul class="math-list" style="margin-bottom:14px; list-style:none;">${weakList}</ul>
                <h5 style="color:var(--primary-light); font-size:12.5px; margin-bottom:6px;"><i class="fa-solid fa-list-check"></i> Actionable Roadmap:</h5>
                <ul class="math-list" style="list-style:none;">${recList}</ul>
            </div>
        `;
    } catch (e) {
        resultBox.innerHTML = '<p class="text-danger p-3">Error fetching student AI diagnostic.</p>';
    }
}

// What-If Simulator Logic
function initSimulator() {
    const sliders = ['attendance', 'math', 'physics', 'python', 'dsa', 'english'];
    sliders.forEach(s => {
        const slider = document.getElementById(`slider-sim-${s}`);
        const label = document.getElementById(`val-sim-${s}`);
        slider?.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            if (s === 'attendance') label.innerText = `${val}%`;
            else label.innerText = val >= 0 ? `+${val.toFixed(1)}` : `${val.toFixed(1)}`;
            runSimulation();
        });
    });

    document.getElementById('btn-run-simulation')?.addEventListener('click', runSimulation);
    document.getElementById('sim-student-id')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') runSimulation();
    });
}

async function runSimulation() {
    const studentId = document.getElementById('sim-student-id')?.value.trim() || currentUser?.id || '25B11CS380';
    const newAtt = parseFloat(document.getElementById('slider-sim-attendance')?.value || 85);
    const deltas = {
        'Mathematics': parseFloat(document.getElementById('slider-sim-math')?.value || 0),
        'Physics': parseFloat(document.getElementById('slider-sim-physics')?.value || 0),
        'Python_Programming': parseFloat(document.getElementById('slider-sim-python')?.value || 0),
        'Data_Structures': parseFloat(document.getElementById('slider-sim-dsa')?.value || 0),
        'English': parseFloat(document.getElementById('slider-sim-english')?.value || 0)
    };

    try {
        const res = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: studentId, attendance: newAtt, marks_delta: deltas })
        });
        const data = await res.json();
        if (data.error) return;

        const sim = data.simulated;
        const out = document.getElementById('simulation-outcome-display');
        if (!out) return;

        const gainSign = sim.percentage_gain >= 0 ? '+' : '';
        const rankGainSign = sim.rank_gain >= 0 ? '🔺 Up' : '🔻 Down';

        out.innerHTML = `
            <div class="sim-trajectory-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h4 style="color:#ffffff; font-size:16px;">${data.name} <code>(${data.student_id})</code></h4>
                        <span style="font-size:12px; color:#94a3b8;">Simulated Performance Shift</span>
                    </div>
                    <span class="badge ${sim.status === 'Pass' ? 'badge-pass' : 'badge-fail'}" style="font-size:13px;">${sim.grade} (${sim.status})</span>
                </div>
                <div class="sim-metrics-grid">
                    <div class="sim-stat-box">
                        <span>Projected Score</span>
                        <strong style="color:#60a5fa;">${sim.percentage}% <span style="font-size:11px; color:#34d399;">(${gainSign}${sim.percentage_gain}%)</span></strong>
                    </div>
                    <div class="sim-stat-box">
                        <span>Projected Class Rank</span>
                        <strong style="color:#fbbf24;">#${sim.class_rank} of 500</strong>
                        <span style="font-size:10.5px; color:#34d399;">${rankGainSign} ${Math.abs(sim.rank_gain)} Ranks</span>
                    </div>
                    <div class="sim-stat-box">
                        <span>Cohort Percentile</span>
                        <strong style="color:#c084fc;">${sim.percentile}%</strong>
                        <span style="font-size:10.5px; color:#94a3b8;">Top ${Math.max(1, (100 - sim.percentile).toFixed(1))}%</span>
                    </div>
                </div>
            </div>
        `;
    } catch (e) {}
}

// Matplotlib Gallery
async function loadMatplotlibGallery() {
    const grid = document.getElementById('matplotlib-gallery-grid');
    if (!grid) return;

    try {
        const res = await fetch('/api/charts/list');
        const data = await res.json();
        grid.innerHTML = '';
        (data.charts || []).forEach(c => {
            const card = document.createElement('div');
            card.className = 'gallery-card';
            card.innerHTML = `
                <div class="gallery-img-wrap" onclick="openLightbox('/api/charts/${c.filename}', '${c.name}')">
                    <img src="/api/charts/${c.filename}" alt="${c.name}" loading="lazy">
                </div>
                <div class="gallery-card-body">
                    <h4>${c.name}</h4>
                    <p>${c.type} • 300 DPI Matplotlib Plot</p>
                    <div style="display:flex; gap:8px;">
                        <button class="btn btn-sm btn-outline" onclick="openLightbox('/api/charts/${c.filename}', '${c.name}')"><i class="fa-solid fa-expand"></i> View</button>
                        <a href="/api/charts/${c.filename}" download="${c.filename}" class="btn btn-sm btn-primary"><i class="fa-solid fa-download"></i> PNG</a>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
    } catch (e) {}
}

// Academic Report
async function loadAcademicReport() {
    const viewer = document.getElementById('report-markdown-content');
    if (!viewer) return;

    try {
        const res = await fetch('/api/report/markdown');
        const data = await res.json();
        if (data.markdown) {
            let html = data.markdown
                .replace(/^# (.*$)/gim, '<h1 style="color:#1e3a8a; border-bottom:2px solid #1e3a8a; padding-bottom:8px; margin-bottom:14px;">$1</h1>')
                .replace(/^## (.*$)/gim, '<h2 style="color:#1e293b; margin-top:20px; margin-bottom:10px; font-size:18px;">$1</h2>')
                .replace(/^### (.*$)/gim, '<h3 style="color:#334155; margin-top:14px; font-size:15px;">$1</h3>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                .replace(/`([^`]+)`/gim, '<code>$1</code>')
                .replace(/\|(.+)\|/gim, (match) => {
                    const cells = match.split('|').filter(c => c.trim() !== '');
                    return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
                })
                .replace(/\n\n/gim, '<br><br>');

            viewer.innerHTML = `<div style="background:#ffffff; color:#1e293b; padding:24px; border-radius:8px; font-family:Plus Jakarta Sans, sans-serif; line-height:1.6;">${html}</div>`;
        }
    } catch (e) {}
}

// Modals
async function openStudentReportCard(studentId = null) {
    const sId = studentId || currentUser?.id || '25B11CS380';
    try {
        const res = await fetch(`/api/student/${sId}`);
        const card = await res.json();
        if (!card || card.error) return;

        const body = document.getElementById('report-card-body');
        let subjectRows = '';
        for (const [sub, comp] of Object.entries(card.subject_comparisons || {})) {
            const diffClass = comp.difference >= 0 ? '#10b981' : '#ef4444';
            const diffSign = comp.difference >= 0 ? '+' : '';
            subjectRows += `
                <tr>
                    <td><strong>${sub.replace('_', ' ')}</strong></td>
                    <td><strong>${comp.score}</strong> / 100</td>
                    <td>${comp.class_mean}</td>
                    <td style="color:${diffClass}; font-weight:700;">${diffSign}${comp.difference}</td>
                    <td><code>Z = ${comp.z_score}</code></td>
                    <td><span class="badge ${comp.status === 'Pass' ? 'badge-pass' : 'badge-fail'}">${comp.status}</span></td>
                </tr>
            `;
        }

        body.innerHTML = `
            <div class="report-card-view">
                <div class="rc-header">
                    <h2>ADITYA UNIVERSITY</h2>
                    <h3>Department of Computer Science & Engineering</h3>
                    <p style="font-size:12px; color:#64748b; margin-top:2px;">OFFICIAL ACADEMIC GRADE REPORT</p>
                </div>
                <div class="rc-student-info">
                    <div><strong>Student Name:</strong> ${card.name}</div>
                    <div><strong>Roll Number:</strong> <code>${card.student_id}</code></div>
                    <div><strong>Branch:</strong> ${card.branch}</div>
                    <div><strong>Semester:</strong> ${card.semester || 'Semester 4'}</div>
                    <div><strong>Attendance:</strong> ${card.attendance}%</div>
                    <div><strong>Gender:</strong> ${card.gender || 'Male'}</div>
                </div>
                <table class="rc-table">
                    <thead><tr><th>Subject</th><th>Marks</th><th>Class Avg</th><th>Diff</th><th>Z-Score</th><th>Result</th></tr></thead>
                    <tbody>${subjectRows}</tbody>
                </table>
                <div class="rc-summary-box">
                    <div><span>Total Marks</span><br>${card.total_marks} / 500</div>
                    <div><span>Percentage</span><br>${card.percentage}%</div>
                    <div><span>Class Rank</span><br>#${card.class_rank} of 500</div>
                    <div><span>Final Grade</span><br>${card.grade} (${card.status})</div>
                </div>
            </div>
        `;

        document.getElementById('report-card-modal').classList.add('active');
    } catch (e) {}
}

function printStudentReportCard() {
    openStudentReportCard(currentUser?.id);
}

async function openCertificateModal(studentId) {
    try {
        const res = await fetch(`/api/certificate/${studentId}`);
        const cert = await res.json();
        if (cert.error) return;

        const body = document.getElementById('certificate-body');
        body.innerHTML = `
            <div class="certificate-view">
                <div class="cert-title">ADITYA UNIVERSITY</div>
                <div class="cert-subtitle">DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</div>
                <p style="font-size:12px; color:#78350f; letter-spacing:2px; margin-top:4px;">CERTIFICATE OF ACADEMIC EXCELLENCE</p>
                <p style="font-size:13px; font-family:'Plus Jakarta Sans', sans-serif; color:#64748b; margin-top:14px;">This Certificate of Academic Distinction is proudly presented to</p>
                <div class="cert-recipient">${cert.name}</div>
                <p style="font-size:12px; font-family:'JetBrains Mono', monospace; color:#1e3a8a; font-weight:700; margin-bottom:12px;">Roll Number: ${cert.student_id} | ${cert.branch}</p>
                <p class="cert-text">for demonstrating exemplary academic rigor, securing <strong>Rank #${cert.class_rank}</strong> in the 500-student cohort with an overall score of <strong>${cert.percentage}% (Grade ${cert.grade})</strong> during ${cert.issue_date}.</p>
                <div class="cert-footer">
                    <div class="cert-sig">Head of Department<br><strong style="color:#1e3a8a;">Dr. Academic Dean</strong></div>
                    <div class="cert-seal"><i class="fa-solid fa-award"></i></div>
                    <div class="cert-sig">Course Coordinator<br><strong style="color:#1e3a8a;">Faculty Mentor</strong></div>
                </div>
            </div>
        `;

        document.getElementById('certificate-modal').classList.add('active');
    } catch (e) {}
}

function initModals() {
    const studentModal = document.getElementById('student-modal');
    const openAddBtn = document.getElementById('open-add-student-modal');
    const closeAddBtn = document.getElementById('modal-close-btn');
    const cancelAddBtn = document.getElementById('btn-cancel-modal');
    const form = document.getElementById('student-form');

    openAddBtn?.addEventListener('click', () => {
        form.reset();
        document.getElementById('modal-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Add New Student Record';
        document.getElementById('form-id').removeAttribute('readonly');
        studentModal.classList.add('active');
    });

    closeAddBtn?.addEventListener('click', () => studentModal.classList.remove('active'));
    cancelAddBtn?.addEventListener('click', () => studentModal.classList.remove('active'));

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            Student_ID: document.getElementById('form-id').value.trim(),
            Name: document.getElementById('form-name').value.trim(),
            Gender: document.getElementById('form-gender').value,
            Branch: document.getElementById('form-branch').value,
            Semester: document.getElementById('form-semester').value,
            Attendance: parseFloat(document.getElementById('form-attendance').value),
            Mathematics: parseFloat(document.getElementById('form-math').value),
            Physics: parseFloat(document.getElementById('form-physics').value),
            Python_Programming: parseFloat(document.getElementById('form-python').value),
            Data_Structures: parseFloat(document.getElementById('form-dsa').value),
            English: parseFloat(document.getElementById('form-english').value)
        };

        try {
            const res = await fetch('/api/student', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();
            if (result.success) {
                showToast(result.message || 'Saved successfully', 'success');
                studentModal.classList.remove('active');
                loadStudentsTable();
            } else {
                showToast(result.message || 'Error saving student', 'error');
            }
        } catch (err) {
            showToast('Network error while saving student', 'error');
        }
    });

    document.getElementById('report-card-close-btn')?.addEventListener('click', () => {
        document.getElementById('report-card-modal').classList.remove('active');
    });
    document.getElementById('btn-close-report-modal')?.addEventListener('click', () => {
        document.getElementById('report-card-modal').classList.remove('active');
    });

    document.getElementById('certificate-close-btn')?.addEventListener('click', () => {
        document.getElementById('certificate-modal').classList.remove('active');
    });
    document.getElementById('btn-close-cert-modal')?.addEventListener('click', () => {
        document.getElementById('certificate-modal').classList.remove('active');
    });

    document.getElementById('lightbox-close-btn')?.addEventListener('click', () => {
        document.getElementById('image-lightbox-modal').classList.remove('active');
    });

    document.getElementById('btn-regenerate-data')?.addEventListener('click', async () => {
        if (confirm('Regenerate official student dataset with 500 records?')) {
            const res = await fetch('/api/regenerate', { method: 'POST' });
            const data = await res.json();
            showToast(data.message || 'Dataset regenerated', 'success');
            loadAdminPortal();
            loadStudentsTable();
        }
    });

    document.getElementById('btn-refresh-report')?.addEventListener('click', async () => {
        const res = await fetch('/api/generate-report', { method: 'POST' });
        const data = await res.json();
        showToast(data.message || 'Report regenerated', 'success');
        loadAcademicReport();
    });
}

async function deleteStudent(studentId) {
    if (confirm(`Are you sure you want to delete student ${studentId}?`)) {
        try {
            const res = await fetch(`/api/student/${studentId}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                showToast(data.message || 'Student deleted', 'success');
                loadStudentsTable();
            }
        } catch (e) {
            showToast('Error deleting student', 'error');
        }
    }
}

function openLightbox(src, title) {
    document.getElementById('lightbox-img').src = src;
    document.getElementById('lightbox-title').innerText = title;
    document.getElementById('image-lightbox-modal').classList.add('active');
}

function initFiltersAndPagination() {
    document.getElementById('btn-apply-filters')?.addEventListener('click', () => {
        currentPage = 1;
        loadStudentsTable();
    });

    document.getElementById('btn-reset-filters')?.addEventListener('click', () => {
        document.getElementById('search-input').value = '';
        document.getElementById('filter-branch').value = 'All';
        document.getElementById('filter-grade').value = 'All';
        document.getElementById('filter-status').value = 'All';
        currentPage = 1;
        loadStudentsTable();
    });

    document.getElementById('search-input')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            currentPage = 1;
            loadStudentsTable();
        }
    });

    document.getElementById('btn-prev-page')?.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadStudentsTable();
        }
    });

    document.getElementById('btn-next-page')?.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadStudentsTable();
        }
    });
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? 'fa-circle-check' : type === 'error' ? 'fa-circle-xmark' : 'fa-circle-info';
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 250);
    }, 3500);
}


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
            if (targetId === 'proctor-assignments-view') loadFacultyAssignments(facId);
    loadFacultyPendingMeetings(facId);
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
        if (document.getElementById('prof-mentor-name')) document.getElementById('prof-mentor-name').innerText = p.mentor_name || 'Dr. A. K. Sharma';
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


// Universal Global Modal Handlers
window.openModal = function(modalId) {
    const el = document.getElementById(modalId);
    if (el) {
        el.classList.add('active');
        el.style.display = 'flex';
    }
};

window.closeModal = function(modalId) {
    const el = document.getElementById(modalId);
    if (el) {
        el.classList.remove('active');
        el.style.display = 'none';
    }
};

// Close modal on click outside content
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal') || e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        e.target.style.display = 'none';
    }
});

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active, .modal-overlay.active').forEach(m => {
            m.classList.remove('active');
            m.style.display = 'none';
        });
    }
});


// ==============================================================================
// 13. MOBILE NAVIGATION DRAWER & TOUCH CONTROLLERS
// ==============================================================================

function initMobileNavigationDrawer() {
    const toggleBtn = document.getElementById('btn-mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');

    function openSidebar() {
        if (sidebar) sidebar.classList.add('open');
        if (backdrop) backdrop.classList.add('active');
    }

    function closeSidebar() {
        if (sidebar) sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('active');
    }

    toggleBtn?.addEventListener('click', (e) => {
        e.stopPropagation();
        if (sidebar?.classList.contains('open')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });

    backdrop?.addEventListener('click', closeSidebar);

    // Auto-close sidebar on mobile when navigating
    document.addEventListener('click', (e) => {
        const navItem = e.target.closest('.nav-item');
        if (navItem && window.innerWidth <= 992) {
            closeSidebar();
        }
    });
}

// 14. ASSIGNMENTS SUBMISSION & CORRESPONDENT FACULTY ROUTING ENGINE
// ==============================================================================

let currentAvailableAssignments = [];
let currentSubmissionsList = [];
let currentModalSelectedFile = null;
let currentFilterMode = 'all';

// --- A. Interactive Motionable Cursor Engine (Official Aditya "A" Logo - Unique & Small) ---
function initMotionCursor() {
    const dot = document.getElementById('cursor-precision-dot');
    const motionCursor = document.getElementById('aditya-motion-cursor');
    if (!dot || !motionCursor || window.matchMedia('(pointer: coarse)').matches) return;

    let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
    let cursorX = mouseX, cursorY = mouseY;
    let isMoving = false;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        if (!isMoving) {
            isMoving = true;
            document.body.classList.remove('cursor-hidden');
        }
        dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
    });

    document.addEventListener('mouseleave', () => {
        document.body.classList.add('cursor-hidden');
    });

    document.addEventListener('mouseenter', () => {
        document.body.classList.remove('cursor-hidden');
    });

    function loopMotionCursor() {
        cursorX += (mouseX - cursorX) * 0.22;
        cursorY += (mouseY - cursorY) * 0.22;
        motionCursor.style.transform = `translate(${cursorX}px, ${cursorY}px) translate(-50%, -50%)`;
        requestAnimationFrame(loopMotionCursor);
    }
    requestAnimationFrame(loopMotionCursor);

    // Dynamic Hover expansion for interactive UI elements
    document.addEventListener('mouseover', (e) => {
        const interactive = e.target.closest('button, a, input, select, textarea, .nav-item, .panel-card, .asg-clean-card, .quick-chip, .role-tab, .asg-filter-pill, .proctor-sub-btn, tr, .clickable');
        if (interactive) {
            document.body.classList.add('cursor-hover');
        }
    });

    document.addEventListener('mouseout', (e) => {
        const interactive = e.target.closest('button, a, input, select, textarea, .nav-item, .panel-card, .asg-clean-card, .quick-chip, .role-tab, .asg-filter-pill, .proctor-sub-btn, tr, .clickable');
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
        'Python Programming': { bg: '#eff6ff', border: '#bfdbfe', text: '#1e40af', accent: '#2563eb' },
        'Data Structures': { bg: '#f5f3ff', border: '#ddd6fe', text: '#5b21b6', accent: '#7c3aed' },
        'Mathematics': { bg: '#f0fdf4', border: '#bbf7d0', text: '#166534', accent: '#059669' },
        'Physics': { bg: '#fffbeb', border: '#fde68a', text: '#92400e', accent: '#d97706' },
        'English': { bg: '#fff1f2', border: '#fecdd3', text: '#9f1239', accent: '#e11d48' }
    };

    grid.innerHTML = displayList.map(a => {
        const sub = submittedMap[a.id];
        const isSubmitted = !!sub;
        const isGraded = isSubmitted && sub.status === 'Graded';
        
        const colors = subjectColors[a.subject] || { bg: '#f8fafc', border: '#cbd5e1', text: '#0f172a', accent: '#1e3a8a' };

        let statusBadgeHtml = '';
        let actionBtnHtml = '';

        if (!isSubmitted) {
            statusBadgeHtml = '<span class="badge badge-warning" style="font-size:11.5px; font-weight:700;"><i class="fa-solid fa-clock"></i> Pending Submission</span>';
            actionBtnHtml = `<button class="btn btn-primary" onclick="openAssignmentModal('${a.id}')" style="background:linear-gradient(135deg, #1e40af, #2563eb); color:#fff; box-shadow:0 4px 12px rgba(37,99,235,0.25);"><i class="fa-solid fa-cloud-arrow-up"></i> Submit Assignment</button>`;
        } else if (isGraded) {
            statusBadgeHtml = `<span class="badge badge-success" style="font-size:11.5px; font-weight:700;"><i class="fa-solid fa-circle-check"></i> Graded: ${sub.marks}</span>`;
            actionBtnHtml = `<button class="btn btn-outline" onclick="scrollToSubmissions()" style="border:1.5px solid #10b981; color:#047857; background:#ecfdf5; font-weight:700;"><i class="fa-solid fa-eye"></i> View Feedback & Document</button>`;
        } else {
            statusBadgeHtml = '<span class="badge badge-info" style="font-size:11.5px; font-weight:700;"><i class="fa-solid fa-spinner fa-spin"></i> Submitted (Under Review)</span>';
            actionBtnHtml = `<button class="btn btn-outline" onclick="scrollToSubmissions()" style="border:1.5px solid #3b82f6; color:#1d4ed8; background:#eff6ff; font-weight:700;"><i class="fa-solid fa-file-lines"></i> View Submission</button>`;
        }

        return `
            <div class="asg-clean-card" style="border-top: 4px solid ${colors.accent};">
                <div>
                    <div class="asg-card-top-row">
                        <span class="asg-course-badge" style="background:${colors.bg}; border:1.5px solid ${colors.border}; color:${colors.text}; font-weight:800;">
                            ${a.course_code} • ${a.subject}
                        </span>
                        <span class="asg-marks-badge">
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
                        <span><i class="fa-solid fa-calendar-day text-amber"></i> Due: <strong style="color:#0f172a;">${a.due_date}</strong></span>
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

// --- C. Faculty Assignments & Submissions Desk ---
let currentFacultySubmissions = [];

async function loadFacultyAssignments(facultyId) {
    const fId = facultyId || currentUser?.id || '50101';
    try {
        const res = await fetch(`/api/faculty/assignments/${fId}`);
        const data = await res.json();
        currentFacultySubmissions = data.submissions || [];
        
        renderFacultySubmissionsTable('faculty-submissions-tbody');
        renderFacultySubmissionsTable('proctor-asg-submissions-tbody');
        
        const countBadge = document.getElementById('faculty-asg-pending-count');
        if (countBadge) {
            const pendingCount = currentFacultySubmissions.filter(s => s.status !== 'Graded').length;
            countBadge.innerText = `${pendingCount} Submissions Awaiting Evaluation`;
        }
    } catch(e) {
        console.error('Error loading faculty assignments:', e);
    }
}

function renderFacultySubmissionsTable(tbodyId) {
    const tbody = document.getElementById(tbodyId);
    if (!tbody) return;

    if (currentFacultySubmissions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted p-4"><i class="fa-solid fa-folder-open fa-2x mb-2 text-primary"></i><br>No assignment submissions received yet.</td></tr>';
        return;
    }

    tbody.innerHTML = currentFacultySubmissions.map(s => {
        const isGraded = s.status === 'Graded';
        const statusBadge = isGraded 
            ? '<span class="badge badge-success"><i class="fa-solid fa-check-circle"></i> Graded & Verified</span>'
            : '<span class="badge badge-warning"><i class="fa-solid fa-clock"></i> Pending Evaluation</span>';

        const isPdf = (s.file_format || '').toLowerCase().includes('pdf') || (s.filename || '').endsWith('.pdf');
        const fileIcon = isPdf ? 'fa-file-pdf text-danger' : 'fa-file-word text-primary';
        const fileLink = s.file_url ? `<a href="${s.file_url}" target="_blank" class="btn btn-sm btn-outline" style="font-size:11px; padding:3px 7px;"><i class="fa-solid fa-arrow-down"></i> View File</a>` : '';

        return `
            <tr>
                <td>
                    <strong style="color:#0f172a;">${s.student_name || 'Student'}</strong><br>
                    <code style="font-size:11px; color:#1e40af; font-weight:700;">${s.student_id}</code>
                </td>
                <td>
                    <strong style="color:#0f172a;">${s.subject}</strong><br>
                    <span style="font-size:12px; color:#475569;">${s.title}</span>
                </td>
                <td>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <i class="fa-solid ${fileIcon} fa-lg"></i>
                        <div>
                            <strong style="color:#0f172a; font-size:12.5px;">${s.filename}</strong><br>
                            <small class="text-muted">${s.file_size || 'Document'}</small>
                        </div>
                        ${fileLink}
                    </div>
                </td>
                <td><span style="font-size:12px; color:#334155; font-weight:600;">${s.submitted_at}</span></td>
                <td>${statusBadge}</td>
                <td>
                    <strong style="font-size:13.5px; color:${isGraded ? '#15803d' : '#b45309'};">
                        ${s.marks || 'Pending'}
                    </strong>
                </td>
                <td>
                    <span style="font-size:12px; color:#334155;">${s.faculty_remarks || 'Awaiting faculty evaluation'}</span>
                </td>
                <td>
                    <button class="btn btn-sm ${isGraded ? 'btn-outline' : 'btn-primary'}" onclick="openFacultyGradeModal('${s.id}')">
                        <i class="fa-solid fa-marker"></i> ${isGraded ? 'Edit Marks' : 'Evaluate'}
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

function openFacultyGradeModal(subId) {
    const sub = currentFacultySubmissions.find(s => s.id === subId);
    if (!sub) return;

    document.getElementById('grade-submission-id-val').value = sub.id;
    document.getElementById('grade-modal-student-name').innerText = sub.student_name || 'Mukundha';
    document.getElementById('grade-modal-student-id').innerText = sub.student_id;
    document.getElementById('grade-modal-subject').innerText = sub.subject;
    document.getElementById('grade-modal-asg-title').innerText = sub.title;
    document.getElementById('grade-modal-filename').innerText = sub.filename;
    document.getElementById('grade-modal-marks-input').value = sub.marks && sub.marks !== 'Pending' ? sub.marks : '28/30';
    document.getElementById('grade-modal-remarks-input').value = sub.faculty_remarks && !sub.faculty_remarks.includes('routed') ? sub.faculty_remarks : 'Well structured submission meeting all rubric parameters.';

    const linkWrap = document.getElementById('grade-modal-doc-link-wrap');
    if (linkWrap) {
        linkWrap.innerHTML = sub.file_url ? `<a href="${sub.file_url}" target="_blank" class="btn btn-sm btn-outline"><i class="fa-solid fa-arrow-up-right-from-square"></i> Open File</a>` : '';
    }

    openModal('modal-faculty-grade-asg');
}

function initFacultyGradeFormEvents() {
    const form = document.getElementById('form-faculty-grade-asg');
    if (!form || form.dataset.bound) return;
    form.dataset.bound = 'true';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const subId = document.getElementById('grade-submission-id-val').value;
        const marks = document.getElementById('grade-modal-marks-input').value.trim();
        const remarks = document.getElementById('grade-modal-remarks-input').value.trim();
        const facId = currentUser?.id || '50101';

        try {
            const btn = document.getElementById('btn-save-faculty-grade');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

            const res = await fetch('/api/faculty/grade-assignment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    faculty_id: facId,
                    submission_id: subId,
                    marks: marks,
                    remarks: remarks
                })
            });
            const data = await res.json();
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-check-double"></i> <span>Submit Grade & Notify Student</span>';

            if (data.success) {
                showToast('Marks awarded & student notified successfully!', 'success');
                closeModal('modal-faculty-grade-asg');
                loadFacultyAssignments(facId);
            } else {
                showToast(data.message || 'Failed to submit grade', 'danger');
            }
        } catch(err) {
            showToast('Network error submitting grade', 'danger');
        }
    });
}

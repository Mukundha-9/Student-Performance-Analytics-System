# build_js.py
part1 = """/**
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
    initStudentPortalEvents();
    initFacultyPortalEvents();
    initAdminPortalEvents();
    initModals();
    initFiltersAndPagination();
    initSimulator();
    initAIAdvisor();

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

// Theme Switcher
function initTheme() {
    const toggleBtn = document.getElementById('theme-toggle-btn');
    const savedTheme = localStorage.getItem('aditya-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    toggleBtn?.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('aditya-theme', newTheme);
        updateThemeIcon(newTheme);
        showToast(`Switched to ${newTheme.toUpperCase()} mode`, 'info');
    });
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if (icon) icon.className = theme === 'light' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
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
        chips = [
            { id: '25B11CS380', label: 'Mukundha (Lead)' },
            { id: '25B11CS932', label: 'Sai Abhiram' },
            { id: '25B11CS490', label: 'Sameer Reddy' },
            { id: '25B11CS891', label: 'Shaik Sajid' }
        ];
    } else if (role === 'faculty') {
        chips = [
            { id: '50101', label: '50101 (Dr. Sharma)' },
            { id: '50102', label: '50102 (Prof. Priya)' },
            { id: '50103', label: '50103 (Dr. Venkatesh)' }
        ];
    } else {
        chips = [
            { id: '90001', label: '90001 (Registrar Office)' },
            { id: 'admin', label: 'admin (Super Controller)' }
        ];
    }

    chips.forEach(c => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'quick-chip';
        btn.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${c.label}`;
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
        showToast('Signed out of university portal', 'info');
    };

    topLogout?.addEventListener('click', handleLogout);
    sideLogout?.addEventListener('click', handleLogout);
}
"""

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(part1)
print('Generated app.js Part 1 with dedicated Login logic')

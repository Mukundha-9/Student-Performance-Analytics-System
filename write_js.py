# Helper to write static/js/app.js cleanly
import os

part1 = """/**
 * Aditya University - Student Performance Analytics & Multi-Portal System
 * Supports Student Portal | Faculty Portal | University Admin Portal
 */

// Application State
let currentRole = 'student'; // 'student' | 'faculty' | 'admin'
let currentUser = {
    id: '25B11CS380',
    name: 'Kalyanam Mukundha',
    role: 'student',
    branch: 'Computer Science & Engineering',
    semester: 'Semester 4'
};
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
    initRoleSwitcher();
    initStudentPortalEvents();
    initFacultyPortalEvents();
    initAdminPortalEvents();
    initModals();
    initFiltersAndPagination();
    initSimulator();
    initAIAdvisor();

    // Load initial Student Role
    setPortalRole('student', '25B11CS380');
    loadDemoUsersList();
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

// Role Switching System
function initRoleSwitcher() {
    const openBtn = document.getElementById('btn-open-role-switcher');
    const quickBtn = document.getElementById('btn-quick-switch');
    const closeBtn = document.getElementById('btn-close-role-modal');
    const modal = document.getElementById('role-switcher-modal');

    openBtn?.addEventListener('click', () => modal.classList.add('active'));
    quickBtn?.addEventListener('click', () => modal.classList.add('active'));
    closeBtn?.addEventListener('click', () => modal.classList.remove('active'));

    document.querySelectorAll('.role-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.role-tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.demo-profiles-container').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const role = btn.getAttribute('data-role');
            if (role === 'student') document.getElementById('demo-students-view').classList.add('active');
            if (role === 'faculty') document.getElementById('demo-faculty-view').classList.add('active');
            if (role === 'admin') document.getElementById('demo-admin-view').classList.add('active');
        });
    });
}

async function loadDemoUsersList() {
    try {
        const res = await fetch('/api/auth/demo-users');
        const data = await res.json();

        // Students Demo
        const sList = document.getElementById('demo-students-list');
        if (sList && data.students) {
            sList.innerHTML = '';
            data.students.forEach(s => {
                const card = document.createElement('div');
                card.className = 'demo-profile-card';
                card.onclick = () => loginAsRole('student', s.id);
                card.innerHTML = `
                    <div class="demo-avatar"><i class="fa-solid fa-user-graduate"></i></div>
                    <div class="demo-info">
                        <h4>${s.name}</h4>
                        <span>Roll: ${s.id}</span>
                        <small class="text-success">${s.score}</small>
                    </div>
                `;
                sList.appendChild(card);
            });
        }

        // Faculty Demo
        const fList = document.getElementById('demo-faculty-list');
        if (fList && data.faculties) {
            fList.innerHTML = '';
            data.faculties.forEach(f => {
                const card = document.createElement('div');
                card.className = 'demo-profile-card';
                card.onclick = () => loginAsRole('faculty', f.id);
                card.innerHTML = `
                    <div class="demo-avatar" style="background:#f59e0b; color:#ffffff;"><i class="fa-solid fa-chalkboard-user"></i></div>
                    <div class="demo-info">
                        <h4>${f.name}</h4>
                        <span>${f.id} • ${f.dept}</span>
                        <small class="text-warning">${f.designation}</small>
                    </div>
                `;
                fList.appendChild(card);
            });
        }
    } catch (e) {
        console.error('Error loading demo profiles:', e);
    }
}

async function loginAsRole(role, userId, password = '') {
    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role, username: userId, password })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('role-switcher-modal').classList.remove('active');
            setPortalRole(role, userId, data.user);
            showToast(data.message, 'success');
        }
    } catch (e) {
        showToast('Login failed', 'error');
    }
}
"""

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(part1)
print('Wrote app.js Part 1')

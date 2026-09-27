import re

# 1. Update templates/index.html
with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

login_btn_html = """        <!-- Floating Theme Switcher on Login Screen -->
        <div class="login-theme-switch-wrap">
            <button type="button" class="theme-toggle-btn login-theme-toggle" id="login-theme-toggle-btn" title="Toggle Light / Dark Mode">
                <i class="fa-solid fa-moon" id="login-theme-icon"></i>
                <span id="login-theme-label">Light Mode</span>
            </button>
        </div>
"""

if 'id="login-theme-toggle-btn"' not in html:
    html = html.replace('<div class="login-card-container">', login_btn_html + '        <div class="login-card-container">')
    print("Added login theme switch button")

old_theme_btn = """                    <button class="theme-toggle-btn" id="theme-toggle-btn" title="Toggle Dark/Light Mode">
                        <i class="fa-solid fa-sun" id="theme-icon"></i>
                    </button>"""

new_theme_btn = """                    <button class="theme-toggle-btn" id="theme-toggle-btn" title="Toggle Dark/Light Mode">
                        <i class="fa-solid fa-sun" id="theme-icon"></i>
                        <span class="theme-btn-text" id="navbar-theme-label">Light Mode</span>
                    </button>"""

if old_theme_btn in html:
    html = html.replace(old_theme_btn, new_theme_btn)
    print("Updated navbar theme button")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)


# 2. Append Comprehensive Luxury Light Theme CSS to static/css/style.css
light_theme_css = """

/* ==========================================================================
   COMPREHENSIVE LUXURY LIGHT & DARK THEME ENGINE
   ========================================================================== */

/* Theme Toggle Button Styles */
.theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #fbbf24;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.theme-toggle-btn:hover {
    transform: translateY(-1px);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
}

.login-theme-switch-wrap {
    position: absolute;
    top: 24px;
    right: 28px;
    z-index: 50;
}
.login-theme-toggle {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
}

/* --------------------------------------------------------------------------
   COMPLETE LIGHT THEME OVERRIDES ([data-theme="light"])
   -------------------------------------------------------------------------- */

[data-theme="light"] {
    --bg-main: #f8fafc;
    --bg-card: #ffffff;
    --bg-card-hover: #f1f5f9;
    --bg-sidebar: #ffffff;
    --border-color: #e2e8f0;
    --border-light: #cbd5e1;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
    
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #3b82f6;
    --primary-glow: rgba(37, 99, 235, 0.12);
}

[data-theme="light"] body {
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

[data-theme="light"] .theme-toggle-btn {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    color: #475569 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
}
[data-theme="light"] .theme-toggle-btn:hover {
    background: #f1f5f9 !important;
    color: #1e40af !important;
    border-color: #94a3b8 !important;
}
[data-theme="light"] .theme-toggle-btn i {
    color: #2563eb !important;
}

/* Login Screen in Light Theme */
[data-theme="light"] .login-gateway-wrapper {
    background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 45%, #e2e8f0 100%) !important;
}
[data-theme="light"] .login-ambient-orb.orb-1 {
    background: #93c5fd !important;
    opacity: 0.35 !important;
}
[data-theme="light"] .login-ambient-orb.orb-2 {
    background: #c7d2fe !important;
    opacity: 0.35 !important;
}
[data-theme="light"] .login-ambient-orb.orb-3 {
    background: #a7f3d0 !important;
    opacity: 0.35 !important;
}
[data-theme="light"] .login-card-container {
    background: rgba(255, 255, 255, 0.94) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    box-shadow: 0 25px 60px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(226, 232, 240, 0.8) !important;
}
[data-theme="light"] .login-portal-title {
    color: #0f172a !important;
}
[data-theme="light"] .clean-form-label {
    color: #334155 !important;
}
[data-theme="light"] .login-role-tabs {
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .role-tab {
    color: #64748b !important;
}
[data-theme="light"] .role-tab.active {
    background: #ffffff !important;
    color: #1e40af !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08) !important;
    font-weight: 700 !important;
}
[data-theme="light"] .login-input,
[data-theme="light"] .form-input {
    background-color: #f8fafc !important;
    border: 1.5px solid #cbd5e1 !important;
    color: #0f172a !important;
}
[data-theme="light"] .login-input:focus,
[data-theme="light"] .form-input:focus {
    background-color: #ffffff !important;
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}
[data-theme="light"] .quick-chip {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    color: #334155 !important;
}
[data-theme="light"] .quick-chip:hover {
    background: #e2e8f0 !important;
    color: #1d4ed8 !important;
    border-color: #94a3b8 !important;
}
[data-theme="light"] .security-chip {
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
}
[data-theme="light"] .team-credits {
    color: #64748b !important;
}
[data-theme="light"] .btn-toggle-pw {
    color: #64748b !important;
}
[data-theme="light"] .input-icon {
    color: #64748b !important;
}

/* Sidebar in Light Theme */
[data-theme="light"] .sidebar {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 15px rgba(15, 23, 42, 0.03) !important;
}
[data-theme="light"] .brand-info h2 {
    color: #0f172a !important;
}
[data-theme="light"] .brand-info span {
    color: #2563eb !important;
}
[data-theme="light"] .user-role-badge {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] #badge-user-name {
    color: #0f172a !important;
}
[data-theme="light"] #badge-user-role {
    color: #64748b !important;
}
[data-theme="light"] .nav-item {
    color: #475569 !important;
}
[data-theme="light"] .nav-item:hover {
    background-color: #f1f5f9 !important;
    color: #1d4ed8 !important;
}
[data-theme="light"] .nav-item.active {
    background: linear-gradient(90deg, rgba(37, 99, 235, 0.12), rgba(37, 99, 235, 0.03)) !important;
    color: #1d4ed8 !important;
    border-left: 3px solid #2563eb !important;
    font-weight: 700 !important;
}
[data-theme="light"] .sidebar-footer {
    border-top: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .btn-switch-role {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
}
[data-theme="light"] .btn-switch-role:hover {
    background: #fee2e2 !important;
    color: #dc2626 !important;
    border-color: #fecaca !important;
}
[data-theme="light"] .app-version {
    color: #94a3b8 !important;
}

/* Top Navbar in Light Theme */
[data-theme="light"] .top-navbar {
    background-color: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04) !important;
}
[data-theme="light"] #top-portal-heading {
    color: #0f172a !important;
}
[data-theme="light"] #top-portal-sub {
    color: #64748b !important;
}
[data-theme="light"] .active-session-pill {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
}
[data-theme="light"] .btn-nav-action {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    color: #334155 !important;
}
[data-theme="light"] .btn-nav-action:hover {
    background: #fee2e2 !important;
    color: #dc2626 !important;
    border-color: #fecaca !important;
}

/* Panels, Cards & Sections */
[data-theme="light"] .panel-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05) !important;
}
[data-theme="light"] .panel-header h3 {
    color: #0f172a !important;
}
[data-theme="light"] .stat-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04) !important;
}
[data-theme="light"] .stat-label {
    color: #64748b !important;
}
[data-theme="light"] .stat-value {
    color: #0f172a !important;
}

/* KPI Summary Cards */
[data-theme="light"] .kpi-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05) !important;
}
[data-theme="light"] .kpi-card:hover {
    border-color: #2563eb !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12) !important;
}
[data-theme="light"] .kpi-data span {
    color: #64748b !important;
}
[data-theme="light"] .kpi-data h3 {
    color: #0f172a !important;
}
[data-theme="light"] .bg-blue {
    background: #eff6ff !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
}
[data-theme="light"] .bg-emerald {
    background: #ecfdf5 !important;
    color: #059669 !important;
    border: 1px solid #a7f3d0 !important;
}
[data-theme="light"] .bg-purple {
    background: #faf5ff !important;
    color: #7c3aed !important;
    border: 1px solid #e9d5ff !important;
}
[data-theme="light"] .bg-amber {
    background: #fffbeb !important;
    color: #d97706 !important;
    border: 1px solid #fde68a !important;
}

/* Subject Attendance Cards */
[data-theme="light"] .subject-att-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04) !important;
}
[data-theme="light"] .subject-att-card:hover {
    border-color: #2563eb !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12) !important;
}
[data-theme="light"] .subject-att-header h4 {
    color: #0f172a !important;
}
[data-theme="light"] .subject-att-faculty {
    color: #64748b !important;
}
[data-theme="light"] .att-progress-track {
    background: #e2e8f0 !important;
}
[data-theme="light"] .att-calculator-tag.tag-safe {
    background: #ecfdf5 !important;
    border: 1px solid #a7f3d0 !important;
    color: #059669 !important;
}
[data-theme="light"] .att-calculator-tag.tag-risk {
    background: #fef2f2 !important;
    border: 1px solid #fecaca !important;
    color: #dc2626 !important;
}
[data-theme="light"] .att-day-selector {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .att-day-btn {
    color: #64748b !important;
}
[data-theme="light"] .att-day-btn:hover {
    background: #f1f5f9 !important;
    color: #0f172a !important;
}
[data-theme="light"] .att-day-btn.active {
    background: #2563eb !important;
    color: #ffffff !important;
}
[data-theme="light"] .bunk-sim-result-box {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
}

/* Tables in Light Theme */
[data-theme="light"] .data-table th {
    background-color: #f8fafc !important;
    color: #475569 !important;
    border-bottom: 2px solid #e2e8f0 !important;
    font-weight: 700 !important;
}
[data-theme="light"] .data-table td {
    background-color: #ffffff !important;
    border-bottom: 1px solid #e2e8f0 !important;
    color: #1e293b !important;
}
[data-theme="light"] .data-table tbody tr:hover td {
    background-color: #f8fafc !important;
}
[data-theme="light"] code {
    background: #f1f5f9 !important;
    color: #1e40af !important;
    border: 1px solid #e2e8f0 !important;
}

/* Profile Section in Light Theme */
[data-theme="light"] .prof-detail-box {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .prof-label {
    color: #64748b !important;
}
[data-theme="light"] .prof-val {
    color: #0f172a !important;
}
[data-theme="light"] .prior-academic-box {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03) !important;
}
[data-theme="light"] .prior-header h4 {
    color: #0f172a !important;
}
[data-theme="light"] .prior-scores-grid strong {
    color: #0f172a !important;
}
[data-theme="light"] .sem-tabs-bar {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .sem-tab-btn {
    color: #64748b !important;
}
[data-theme="light"] .sem-tab-btn.active {
    background: #2563eb !important;
    color: #ffffff !important;
}
[data-theme="light"] .sem-summary-footer {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #0f172a !important;
}
[data-theme="light"] #prof-proctor-card-container {
    background: #fffbeb !important;
    border: 1px solid #fde68a !important;
}

/* Timetable & Faculty Cards in Light Theme */
[data-theme="light"] .timetable-day-selector {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .day-btn {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #64748b !important;
}
[data-theme="light"] .day-btn.active {
    background: #2563eb !important;
    color: #ffffff !important;
    border-color: #2563eb !important;
}
[data-theme="light"] .period-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
}
[data-theme="light"] .period-card h4 {
    color: #0f172a !important;
}
[data-theme="light"] .faculty-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
}
[data-theme="light"] .faculty-card h4 {
    color: #0f172a !important;
}

/* Notifications in Light Theme */
[data-theme="light"] .notifications-filter-bar {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .notif-filter-btn {
    color: #64748b !important;
}
[data-theme="light"] .notif-filter-btn.active {
    background: #2563eb !important;
    color: #ffffff !important;
}
[data-theme="light"] .notif-stream-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04) !important;
}
[data-theme="light"] .notif-card-header h4 {
    color: #0f172a !important;
}
[data-theme="light"] .notif-card-body {
    color: #334155 !important;
}

/* Modals in Light Theme */
[data-theme="light"] .modal-content,
[data-theme="light"] .modal-dialog {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: 0 25px 60px -15px rgba(15, 23, 42, 0.25) !important;
    color: #0f172a !important;
}
[data-theme="light"] .modal-header {
    background: #f8fafc !important;
    border-bottom: 1px solid #e2e8f0 !important;
}
[data-theme="light"] .modal-header h3 {
    color: #0f172a !important;
}
[data-theme="light"] .modal-footer {
    background: #f8fafc !important;
    border-top: 1px solid #e2e8f0 !important;
}

/* Charts in Light Theme */
[data-theme="light"] .chart-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05) !important;
}
[data-theme="light"] .chart-header h3 {
    color: #0f172a !important;
}

/* Matplotlib Gallery in Light Theme */
[data-theme="light"] .gallery-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05) !important;
}
[data-theme="light"] .gallery-card h4 {
    color: #0f172a !important;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(light_theme_css)

print("Appended luxury light theme CSS to static/css/style.css")


# ==============================================================================
# 3. Update static/js/app.js with Synchronized Theme Switching
# ==============================================================================

with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Replace initTheme() with unified synchronized theme switcher
old_init_theme = """function initTheme() {
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
}"""

new_init_theme = """function initTheme() {
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
}

function applyTheme(theme, showNotice = true) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('aditya-theme', theme);

    // Update Top Navbar Button
    const navIcon = document.getElementById('theme-icon');
    const navLabel = document.getElementById('navbar-theme-label');
    if (navIcon) navIcon.className = theme === 'light' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
    if (navLabel) navLabel.innerText = theme === 'light' ? 'Dark Mode' : 'Light Mode';

    // Update Login Screen Button
    const loginIcon = document.getElementById('login-theme-icon');
    const loginLabel = document.getElementById('login-theme-label');
    if (loginIcon) loginIcon.className = theme === 'light' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
    if (loginLabel) loginLabel.innerText = theme === 'light' ? 'Dark Mode' : 'Light Mode';

    if (showNotice) {
        showToast(`Switched to ${theme.toUpperCase()} Theme`, 'info');
    }

    // Refresh charts if rendered
    refreshChartsTheme();
}

function refreshChartsTheme() {
    if (currentRole === 'admin') {
        loadAdminPortal();
    } else if (currentRole === 'student') {
        if (currentTab === 'student-overview-tab') loadStudentOverview(currentUser?.id);
    }
}"""

if old_init_theme in js:
    js = js.replace(old_init_theme, new_init_theme)
    print("Replaced initTheme in app.js")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updated static/js/app.js with synchronized theme switcher")
print("ALL DONE!")

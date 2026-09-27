# make_mobile_responsive.py
import re

# 1. Clean and update templates/index.html
with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix duplicate head/body at start
clean_start = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Aditya University - Academic Analytics & Multi-Role Portal</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cinzel:wght@600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

    <!-- Backdrop Overlay for Mobile Sidebar Drawer -->
    <div class="sidebar-backdrop" id="sidebar-backdrop"></div>
"""

# Replace top part until login-gateway-wrapper
html = re.sub(r'<!DOCTYPE html>[\s\S]*?<!-- 1\. FULL-PAGE ULTRA-MODERN LOGIN GATEWAY -->', clean_start + '\n    <!-- 1. FULL-PAGE ULTRA-MODERN LOGIN GATEWAY -->', html)

# Add Mobile Hamburger Toggle inside top-navbar
old_navbar_left = """            <!-- TOP NAVBAR -->
            <header class="top-navbar">
                <div class="navbar-left">"""

new_navbar_left = """            <!-- TOP NAVBAR -->
            <header class="top-navbar">
                <div class="navbar-left">
                    <button class="mobile-menu-btn" id="btn-mobile-menu-toggle" aria-label="Toggle Navigation">
                        <i class="fa-solid fa-bars"></i>
                    </button>"""

if old_navbar_left in html:
    html = html.replace(old_navbar_left, new_navbar_left)
    print("Added mobile menu toggle button to navbar")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated templates/index.html with mobile drawer and clean markup")

# 2. Append Mobile Responsive CSS to static/css/style.css
mobile_css = """

/* ==========================================================================
   COMPLETE COMPREHENSIVE MOBILE & TABLET RESPONSIVE STYLES
   ========================================================================== */

/* Mobile Hamburger Button */
.mobile-menu-btn {
    display: none;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    font-size: 18px;
    cursor: pointer;
    margin-right: 10px;
    flex-shrink: 0;
    transition: var(--transition);
}
.mobile-menu-btn:hover {
    background: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
}

/* Sidebar Backdrop on Mobile */
.sidebar-backdrop {
    display: none;
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(2, 6, 23, 0.7);
    backdrop-filter: blur(4px);
    z-index: 998;
}
.sidebar-backdrop.active {
    display: block;
}

/* Tablet & Mobile Breakpoints (<= 992px) */
@media (max-width: 992px) {
    .mobile-menu-btn {
        display: flex !important;
    }

    .sidebar {
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 280px !important;
        max-width: 85vw !important;
        z-index: 999 !important;
        transform: translateX(-100%) !important;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 10px 0 35px rgba(0, 0, 0, 0.6) !important;
    }

    .sidebar.open {
        transform: translateX(0) !important;
    }

    .main-content {
        margin-left: 0 !important;
        max-width: 100vw !important;
        width: 100% !important;
        padding: 14px 14px 80px 14px !important;
        box-sizing: border-box !important;
    }

    .top-navbar {
        padding: 10px 14px !important;
        gap: 8px !important;
    }

    .portal-title-tag {
        font-size: 12px !important;
    }
    #top-portal-sub {
        display: none !important;
    }

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
    }

    .grid-2-columns, .charts-grid-2, .profile-details-grid {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
    }

    .profile-hero-card {
        flex-direction: column !important;
        text-align: center !important;
        padding: 18px !important;
    }
    .profile-hero-info {
        width: 100% !important;
    }
    .profile-badges-row {
        justify-content: center !important;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
    }

    .welcome-hero-card {
        flex-direction: column !important;
        gap: 14px !important;
        padding: 18px !important;
    }
    .hero-stats {
        width: 100% !important;
        justify-content: space-between !important;
    }
    .hero-stat-box {
        flex: 1 !important;
        min-width: 0 !important;
        padding: 10px 8px !important;
    }
}

/* Small Smartphone Breakpoints (<= 576px) */
@media (max-width: 576px) {
    .kpi-grid {
        grid-template-columns: 1fr !important;
    }

    .stats-grid {
        grid-template-columns: 1fr !important;
    }

    .login-card-container {
        padding: 22px 16px !important;
        border-radius: 16px !important;
    }

    .login-main-logo {
        height: 60px !important;
        max-width: 180px !important;
    }

    .role-tab {
        padding: 7px 4px !important;
        font-size: 11px !important;
    }

    .quick-chips-row {
        flex-direction: column !important;
        gap: 6px !important;
    }
    .quick-chip {
        width: 100% !important;
        justify-content: center !important;
    }

    .active-session-pill {
        display: none !important;
    }

    .subject-attendance-grid {
        grid-template-columns: 1fr !important;
    }

    .table-responsive {
        width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        display: block !important;
    }

    .sem-tabs-bar, .att-day-selector, .timetable-day-selector, .notifications-filter-bar {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        flex-wrap: nowrap !important;
        padding-bottom: 6px !important;
    }

    .proctor-hero-card {
        grid-template-columns: 1fr !important;
        text-align: center !important;
    }
    .proctor-avatar {
        margin: 0 auto !important;
    }
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(mobile_css)

print("Appended comprehensive mobile responsive rules to static/css/style.css")

# 3. Add Mobile Navigation Drawer event handlers in static/js/app.js
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

mobile_nav_js = """

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
"""

if "initMobileNavigationDrawer" not in js:
    js += mobile_nav_js
    js = js.replace("initBunkSimulatorEvents();", "initBunkSimulatorEvents();\n    initMobileNavigationDrawer();")
    with open("static/js/app.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Injected mobile navigation drawer controller into static/js/app.js")

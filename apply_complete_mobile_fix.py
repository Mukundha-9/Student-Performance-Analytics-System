# apply_complete_mobile_fix.py
import re

# ==============================================================================
# 1. Update static/css/style.css with Flawless Universal Mobile Rules
# ==============================================================================

with open("static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# Add universal mobile reset & comprehensive responsive styles
master_mobile_css = """

/* ==========================================================================
   MASTER FLAWLESS MOBILE & TABLET RESPONSIVE ENGINE (ZERO CUTTING / OVERFLOW)
   ========================================================================== */

/* Universal Box-Sizing & Viewport Containment */
html, body {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    position: relative !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 !important;
    -webkit-text-size-adjust: 100% !important;
}

*, *::before, *::after {
    box-sizing: border-box !important;
}

/* Touch-Friendly Horizontal Scrolling Containers */
.table-responsive {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    display: block !important;
    margin-bottom: 12px !important;
    border-radius: 8px !important;
}

.table-responsive::-webkit-scrollbar {
    height: 5px;
}
.table-responsive::-webkit-scrollbar-thumb {
    background: rgba(59, 130, 246, 0.4);
    border-radius: 4px;
}

.data-table {
    min-width: 580px !important;
    width: 100% !important;
}

.sem-tabs-bar,
.att-day-selector,
.timetable-day-selector,
.notifications-filter-bar,
.proctor-subnav-bar,
.quick-chips-row {
    display: flex !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    flex-wrap: nowrap !important;
    white-space: nowrap !important;
    width: 100% !important;
    max-width: 100% !important;
    padding-bottom: 6px !important;
    gap: 6px !important;
}

.sem-tabs-bar::-webkit-scrollbar,
.att-day-selector::-webkit-scrollbar,
.timetable-day-selector::-webkit-scrollbar,
.notifications-filter-bar::-webkit-scrollbar,
.proctor-subnav-bar::-webkit-scrollbar {
    height: 4px;
}
.sem-tabs-bar::-webkit-scrollbar-thumb,
.att-day-selector::-webkit-scrollbar-thumb,
.timetable-day-selector::-webkit-scrollbar-thumb,
.notifications-filter-bar::-webkit-scrollbar-thumb,
.proctor-subnav-bar::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 4px;
}

/* Base Container Safety on Mobile */
.app-container,
.main-content,
.content-body,
.tab-content,
.panel-card,
.kpi-grid,
.grid-2-columns,
.charts-grid-2,
.profile-details-grid,
.stats-grid,
.subject-attendance-grid,
.welcome-hero-card,
.profile-hero-card,
.proctor-hero-card,
.fee-summary-grid,
.gallery-grid {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    min-width: 0 !important;
}

/* Tablet & Mobile Screens (<= 992px) */
@media (max-width: 992px) {
    /* Mobile Drawer */
    .mobile-menu-btn {
        display: inline-flex !important;
    }

    .sidebar {
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 280px !important;
        max-width: 82vw !important;
        z-index: 10000 !important;
        transform: translateX(-105%) !important;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 15px 0 40px rgba(0, 0, 0, 0.7) !important;
        background: #090e1a !important;
    }

    .sidebar.open {
        transform: translateX(0) !important;
    }

    .sidebar-backdrop {
        position: fixed !important;
        inset: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: rgba(2, 6, 23, 0.75) !important;
        backdrop-filter: blur(5px) !important;
        z-index: 9999 !important;
        display: none !important;
    }
    .sidebar-backdrop.active {
        display: block !important;
    }

    .main-content {
        margin-left: 0 !important;
        max-width: 100vw !important;
        width: 100% !important;
        padding: 12px 12px 80px 12px !important;
    }

    /* Top Navbar */
    .top-navbar {
        padding: 8px 12px !important;
        gap: 6px !important;
    }
    .portal-title-tag {
        font-size: 11.5px !important;
    }
    #top-portal-sub {
        display: none !important;
    }
    .active-session-pill {
        display: none !important;
    }
    .btn-nav-action span {
        display: none !important;
    }
    .btn-nav-action {
        padding: 6px 10px !important;
    }

    /* Grids & Cards */
    .grid-2-columns,
    .charts-grid-2,
    .profile-details-grid,
    .fee-summary-grid {
        grid-template-columns: 1fr !important;
        gap: 12px !important;
    }

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
    }

    .subject-attendance-grid {
        grid-template-columns: 1fr !important;
        gap: 12px !important;
    }

    .gallery-grid {
        grid-template-columns: 1fr !important;
        gap: 16px !important;
    }

    /* Hero Cards */
    .welcome-hero-card {
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 16px !important;
        gap: 14px !important;
    }
    .hero-stats {
        width: 100% !important;
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
    }
    .hero-stat-box {
        width: 100% !important;
        min-width: 0 !important;
        padding: 10px 12px !important;
    }

    .profile-hero-card {
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        padding: 18px 14px !important;
        gap: 12px !important;
    }
    .profile-hero-info {
        width: 100% !important;
    }
    .profile-badges-row {
        justify-content: center !important;
    }

    .proctor-hero-card {
        grid-template-columns: 1fr !important;
        text-align: center !important;
        padding: 16px !important;
        gap: 12px !important;
    }
    .proctor-avatar {
        margin: 0 auto !important;
    }
    .proctor-hero-card button {
        width: 100% !important;
    }

    /* Prior Academics */
    .prior-scores-grid {
        grid-template-columns: 1fr !important;
        gap: 8px !important;
    }

    /* Modals on Mobile */
    .modal, .modal-overlay {
        padding: 10px !important;
    }
    .modal-content, .modal-dialog {
        width: 95vw !important;
        max-width: 95vw !important;
        margin: auto !important;
        border-radius: 12px !important;
    }
    .modal-body {
        padding: 16px 14px !important;
        max-height: 70vh !important;
    }
    .modal-header {
        padding: 14px 16px !important;
    }
    .modal-footer {
        padding: 12px 16px !important;
    }

    /* Filter Toolbars */
    .filter-bar, .filter-toolbar {
        flex-direction: column !important;
        gap: 8px !important;
    }
    .filter-bar .form-group, .filter-toolbar .form-group {
        width: 100% !important;
    }
    .filter-bar button, .filter-toolbar button {
        width: 100% !important;
    }

    /* Forms */
    .form-row, .form-grid-2, .form-grid-3, .form-grid-5 {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
    }

    /* Report Markdown Body */
    .report-document-body > div {
        padding: 16px 14px !important;
    }
    .report-document-body h1 {
        font-size: 19px !important;
    }
    .report-document-body h2 {
        font-size: 16px !important;
    }
    .report-document-body h3 {
        font-size: 14px !important;
    }
}

/* Smartphone Screens (<= 576px) */
@media (max-width: 576px) {
    .kpi-grid {
        grid-template-columns: 1fr !important;
        gap: 8px !important;
    }
    .kpi-card {
        padding: 14px !important;
        gap: 12px !important;
    }
    .kpi-icon-wrap {
        width: 44px !important;
        height: 44px !important;
        font-size: 18px !important;
    }
    .kpi-data h3 {
        font-size: 20px !important;
    }

    .stats-grid {
        grid-template-columns: 1fr !important;
    }

    .login-card-container {
        padding: 20px 14px !important;
        border-radius: 16px !important;
    }
    .login-main-logo {
        height: 55px !important;
        max-width: 160px !important;
    }
    .login-portal-title {
        font-size: 12.5px !important;
    }
    .role-tab {
        padding: 7px 4px !important;
        font-size: 11px !important;
        gap: 4px !important;
    }

    .quick-chips-row {
        flex-direction: column !important;
        gap: 5px !important;
    }
    .quick-chip {
        width: 100% !important;
        font-size: 11px !important;
        padding: 6px 8px !important;
        justify-content: center !important;
    }

    .btn-login-submit {
        padding: 11px !important;
        font-size: 13px !important;
    }

    .sem-summary-footer {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
    }

    .panel-card {
        padding: 14px !important;
        border-radius: 12px !important;
        margin-bottom: 14px !important;
    }
    .panel-header {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 6px !important;
    }

    .hero-stats {
        grid-template-columns: 1fr !important;
    }
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(master_mobile_css)

print("Injected Master Flawless Mobile Responsive Styles into static/css/style.css")

# Script to write templates/index.html cleanly
import os

part1 = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditya University - Student Performance Analytics & Multi-Role Portal</title>
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
    <div class="app-container">
        <!-- SIDEBAR NAVIGATION -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="brand-logo">
                    <i class="fa-solid fa-graduation-cap"></i>
                </div>
                <div class="brand-info">
                    <h2>ADITYA</h2>
                    <span>University Portal</span>
                </div>
            </div>

            <!-- Role Badge -->
            <div class="user-role-badge" id="sidebar-user-badge">
                <div class="user-avatar" id="badge-avatar"><i class="fa-solid fa-user-graduate"></i></div>
                <div class="user-details">
                    <h4 id="badge-user-name">Kalyanam Mukundha</h4>
                    <span id="badge-user-role">🎓 Student (25B11CS380)</span>
                </div>
            </div>

            <!-- Dynamic Role Menu -->
            <nav class="sidebar-nav" id="sidebar-navigation-menu">
                <!-- Injected via JavaScript based on role -->
            </nav>

            <div class="sidebar-footer">
                <button class="btn-switch-role" id="btn-open-role-switcher">
                    <i class="fa-solid fa-right-left"></i> Switch Portal Role
                </button>
                <div class="app-version">DAE Analytics Engine v3.0</div>
            </div>
        </aside>

        <!-- MAIN CONTENT WRAPPER -->
        <main class="main-content">
            <!-- TOP NAVBAR -->
            <header class="top-navbar">
                <div class="navbar-left">
                    <div class="portal-title-tag" id="top-portal-title-tag">
                        <span class="portal-indicator-dot"></span>
                        <strong id="top-portal-heading">🎓 STUDENT PORTAL</strong> &nbsp;|&nbsp;
                        <span id="top-portal-sub">Department of Computer Science & Engineering</span>
                    </div>
                </div>
                <div class="navbar-right">
                    <button class="theme-toggle-btn" id="theme-toggle-btn" title="Toggle Dark/Light Mode">
                        <i class="fa-solid fa-sun" id="theme-icon"></i>
                    </button>
                    <div class="active-session-pill" id="nav-session-pill">
                        <i class="fa-solid fa-circle-check text-success"></i>
                        <span id="nav-session-user">25B11CS380</span>
                    </div>
                    <button class="btn-nav-action" id="btn-quick-switch" title="Quick Switch Demo Role">
                        <i class="fa-solid fa-user-gear"></i> Demo Roles
                    </button>
                </div>
            </header>

            <!-- TAB CONTENT CONTAINER -->
            <div class="content-body">

                <!-- ============================================================== -->
                <!-- 1. STUDENT PORTAL TABS -->
                <!-- ============================================================== -->

                <!-- TAB: Student Overview & Grade Sheet -->
                <section class="tab-content active" id="student-overview-tab">
                    <div class="welcome-hero-card">
                        <div class="hero-info">
                            <span class="badge badge-primary" id="hero-branch-badge">Computer Science & Engineering</span>
                            <h2 id="hero-student-name">Welcome, Kalyanam Mukundha</h2>
                            <p id="hero-student-sub">B.Tech 2nd Year &nbsp;•&nbsp; Semester 4 &nbsp;•&nbsp; Academic Year 2025-2026</p>
                        </div>
                        <div class="hero-stats">
                            <div class="hero-stat-box">
                                <span>Overall Score</span>
                                <h3 id="hero-score-val">93.1%</h3>
                                <small class="text-success"><i class="fa-solid fa-award"></i> Grade A+</small>
                            </div>
                            <div class="hero-stat-box">
                                <span>Cohort Rank</span>
                                <h3 id="hero-rank-val">#81</h3>
                                <small class="text-info">Top 16.2%</small>
                            </div>
                            <div class="hero-stat-box">
                                <span>Attendance</span>
                                <h3 id="hero-att-val">98.0%</h3>
                                <small class="text-success"><i class="fa-solid fa-circle-check"></i> Eligible</small>
                            </div>
                        </div>
                    </div>

                    <!-- 5-Axis Radar & Subject Marks Grid -->
                    <div class="grid-2-columns mt-3">
                        <div class="chart-card">
                            <div class="chart-header">
                                <h3><i class="fa-solid fa-spider"></i> My Academic Competency Radar</h3>
                                <span class="badge badge-info">5-Axis Analysis</span>
                            </div>
                            <div class="chart-body" style="height: 320px;">
                                <canvas id="chart-student-radar"></canvas>
                            </div>
                        </div>
                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-table-list"></i> Semester Marks Breakdown</h3>
                                <button class="btn btn-sm btn-outline" onclick="openStudentReportCard()"><i class="fa-solid fa-print"></i> Print Card</button>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table table-sm" id="student-marks-table">
                                    <thead>
                                        <tr>
                                            <th>Subject</th>
                                            <th>Marks</th>
                                            <th>Class Avg</th>
                                            <th>Z-Score</th>
                                            <th>Result</th>
                                        </tr>
                                    </thead>
                                    <tbody id="student-marks-tbody">
                                        <!-- Populated via JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </section>
"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(part1)
print('Wrote Part 1')

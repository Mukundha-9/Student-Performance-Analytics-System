# build_ui.py
part1 = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

    <!-- 1. FULL-PAGE ULTRA-MODERN LOGIN GATEWAY -->
    <div class="login-gateway-wrapper active" id="login-screen">
        <div class="login-ambient-orb orb-1"></div>
        <div class="login-ambient-orb orb-2"></div>
        <div class="login-ambient-orb orb-3"></div>

        <div class="login-card-container">
            <div class="login-branding-header">
                <div class="logo-aura-wrap">
                    <img src="/static/images/aditya_logo.png" alt="Aditya University" class="login-university-logo">
                </div>
                <h2>ADITYA UNIVERSITY</h2>
                <p class="login-subtitle">STUDENT PERFORMANCE ANALYTICS & ACADEMIC ERP GATEWAY</p>
                <div class="login-badge-dept">Department of Computer Science & Engineering • DAE Project</div>
            </div>

            <div class="login-role-tabs">
                <button class="role-tab active" data-login-role="student" id="tab-btn-student">
                    <i class="fa-solid fa-user-graduate"></i>
                    <span>Student Login</span>
                </button>
                <button class="role-tab" data-login-role="faculty" id="tab-btn-faculty">
                    <i class="fa-solid fa-chalkboard-user"></i>
                    <span>Faculty Login</span>
                </button>
                <button class="role-tab" data-login-role="admin" id="tab-btn-admin">
                    <i class="fa-solid fa-building-columns"></i>
                    <span>Admin Login</span>
                </button>
            </div>

            <form id="main-login-form" class="login-form-box">
                <div class="form-group mb-3">
                    <label id="login-id-label"><i class="fa-solid fa-id-card"></i> Student Roll Number</label>
                    <div class="input-icon-wrap">
                        <i class="fa-solid fa-user input-icon" id="login-user-icon"></i>
                        <input type="text" class="form-input login-input" id="login-username" value="25B11CS380" placeholder="e.g. 25B11CS380" required>
                    </div>
                </div>

                <div class="form-group mb-3">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <label><i class="fa-solid fa-lock"></i> Security Password</label>
                        <span class="pw-hint-tag">Password: <code>aditya@123</code></span>
                    </div>
                    <div class="input-icon-wrap">
                        <i class="fa-solid fa-key input-icon"></i>
                        <input type="password" class="form-input login-input" id="login-password" value="aditya@123" placeholder="Enter password..." required>
                        <button type="button" class="btn-toggle-pw" id="btn-toggle-password" title="Show / Hide Password">
                            <i class="fa-solid fa-eye" id="eye-icon"></i>
                        </button>
                    </div>
                </div>

                <div class="quick-credentials-box">
                    <span class="quick-title"><i class="fa-solid fa-bolt text-warning"></i> 1-Click Quick Demo Profiles:</span>
                    <div class="quick-chips-row" id="quick-chips-container">
                        <!-- Injected via JS -->
                    </div>
                </div>

                <button type="submit" class="btn-login-submit" id="btn-submit-login">
                    <span>Secure Sign In to Portal</span>
                    <i class="fa-solid fa-arrow-right-to-bracket"></i>
                </button>
            </form>

            <div class="login-card-footer">
                <div class="security-chip">
                    <i class="fa-solid fa-shield-halved text-success"></i> 256-Bit SSL Encrypted University Gateway
                </div>
                <div class="team-credits">
                    Team: <strong>K. Mukundha (25B11CS380)</strong> • <strong>T. Sai Abhiram (25B11CS932)</strong> • <strong>K. Sameer Reddy (25B11CS490)</strong> • <strong>Shaik Sajid (25B11CS891)</strong>
                </div>
            </div>
        </div>
    </div>
"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(part1)
print('Generated login screen part 1')

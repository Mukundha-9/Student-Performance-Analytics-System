# fix_proctor_card_and_profile.py
import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Dedicated Faculty Proctor & Mentor Card in student-profile-tab
mentor_card_profile_html = """
                    <!-- Assigned Faculty Proctor & Mentor Desk Card -->
                    <div class="panel-card mb-3" style="border-left: 5px solid #f59e0b;">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-user-shield text-warning"></i> Assigned Faculty Proctor & Academic Mentor</h3>
                                <p class="text-muted" style="font-size:12.5px;">Official university proctor assigned for academic counselling, attendance clearance & project guidance</p>
                            </div>
                            <span class="badge badge-warning" style="font-size:12px;"><i class="fa-solid fa-certificate"></i> Approved Mentor</span>
                        </div>
                        <div class="proctor-hero-card" id="prof-proctor-card-container">
                            <div class="proctor-avatar"><i class="fa-solid fa-user-tie"></i></div>
                            <div style="min-width:0;">
                                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                                    <h4 style="font-size:18px; color:var(--text-primary); font-weight:800;" id="prof-mentor-name">Dr. A. K. Sharma</h4>
                                    <span class="badge badge-warning">Professor & Head of Academic Council</span>
                                </div>
                                <p style="font-size:13px; color:var(--text-secondary); margin:4px 0;" id="prof-mentor-dept">Department of Computer Science & Engineering • Aditya University</p>
                                <div style="display:flex; gap:16px; flex-wrap:wrap; font-size:12px; color:var(--text-muted); margin-top:10px;">
                                    <span><i class="fa-solid fa-envelope text-primary"></i> <strong id="prof-mentor-email" style="color:var(--text-primary);">aksharma@aditya.ac.in</strong></span>
                                    <span><i class="fa-solid fa-phone text-success"></i> <strong id="prof-mentor-phone" style="color:var(--text-primary);">+91 98765 43210</strong></span>
                                    <span><i class="fa-solid fa-door-open text-warning"></i> <strong id="prof-mentor-office" style="color:var(--text-primary);">Ramanujan Block - Room 402</strong></span>
                                    <span><i class="fa-solid fa-clock text-info"></i> <strong id="prof-mentor-hours" style="color:var(--text-primary);">Mon - Fri (03:30 PM - 05:00 PM)</strong></span>
                                </div>
                            </div>
                            <div>
                                <button class="btn btn-primary" onclick="openModal('modal-request-meeting')">
                                    <i class="fa-solid fa-calendar-plus"></i> Request 1-on-1 Meeting
                                </button>
                            </div>
                        </div>
                    </div>
"""

# Insert mentor_card_profile_html right before <!-- Multi-Semester Comprehensive Academic Performance Ledger -->
if 'id="prof-proctor-card-container"' not in html:
    html = html.replace('<!-- Multi-Semester Comprehensive Academic Performance Ledger -->', mentor_card_profile_html + '\n                    <!-- Multi-Semester Comprehensive Academic Performance Ledger -->')
    print("Inserted dedicated proctor mentor card into student-profile-tab")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

# Update static/js/app.js to populate both proctor cards
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

old_prof_mentor_fill = "document.getElementById('prof-mentor-badge').innerText = `Proctor: ${p.mentor_name}`;"
new_prof_mentor_fill = """document.getElementById('prof-mentor-badge').innerText = `Proctor: ${p.mentor_name}`;
        if (document.getElementById('prof-mentor-name')) document.getElementById('prof-mentor-name').innerText = p.mentor_name || 'Dr. A. K. Sharma';"""

if old_prof_mentor_fill in js:
    js = js.replace(old_prof_mentor_fill, new_prof_mentor_fill)
    print("Updated loadStudentProfile in app.js to fill proctor card details.")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

# Update static/css/style.css to ensure proctor-hero-card is fluid and never cut off
css_fix = """
/* ==========================================================================
   PROCTOR HERO CARD AND PROFILE DESK RESPONSIVE FIX
   ========================================================================== */

.proctor-hero-card {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, var(--bg-card) 100%);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    display: grid;
    grid-template-columns: 70px 1fr auto;
    gap: 20px;
    align-items: center;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
}

@media (max-width: 960px) {
    .proctor-hero-card {
        grid-template-columns: 1fr;
        text-align: left;
        gap: 14px;
    }
}

.proctor-avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}

#student-faculty-tab .grid-2-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

#student-meetings-table {
    width: 100%;
    min-width: 100%;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_fix)

print("Successfully injected responsive proctor hero card fixes into static/css/style.css")

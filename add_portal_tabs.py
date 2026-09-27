# add_portal_tabs.py
import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

faculty_new_tabs = """
                <!-- TAB: Faculty Remedial Action Planner -->
                <section class="tab-content" id="faculty-remedial-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-graduation-cap text-warning"></i> Remedial Action Planner & Weak Concept Reinforcement</h3>
                                <p class="text-muted" style="font-size:12.5px;">Auto-identified student cohort scoring < 50% requiring tutorial intervention</p>
                            </div>
                            <button class="btn btn-sm btn-primary" onclick="showToast('Remedial Schedule Broadcasted to Students', 'success')"><i class="fa-solid fa-bullhorn"></i> Broadcast Schedule</button>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table" id="faculty-remedial-table">
                                <thead>
                                    <tr>
                                        <th>Roll Number</th>
                                        <th>Student Name</th>
                                        <th>Branch</th>
                                        <th>Subject</th>
                                        <th>Current Score</th>
                                        <th>Attendance</th>
                                        <th>Gap Analysis & Remedial Action</th>
                                        <th>Target Score</th>
                                    </tr>
                                </thead>
                                <tbody id="faculty-remedial-tbody"></tbody>
                            </table>
                        </div>
                    </div>

                    <div class="panel-card">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-calendar-week text-primary"></i> 4-Week Remedial Master Schedule</h3>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table table-sm" id="faculty-remedial-schedule-table">
                                <thead>
                                    <tr><th>Phase</th><th>Remedial Focus Topic</th><th>Session Schedule</th><th>Allotted Venue</th></tr>
                                </thead>
                                <tbody id="faculty-remedial-schedule-tbody"></tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- TAB: Faculty Leave & Slot Swapping Desk -->
                <section class="tab-content" id="faculty-leave-tab">
                    <div class="grid-2-columns">
                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-calendar-check text-primary"></i> Apply Leave & Assign Lecture Substitute</h3>
                            </div>
                            <form id="faculty-leave-form" class="compact-form">
                                <div class="form-group">
                                    <label>Leave Date</label>
                                    <input type="date" class="form-input" id="leave-date-input" required>
                                </div>
                                <div class="form-group">
                                    <label>Leave Category</label>
                                    <select class="form-input" id="leave-type-select">
                                        <option value="On Duty (National Conference/Seminar)">On Duty (National Conference/Seminar)</option>
                                        <option value="Casual Leave (Personal)">Casual Leave (Personal)</option>
                                        <option value="Medical Leave">Medical Leave</option>
                                        <option value="Academic Research Duty">Academic Research Duty</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Designated Substitute Faculty</label>
                                    <select class="form-input" id="leave-substitute-select">
                                        <option value="Prof. V. Priya (50102) - CSE">Prof. V. Priya (50102) - CSE</option>
                                        <option value="Dr. K. Venkatesh Rao (50103) - CSE">Dr. K. Venkatesh Rao (50103) - CSE</option>
                                        <option value="Dr. S. R. Murthy (50201) - ECE">Dr. S. R. Murthy (50201) - ECE</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Lecture Slot Details to Swap / Cover</label>
                                    <input type="text" class="form-input" id="leave-slot-input" placeholder="e.g. Period 2 (09:50 - 10:40 AM) in Lab-3" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block"><i class="fa-solid fa-paper-plane"></i> Submit Leave & Auto-Swap Timetable</button>
                            </form>
                        </div>

                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-clock-rotate-left"></i> Leave History & Substitute Log</h3>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table table-sm" id="faculty-leaves-table">
                                    <thead>
                                        <tr><th>Leave ID</th><th>Date</th><th>Type</th><th>Substitute Faculty</th><th>Status</th></tr>
                                    </thead>
                                    <tbody id="faculty-leaves-tbody"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </section>
"""

admin_new_tabs = """
                <!-- TAB: Admin Semester Results Moderation & Publishing Engine -->
                <section class="tab-content" id="admin-results-tab">
                    <div class="fee-summary-grid mb-3">
                        <div class="stat-card">
                            <div class="stat-icon" style="background:rgba(16,185,129,0.15); color:#10b981;"><i class="fa-solid fa-globe"></i></div>
                            <div class="stat-details">
                                <span>Portal Result Status</span>
                                <h3 id="admin-publish-status-display" style="color:#10b981;">PUBLISHED LIVE</h3>
                                <small class="text-muted">Semester 4 Regular AY 2025-26</small>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon" style="background:rgba(59,130,246,0.15); color:#3b82f6;"><i class="fa-solid fa-chart-line"></i></div>
                            <div class="stat-details">
                                <span>Current Pass Rate</span>
                                <h3 id="admin-pass-rate-display">89.6%</h3>
                                <small class="text-success">500 Students Enrolled</small>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;"><i class="fa-solid fa-scale-balanced"></i></div>
                            <div class="stat-details">
                                <span>Moderation Policy</span>
                                <h3 id="admin-grace-display">+3 Marks Max</h3>
                                <small class="text-muted">Borderline (35-39) Threshold</small>
                            </div>
                        </div>
                    </div>

                    <div class="grid-2-columns">
                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-sliders text-primary"></i> University Result Moderation Tool</h3>
                            </div>
                            <p class="text-muted mb-3" style="font-size:12.5px;">Apply standardized university academic council grace marks (1-5 marks) for students failing marginally at 35-39 marks.</p>
                            <div class="form-group mb-3">
                                <label>Grace Marks to Allocate</label>
                                <select class="form-input" id="moderation-grace-select">
                                    <option value="1">+1 Grace Mark (Borderline 39 -> 40 Pass)</option>
                                    <option value="2">+2 Grace Marks (Borderline 38-39 -> 40 Pass)</option>
                                    <option value="3" selected>+3 Grace Marks (Borderline 37-39 -> 40 Pass)</option>
                                    <option value="4">+4 Grace Marks (Borderline 36-39 -> 40 Pass)</option>
                                    <option value="5">+5 Grace Marks (Academic Council Discretion)</option>
                                </select>
                            </div>
                            <div style="display:flex; gap:10px;">
                                <button class="btn btn-primary flex-1" id="btn-apply-moderation"><i class="fa-solid fa-calculator"></i> Apply Moderation</button>
                                <button class="btn btn-outline" id="btn-toggle-publish"><i class="fa-solid fa-lock"></i> Toggle Publish</button>
                            </div>
                        </div>

                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-list-check"></i> Examination Committee Log</h3>
                            </div>
                            <div id="admin-moderation-log" style="font-size:12.5px; color:var(--text-secondary); line-height:1.6;">
                                <div style="background:var(--bg-main); padding:12px; border-radius:6px; border:1px solid var(--border-color); margin-bottom:8px;">
                                    <strong><i class="fa-solid fa-circle-check text-success"></i> Academic Council Clearance:</strong> Verified against 500 candidate answer scripts.
                                </div>
                                <div style="background:var(--bg-main); padding:12px; border-radius:6px; border:1px solid var(--border-color);">
                                    <strong><i class="fa-solid fa-shield-halved text-primary"></i> Tamper-Proof Audit:</strong> All recalculated scores auto-synced with master database.
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- TAB: Admin NAAC / NBA Accreditation Audit Desk -->
                <section class="tab-content" id="admin-audit-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-award text-warning"></i> Institutional Quality & NAAC/NBA Compliance Audit Desk</h3>
                                <p class="text-muted" style="font-size:12.5px;">Aditya University • Cycle-3 NAAC / Tier-1 NBA Assessment Metrics</p>
                            </div>
                            <span class="badge badge-success" style="font-size:13px;"><i class="fa-solid fa-certificate"></i> Grade A++ (Score 3.78/4.00)</span>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table" id="admin-criteria-table">
                                <thead><tr><th>NAAC / NBA Accreditation Criteria</th><th>Assessed Score (out of 4.0)</th><th>Compliance Rating</th></tr></thead>
                                <tbody id="admin-criteria-tbody"></tbody>
                            </table>
                        </div>
                    </div>

                    <div class="panel-card">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-diagram-project text-primary"></i> Department-Level Performance & Outcome-Based Education (OBE) Attainment</h3>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table table-sm" id="admin-branch-audit-table">
                                <thead><tr><th>Department / Branch</th><th>Enrolled</th><th>Pass Rate</th><th>Mean Score</th><th>OBE Attainment</th><th>Accreditation Status</th></tr></thead>
                                <tbody id="admin-branch-audit-tbody"></tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- TAB: Admin Campus Detention & Warning Desk -->
                <section class="tab-content" id="admin-detention-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-triangle-exclamation text-danger"></i> Campus-Wide Attendance Detention Order & Condonation Desk</h3>
                                <p class="text-muted" style="font-size:12.5px;">Students with Attendance < 75% across all 6 Engineering Departments</p>
                            </div>
                            <button class="btn btn-sm btn-primary" onclick="window.print()"><i class="fa-solid fa-print"></i> Print Official Detention Order</button>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table" id="admin-detention-table">
                                <thead>
                                    <tr><th>Student ID</th><th>Student Name</th><th>Branch</th><th>Attendance %</th><th>Overall Score</th><th>Compliance Status</th><th>Parent Contact</th><th>Notice Dispatch</th></tr>
                                </thead>
                                <tbody id="admin-detention-tbody"></tbody>
                            </table>
                        </div>
                    </div>
                </section>
"""

# Insert faculty tabs right before <!-- 3. ADMIN PORTAL TABS -->
content = content.replace("<!-- ============================================================== -->\n                <!-- 3. ADMIN PORTAL TABS -->", faculty_new_tabs + "\n                <!-- ============================================================== -->\n                <!-- 3. ADMIN PORTAL TABS -->")

# Insert admin tabs right before <!-- TAB: Shared Aditya AI Advisor -->
content = content.replace("<!-- TAB: Shared Aditya AI Advisor -->", admin_new_tabs + "\n                <!-- TAB: Shared Aditya AI Advisor -->")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Successfully injected unique Faculty and Admin tabs into templates/index.html")

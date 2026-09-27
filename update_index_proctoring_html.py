# update_index_proctoring_html.py
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Enhanced Student Faculty Tab with Proctor Meetings and Assigned Forms
enhanced_student_faculty = """                <!-- TAB: Enrolled Faculty & Proctor Desk -->
                <section class="tab-content" id="student-faculty-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-user-shield text-warning"></i> My Assigned Faculty Proctor & Mentor</h3>
                            <span class="badge badge-warning">Academic Mentorship Desk</span>
                        </div>
                        <div class="proctor-hero-card" id="student-proctor-card"></div>
                    </div>

                    <!-- Student Proctor Meetings & Assigned University Forms -->
                    <div class="grid-2-columns mb-3">
                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-calendar-check text-primary"></i> My Scheduled Proctor Meetings</h3>
                                <span class="badge badge-info">Locked Schedule</span>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table table-sm" id="student-meetings-table">
                                    <thead><tr><th>Date & Time</th><th>Purpose</th><th>Venue</th><th>Status</th></tr></thead>
                                    <tbody id="student-meetings-tbody"></tbody>
                                </table>
                            </div>
                        </div>

                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-clipboard-list text-success"></i> University Forms & Proctor Tasks</h3>
                                <span class="badge badge-warning">Action Required</span>
                            </div>
                            <div class="proctor-tasks-student-list" id="student-tasks-list"></div>
                        </div>
                    </div>

                    <div class="panel-card">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-chalkboard-user"></i> Semester Subject Professors</h3>
                        </div>
                        <div class="faculty-cards-grid" id="student-faculties-grid"></div>
                    </div>
                </section>"""

# 2. Enhanced Faculty Proctoring Tab with 4 Comprehensive Sub-Panels
enhanced_faculty_proctoring = """                <!-- TAB: Faculty Proctoring & Mentorship Hub -->
                <section class="tab-content" id="faculty-proctoring-tab">
                    <!-- Proctor Sub-Nav Pill Switcher -->
                    <div class="proctor-subnav-bar mb-3">
                        <button class="proctor-sub-btn active" data-target="proctor-roster-view"><i class="fa-solid fa-users"></i> 25 Mentees Roster</button>
                        <button class="proctor-sub-btn" data-target="proctor-meetings-view"><i class="fa-solid fa-calendar-days"></i> Locked Meetings Desk</button>
                        <button class="proctor-sub-btn" data-target="proctor-tasks-view"><i class="fa-solid fa-clipboard-check"></i> Form & Task Compliance Tracker</button>
                        <button class="proctor-sub-btn" data-target="proctor-ptm-view"><i class="fa-solid fa-phone-volume"></i> Twice-Weekly Parent Diary</button>
                    </div>

                    <!-- SUB-VIEW 1: Mentees Roster -->
                    <div class="proctor-sub-view active" id="proctor-roster-view">
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-user-shield text-warning"></i> Assigned Proctoring Mentees (25 Students)</h3>
                                    <p class="text-muted" style="font-size:12.5px;">Monitor attendance, academic health, and lock 1-on-1 meetings</p>
                                </div>
                                <span class="badge badge-danger" id="proctor-alert-count">3 Mentees Flagged At-Risk</span>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table" id="faculty-proctoring-table">
                                    <thead>
                                        <tr>
                                            <th>Student ID</th>
                                            <th>Student Name</th>
                                            <th>Branch</th>
                                            <th>Attendance</th>
                                            <th>Percentage</th>
                                            <th>Grade</th>
                                            <th>Academic Standing</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody id="faculty-proctoring-tbody"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- SUB-VIEW 2: Locked Proctor Meetings Desk -->
                    <div class="proctor-sub-view" id="proctor-meetings-view" style="display:none;">
                        <div class="grid-2-columns">
                            <div class="panel-card">
                                <div class="panel-header">
                                <h3><i class="fa-solid fa-calendar-plus text-primary"></i> Lock 1-on-1 Proctor Meeting</h3>
                            </div>
                            <form id="proctor-meeting-form" class="compact-form">
                                <div class="form-group">
                                    <label>Select Mentee Student</label>
                                    <select class="form-input" id="meet-student-select" required></select>
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label>Meeting Date</label>
                                        <input type="date" class="form-input" id="meet-date-input" required>
                                    </div>
                                    <div class="form-group">
                                        <label>Time Slot</label>
                                        <input type="text" class="form-input" id="meet-time-input" value="03:30 PM - 04:00 PM" placeholder="e.g. 03:30 PM - 04:00 PM" required>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label>Meeting Purpose / Agenda</label>
                                    <input type="text" class="form-input" id="meet-purpose-input" placeholder="e.g. Attendance Shortage & Mid-Term Review" required>
                                </div>
                                <div class="form-group">
                                    <label>Meeting Venue</label>
                                    <input type="text" class="form-input" id="meet-venue-input" value="Ramanujan Block - Room 402 (Faculty Cabin)" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block"><i class="fa-solid fa-lock"></i> Lock Meeting & Notify Student</button>
                            </form>
                        </div>

                        <div class="panel-card">
                            <div class="panel-header">
                                <h3><i class="fa-solid fa-calendar-check"></i> Confirmed & Locked Meetings</h3>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table table-sm" id="proctor-meetings-table">
                                    <thead><tr><th>Mentee</th><th>Date & Time</th><th>Purpose</th><th>Status</th></tr></thead>
                                    <tbody id="proctor-meetings-tbody"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                    <!-- SUB-VIEW 3: University Form & Task Compliance Tracker -->
                    <div class="proctor-sub-view" id="proctor-tasks-view" style="display:none;">
                        <div class="panel-card mb-3">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-paper-plane text-primary"></i> Broadcast Official University Form / Task to Mentees</h3>
                                    <p class="text-muted" style="font-size:12.5px;">Pushes tasks directly to student notification feeds with live submission tracking</p>
                                </div>
                            </div>
                            <form id="proctor-task-form" class="compact-form">
                                <div class="form-row">
                                    <div class="form-group" style="flex:2;">
                                        <label>Form / Task Title</label>
                                        <input type="text" class="form-input" id="task-title-input" placeholder="e.g. End-Semester Elective Choice & Exam Form" required>
                                    </div>
                                    <div class="form-group">
                                        <label>Category</label>
                                        <select class="form-input" id="task-category-select">
                                            <option value="University Official Form">University Official Form</option>
                                            <option value="Placement Compliance">Placement Compliance</option>
                                            <option value="Statutory Undertaking">Statutory Undertaking</option>
                                            <option value="Academic Feedback">Academic Feedback</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label>Submission Deadline</label>
                                        <input type="text" class="form-input" id="task-deadline-input" placeholder="e.g. 05-Sep-2026 (05:00 PM)" required>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label>Instructions & Description for Students</label>
                                    <input type="text" class="form-input" id="task-desc-input" placeholder="Enter instructions for students to complete this form..." required>
                                </div>
                                <button type="submit" class="btn btn-primary"><i class="fa-solid fa-bullhorn"></i> Send Form to All 25 Mentees</button>
                            </form>
                        </div>

                        <!-- Live Compliance Cards Feed -->
                        <div id="proctor-tasks-tracking-container"></div>
                    </div>

                    <!-- SUB-VIEW 4: Twice-Weekly Parent Interaction Diary -->
                    <div class="proctor-sub-view" id="proctor-ptm-view" style="display:none;">
                        <div class="grid-2-columns">
                            <div class="panel-card">
                                <div class="panel-header">
                                    <h3><i class="fa-solid fa-phone-volume text-success"></i> Log Parent Interaction (Twice-Weekly Schedule)</h3>
                                </div>
                                <form id="proctor-parent-call-form" class="compact-form">
                                    <div class="form-group">
                                        <label>Select Student Mentee</label>
                                        <select class="form-input" id="ptm-student-select" required></select>
                                    </div>
                                    <div class="form-row">
                                        <div class="form-group">
                                            <label>Parent / Guardian Name</label>
                                            <input type="text" class="form-input" id="ptm-parent-input" placeholder="e.g. K. Venkata Rao" required>
                                        </div>
                                        <div class="form-group">
                                            <label>Scheduled Slot</label>
                                            <select class="form-input" id="ptm-slot-select">
                                                <option value="Tuesday Slot (04:00 PM - 04:30 PM)">Tuesday Slot (04:00 PM - 04:30 PM)</option>
                                                <option value="Friday Slot (04:30 PM - 05:00 PM)">Friday Slot (04:30 PM - 05:00 PM)</option>
                                                <option value="Special Weekend Follow-up">Special Weekend Follow-up</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label>Discussion Summary (Attendance, Grades & Discipline)</label>
                                        <textarea class="form-input" id="ptm-topic-input" rows="2" placeholder="Brief discussion points discussed with parent..." required></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label>Parent Response / Remarks</label>
                                        <input type="text" class="form-input" id="ptm-feedback-input" placeholder="Parent agreed to monitor study hours..." required>
                                    </div>
                                    <button type="submit" class="btn btn-primary btn-block"><i class="fa-solid fa-floppy-disk"></i> Save to Official Parent Diary</button>
                                </form>
                            </div>

                            <div class="panel-card">
                                <div class="panel-header">
                                    <h3><i class="fa-solid fa-book-bookmark"></i> Bi-Weekly Parent Interaction Log</h3>
                                </div>
                                <div class="table-responsive">
                                    <table class="data-table table-sm" id="proctor-ptm-table">
                                        <thead><tr><th>Student / Parent</th><th>Scheduled Slot</th><th>Call Summary</th><th>Status</th></tr></thead>
                                        <tbody id="proctor-ptm-tbody"></tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>"""

# Replace in index.html
old_student_faculty = """                <!-- TAB: Enrolled Faculty -->
                <section class="tab-content" id="student-faculty-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-user-shield text-warning"></i> My Assigned Faculty Proctor & Mentor</h3>
                            <span class="badge badge-warning">Academic Mentorship Desk</span>
                        </div>
                        <div class="proctor-hero-card" id="student-proctor-card"></div>
                    </div>

                    <div class="panel-card">
                        <div class="panel-header">
                            <h3><i class="fa-solid fa-chalkboard-user"></i> Semester Subject Professors</h3>
                        </div>
                        <div class="faculty-cards-grid" id="student-faculties-grid"></div>
                    </div>
                </section>"""

content = content.replace(old_student_faculty, enhanced_student_faculty)

old_faculty_proctoring = """                <!-- TAB: Faculty Proctoring & Mentorship Desk -->
                <section class="tab-content" id="faculty-proctoring-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-user-shield text-warning"></i> Assigned Proctoring Mentees (25 Students)</h3>
                                <p class="text-muted" style="font-size:12.5px;">Monitor attendance, academic standing, and record counselling action logs</p>
                            </div>
                            <span class="badge badge-danger" id="proctor-alert-count">3 Mentees Flagged At-Risk</span>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table" id="faculty-proctoring-table">
                                <thead>
                                    <tr>
                                        <th>Student ID</th>
                                        <th>Student Name</th>
                                        <th>Branch</th>
                                        <th>Attendance</th>
                                        <th>Percentage</th>
                                        <th>Grade</th>
                                        <th>Academic Health Status</th>
                                        <th>Proctor Action</th>
                                    </tr>
                                </thead>
                                <tbody id="faculty-proctoring-tbody"></tbody>
                            </table>
                        </div>
                    </div>
                </section>"""

content = content.replace(old_faculty_proctoring, enhanced_faculty_proctoring)

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully replaced proctoring sections in templates/index.html")

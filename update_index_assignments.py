# update_index_assignments.py
import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Sidebar Brand info to same-line ADITYA UNIVERSITY PORTAL
old_sidebar_brand = """                <div class="brand-info">
                    <h2>ADITYA</h2>
                    <span>University Portal</span>
                </div>"""

new_sidebar_brand = """                <div class="brand-info">
                    <div class="brand-title-same-line">
                        <span class="brand-word-aditya">ADITYA</span>
                        <span class="brand-word-university">UNIVERSITY</span>
                        <span class="brand-word-portal">PORTAL</span>
                    </div>
                </div>"""

if old_sidebar_brand in html:
    html = html.replace(old_sidebar_brand, new_sidebar_brand)
    print("Updated sidebar brand header to same line with custom colors")
else:
    print("Sidebar brand pattern not matched directly, checking alternatives")

# 2. Update Top Navbar Title Tag to same-line ADITYA UNIVERSITY PORTAL
old_navbar_title = """                    <div class="portal-title-tag" id="top-portal-title-tag">
                        <span class="portal-indicator-dot"></span>
                        <strong id="top-portal-heading">🎓 STUDENT PORTAL</strong> &nbsp;|&nbsp;
                        <span id="top-portal-sub">Department of Computer Science & Engineering</span>
                    </div>"""

new_navbar_title = """                    <div class="portal-title-tag" id="top-portal-title-tag">
                        <span class="portal-indicator-dot"></span>
                        <div class="brand-title-same-line nav-brand-inline">
                            <span class="brand-word-aditya">ADITYA</span>
                            <span class="brand-word-university">UNIVERSITY</span>
                            <span class="brand-word-portal">PORTAL</span>
                        </div>
                        <span class="nav-brand-pipe" style="color:var(--border-light); margin:0 6px;">|</span>
                        <strong id="top-portal-heading">🎓 STUDENT PORTAL</strong> &nbsp;|&nbsp;
                        <span id="top-portal-sub">Department of Computer Science & Engineering</span>
                    </div>"""

if old_navbar_title in html:
    html = html.replace(old_navbar_title, new_navbar_title)
    print("Updated top navbar title to same line with custom colors")

# 3. Add Student Assignments Submission Section (#student-assignments-tab)
assignments_tab_html = """
                <!-- TAB: Student Assignments & Coursework Submission Desk -->
                <section class="tab-content" id="student-assignments-tab">
                    <div class="welcome-hero-card" style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 40%, #ea580c 100%);">
                        <div class="hero-info">
                            <span class="badge badge-primary"><i class="fa-solid fa-file-arrow-up"></i> Digital Coursework Submission Portal</span>
                            <h2>Assignments & Project Submissions</h2>
                            <p>Upload your continuous assessment files (PDF, DOC, DOCX) directly to the correspondent course faculty for verification and CIA grading.</p>
                        </div>
                        <div class="hero-stats">
                            <div class="hero-stat-box">
                                <span>Active Assignments</span>
                                <h3 id="stat-active-assignments">5</h3>
                                <small class="text-success"><i class="fa-solid fa-clock"></i> Current Sem</small>
                            </div>
                            <div class="hero-stat-box">
                                <span>Submitted</span>
                                <h3 id="stat-submitted-assignments">2</h3>
                                <small class="text-info"><i class="fa-solid fa-check-double"></i> Documented</small>
                            </div>
                        </div>
                    </div>

                    <div class="grid-2-columns" style="margin-top: 20px;">
                        <!-- Assignment Upload Card -->
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-cloud-arrow-up text-primary"></i> Submit Coursework to Faculty</h3>
                                    <p class="text-muted" style="font-size:12.5px;">Auto-routed directly to the correspondent subject professor</p>
                                </div>
                                <span class="badge badge-primary" style="font-size:11px;">PDF / Word DOCX</span>
                            </div>

                            <form id="form-submit-assignment" class="assignment-submit-form">
                                <div class="form-group mb-3">
                                    <label class="form-label"><i class="fa-solid fa-book-bookmark text-primary"></i> Select Subject & Assignment Task *</label>
                                    <select class="form-input" id="asg-select-task" required>
                                        <!-- Injected via JS -->
                                    </select>
                                </div>

                                <!-- Correspondent Faculty Info Box -->
                                <div class="correspondent-faculty-banner mb-3" id="asg-faculty-banner">
                                    <div class="asg-fac-avatar"><i class="fa-solid fa-chalkboard-user"></i></div>
                                    <div class="asg-fac-info">
                                        <span class="asg-fac-sub">Correspondent Faculty Member:</span>
                                        <h4 id="asg-fac-name">Prof. V. Priya (50102)</h4>
                                        <p id="asg-fac-dept">Assistant Professor • Dept. of Computer Science & Engineering</p>
                                    </div>
                                    <div class="asg-fac-status">
                                        <span class="badge badge-success"><i class="fa-solid fa-paper-plane"></i> Direct Route</span>
                                    </div>
                                </div>

                                <div class="form-group mb-3">
                                    <label class="form-label"><i class="fa-solid fa-pen-nib text-primary"></i> Submission Title / Topic *</label>
                                    <input type="text" class="form-input" id="asg-title-input" placeholder="e.g. Lab Experiment 4 - Dijkstra Routing Implementation" required>
                                </div>

                                <div class="form-group mb-3">
                                    <label class="form-label"><i class="fa-solid fa-comment-dots text-primary"></i> Student Notes / Remarks to Professor (Optional)</label>
                                    <textarea class="form-input" id="asg-notes-input" rows="2" placeholder="Mention problem set variations, github repository links, or specific queries..."></textarea>
                                </div>

                                <!-- Drag & Drop Document Upload Zone -->
                                <div class="form-group mb-3">
                                    <label class="form-label"><i class="fa-solid fa-file-pdf text-danger"></i> Attach Document (.pdf, .doc, .docx - Max 25MB) *</label>
                                    <div class="upload-dropzone" id="asg-dropzone">
                                        <input type="file" id="asg-file-input" accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" style="display:none;">
                                        <div class="dropzone-content" id="dropzone-prompt">
                                            <i class="fa-solid fa-cloud-arrow-up dropzone-icon"></i>
                                            <h4>Click to Browse or Drag & Drop File here</h4>
                                            <p>Accepts <strong>.pdf</strong>, <strong>.doc</strong>, <strong>.docx</strong> (Max 25MB)</p>
                                        </div>
                                        <div class="dropzone-selected-file" id="dropzone-file-preview" style="display:none;">
                                            <div class="file-icon-wrap" id="asg-file-type-icon">
                                                <i class="fa-solid fa-file-pdf text-danger"></i>
                                            </div>
                                            <div class="file-info-meta">
                                                <h5 id="asg-preview-filename">Assignment_Document.pdf</h5>
                                                <span id="asg-preview-filesize">2.1 MB</span> • <span class="text-success"><i class="fa-solid fa-circle-check"></i> Document Attached</span>
                                            </div>
                                            <button type="button" class="btn-remove-file" id="btn-remove-selected-file" title="Remove file"><i class="fa-solid fa-xmark"></i></button>
                                        </div>
                                    </div>
                                </div>

                                <button type="submit" class="btn-submit-assignment" id="btn-submit-asg">
                                    <i class="fa-solid fa-paper-plane"></i>
                                    <span>Submit Document to Correspondent Faculty</span>
                                </button>
                            </form>
                        </div>

                        <!-- Active Assignment Schedules & Guidelines -->
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-calendar-check text-warning"></i> Active Course Deadlines</h3>
                                    <p class="text-muted" style="font-size:12.5px;">Semester 4 coursework deadlines and rubrics</p>
                                </div>
                            </div>
                            <div class="active-assignments-list" id="asg-deadlines-container">
                                <!-- Populated dynamically via JS -->
                            </div>

                            <div class="assignment-policy-box mt-3">
                                <h4><i class="fa-solid fa-circle-info text-primary"></i> University Coursework Guidelines:</h4>
                                <ul>
                                    <li>Files must be submitted in <strong>PDF</strong>, <strong>DOC</strong>, or <strong>DOCX</strong> format before 11:59 PM on the due date.</li>
                                    <li>Your submission is immediately delivered to the correspondent faculty's evaluation dashboard.</li>
                                    <li>Faculty evaluations and CIA marks will appear directly in your submissions gradebook below.</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Submissions History & Gradebook Table -->
                    <div class="panel-card" style="margin-top: 24px;">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-clock-rotate-left text-success"></i> My Submissions History & Faculty Evaluation</h3>
                                <p class="text-muted" style="font-size:12.5px;">Real-time review status, CIA marks, and faculty comments</p>
                            </div>
                            <div class="table-actions">
                                <span class="badge badge-info" id="badge-total-submissions">2 Submissions</span>
                            </div>
                        </div>

                        <div class="table-responsive">
                            <table class="data-table" id="student-submissions-table">
                                <thead>
                                    <tr>
                                        <th>Subject & Task</th>
                                        <th>Correspondent Faculty</th>
                                        <th>Submitted File</th>
                                        <th>Submission Date & Time</th>
                                        <th>Review Status</th>
                                        <th>Marks Awarded</th>
                                        <th>Faculty Feedback & Remarks</th>
                                    </tr>
                                </thead>
                                <tbody id="student-submissions-tbody">
                                    <!-- Injected via JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>
"""

# Insert before </section> of student-profile-tab or right before student-timetable-tab
if 'id="student-assignments-tab"' not in html:
    html = html.replace('<!-- TAB: Student Timetable -->', assignments_tab_html + '\n                <!-- TAB: Student Timetable -->')
    print("Inserted student-assignments-tab section into index.html")

# 4. Add Faculty Submissions Review View inside faculty-proctoring-tab
faculty_asg_subnav_btn = '<button class="proctor-sub-btn" data-target="proctor-assignments-view"><i class="fa-solid fa-file-circle-check"></i> Coursework Submissions Received</button>'
if 'data-target="proctor-assignments-view"' not in html:
    html = html.replace(
        '<button class="proctor-sub-btn" data-target="proctor-ptm-view"><i class="fa-solid fa-phone-volume"></i> Twice-Weekly Parent Diary</button>',
        '<button class="proctor-sub-btn" data-target="proctor-ptm-view"><i class="fa-solid fa-phone-volume"></i> Twice-Weekly Parent Diary</button>\n                        ' + faculty_asg_subnav_btn
    )
    print("Added Coursework Submissions subnav button to faculty-proctoring-tab")

faculty_asg_view_html = """
                    <!-- SUB-VIEW 5: Coursework Submissions Received by Faculty -->
                    <div class="proctor-sub-view" id="proctor-assignments-view" style="display:none;">
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-file-signature text-primary"></i> Coursework Submissions Received from Students</h3>
                                    <p class="text-muted" style="font-size:12.5px;">Evaluate PDF/DOC submissions, verify documents, and assign CIA internal marks</p>
                                </div>
                                <span class="badge badge-primary" id="badge-fac-asg-count">Course Submissions</span>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table" id="faculty-assignments-table">
                                    <thead>
                                        <tr>
                                            <th>Student ID & Name</th>
                                            <th>Subject & Assignment</th>
                                            <th>Submitted Document</th>
                                            <th>Submitted At</th>
                                            <th>Status</th>
                                            <th>Marks Awarded</th>
                                            <th>Action / Grade</th>
                                        </tr>
                                    </thead>
                                    <tbody id="faculty-assignments-tbody">
                                        <!-- Injected via JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
"""

if 'id="proctor-assignments-view"' not in html:
    html = html.replace('</section>\n\n                <!-- ============================================================== -->\n                <!-- 3. UNIVERSITY ADMIN PORTAL TABS -->', faculty_asg_view_html + '\n                </section>\n\n                <!-- ============================================================== -->\n                <!-- 3. UNIVERSITY ADMIN PORTAL TABS -->')
    print("Added proctor-assignments-view to faculty section")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated templates/index.html with all Assignment elements and Brand headers.")

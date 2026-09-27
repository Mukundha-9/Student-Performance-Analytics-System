# update_app_to_light_and_branding.py
import re

# ==============================================================================
# 1. Update templates/index.html
# ==============================================================================

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# A. Force data-theme="light" permanently on html tag
html = re.sub(r'<html\s+lang="en"[^>]*>', '<html lang="en" data-theme="light">', html)

# B. Remove theme toggle button from login screen
html = re.sub(r'<!-- Floating Theme Switcher on Login Screen -->[\s\S]*?</div>\s*</div>', '', html)
html = re.sub(r'<div class="login-theme-switch-wrap">[\s\S]*?</div>', '', html)

# C. Remove theme toggle button from top navbar
html = re.sub(r'<button class="theme-toggle-btn" id="theme-toggle-btn"[\s\S]*?</button>', '', html)

# D. Insert Motionable Custom Interactive Cursor right after <body>
cursor_html = """    <!-- Unique Motionable Interactive Cursor Elements -->
    <div class="custom-cursor-dot" id="cursor-dot"></div>
    <div class="custom-cursor-ring" id="cursor-ring"></div>
"""
if 'id="cursor-dot"' not in html:
    html = html.replace('<body>\n', '<body>\n' + cursor_html)
    print("Added custom motion cursor elements")

# E. Update Sidebar Header to use the official logo image
sidebar_header_new = """            <div class="sidebar-header">
                <div class="sidebar-official-brand">
                    <img src="/static/images/aditya_logo.png" alt="Aditya University" class="sidebar-brand-img">
                    <span class="sidebar-portal-badge">PORTAL</span>
                </div>
            </div>"""

html = re.sub(r'<div class="sidebar-header">[\s\S]*?</div>\s*</div>\s*</div>', sidebar_header_new, html, count=1)
if "sidebar-official-brand" not in html:
    # Alternative replace
    html = re.sub(r'<div class="sidebar-header">[\s\S]*?</div>\s*</div>', sidebar_header_new, html, count=1)
print("Updated sidebar header with official logo")

# F. Update Top Navbar Brand with official logo image
navbar_brand_new = """                    <div class="portal-title-tag" id="top-portal-title-tag">
                        <span class="portal-indicator-dot"></span>
                        <div class="nav-official-brand">
                            <img src="/static/images/aditya_logo.png" alt="Aditya University" class="nav-brand-img">
                            <span class="nav-portal-badge">PORTAL</span>
                        </div>
                        <span class="nav-brand-pipe" style="color:#cbd5e1; margin:0 8px;">|</span>
                        <strong id="top-portal-heading">🎓 STUDENT PORTAL</strong> &nbsp;|&nbsp;
                        <span id="top-portal-sub">Department of Computer Science & Engineering</span>
                    </div>"""

html = re.sub(r'<div class="portal-title-tag" id="top-portal-title-tag">[\s\S]*?</div>\s*</div>', navbar_brand_new, html, count=1)
print("Updated top navbar with official logo")

# G. Redesign Student Assignments Section (#student-assignments-tab)
assignments_tab_redesigned = """
                <!-- TAB: Student Assignments & Coursework Hub (Clean, Intuitive & Error-Free) -->
                <section class="tab-content" id="student-assignments-tab">
                    <!-- Clean Hero Banner -->
                    <div class="welcome-hero-card" style="background: linear-gradient(135deg, #1e40af 0%, #2563eb 55%, #ea580c 100%);">
                        <div class="hero-info">
                            <span class="badge badge-primary"><i class="fa-solid fa-file-circle-check"></i> Digital Coursework Submission Portal</span>
                            <h2>Coursework & Assignment Hub</h2>
                            <p>Submit assignments in PDF or Word document format directly to your correspondent course faculty for continuous assessment (CIA) grading.</p>
                        </div>
                        <div class="hero-stats">
                            <div class="hero-stat-box">
                                <span>Total Assigned</span>
                                <h3 id="stat-active-assignments">5</h3>
                                <small class="text-success"><i class="fa-solid fa-book-open"></i> Semester 4</small>
                            </div>
                            <div class="hero-stat-box">
                                <span>Awaiting Submission</span>
                                <h3 id="stat-pending-assignments">3</h3>
                                <small class="text-warning"><i class="fa-solid fa-clock"></i> Action Needed</small>
                            </div>
                            <div class="hero-stat-box">
                                <span>Completed & Graded</span>
                                <h3 id="stat-submitted-assignments">2</h3>
                                <small class="text-info"><i class="fa-solid fa-circle-check"></i> Documented</small>
                            </div>
                        </div>
                    </div>

                    <!-- Filter Pill Bar -->
                    <div class="asg-filter-bar mt-4 mb-3">
                        <button class="asg-filter-pill active" onclick="filterAssignmentsList('all')">
                            <i class="fa-solid fa-list-check"></i> All Assignments (<span id="pill-count-all">5</span>)
                        </button>
                        <button class="asg-filter-pill" onclick="filterAssignmentsList('pending')">
                            <i class="fa-solid fa-clock text-warning"></i> Pending Submission (<span id="pill-count-pending">3</span>)
                        </button>
                        <button class="asg-filter-pill" onclick="filterAssignmentsList('completed')">
                            <i class="fa-solid fa-circle-check text-success"></i> Submitted & Graded (<span id="pill-count-completed">2</span>)
                        </button>
                    </div>

                    <!-- Visual Assignment Cards Grid -->
                    <div class="assignments-cards-grid" id="asg-cards-grid">
                        <!-- Populated dynamically via JS -->
                    </div>

                    <!-- Submissions History & Gradebook Table -->
                    <div class="panel-card" style="margin-top: 28px;">
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
                                        <th>Submitted Document</th>
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

html = re.sub(r'<section class="tab-content"[^>]*id="student-assignments-tab"[\s\S]*?</section>', assignments_tab_redesigned.strip(), html)
print("Updated student-assignments-tab with clean cards-based hub")

# H. Add Clean Assignment Submission Modal (#modal-submit-assignment) before </body>
modal_submit_html = """
    <!-- DEDICATED ASSIGNMENT SUBMISSION MODAL -->
    <div class="modal-overlay" id="modal-submit-assignment" style="display:none;">
        <div class="modal-dialog asg-modal-dialog">
            <div class="modal-header">
                <div>
                    <h3 id="modal-asg-header-title"><i class="fa-solid fa-cloud-arrow-up text-primary"></i> Submit Assignment</h3>
                    <p class="text-muted" style="font-size:12px; margin:0;" id="modal-asg-header-sub">Route document to correspondent course faculty</p>
                </div>
                <button type="button" class="btn-close-modal" onclick="closeModal('modal-submit-assignment')"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <form id="form-modal-submit-asg">
                <input type="hidden" id="modal-asg-id-val">
                <div class="modal-body">
                    <!-- Correspondent Faculty Info Strip -->
                    <div class="correspondent-faculty-banner mb-3" style="background:#eff6ff; border-color:#bfdbfe;">
                        <div class="asg-fac-avatar"><i class="fa-solid fa-chalkboard-user"></i></div>
                        <div class="asg-fac-info">
                            <span class="asg-fac-sub">Submitting To Correspondent Faculty:</span>
                            <h4 id="modal-asg-fac-name">Prof. V. Priya (50102)</h4>
                            <p id="modal-asg-fac-dept">Assistant Professor • Dept. of Computer Science & Engineering</p>
                        </div>
                        <div class="asg-fac-status">
                            <span class="badge badge-success"><i class="fa-solid fa-paper-plane"></i> Direct Route</span>
                        </div>
                    </div>

                    <div class="asg-modal-meta-strip mb-3">
                        <div><small>Subject:</small><strong id="modal-asg-subject-val">Python Programming</strong></div>
                        <div><small>Maximum Marks:</small><strong id="modal-asg-maxmarks-val" class="text-primary">30 Marks</strong></div>
                        <div><small>Submission Due:</small><strong id="modal-asg-due-val" class="text-danger">15-Oct-2026</strong></div>
                    </div>

                    <div class="form-group mb-3">
                        <label class="form-label font-weight-bold"><i class="fa-solid fa-pen-nib text-primary"></i> Assignment Title / Submission Topic *</label>
                        <input type="text" class="form-input" id="modal-asg-title-input" required placeholder="e.g. Lab Experiment 4 - Shortest Path Implementation">
                    </div>

                    <div class="form-group mb-3">
                        <label class="form-label"><i class="fa-solid fa-comment-dots text-primary"></i> Student Notes / Remarks to Professor (Optional)</label>
                        <textarea class="form-input" id="modal-asg-notes-input" rows="2" placeholder="Mention problem set variations, github links, or specific queries..."></textarea>
                    </div>

                    <!-- Drag & Drop Upload Zone -->
                    <div class="form-group mb-2">
                        <label class="form-label font-weight-bold"><i class="fa-solid fa-file-pdf text-danger"></i> Attach Document (.pdf, .doc, .docx - Max 25MB) *</label>
                        <div class="upload-dropzone" id="modal-asg-dropzone">
                            <input type="file" id="modal-asg-file-input" accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" style="display:none;">
                            <div class="dropzone-content" id="modal-dropzone-prompt">
                                <i class="fa-solid fa-cloud-arrow-up dropzone-icon"></i>
                                <h4>Click to Browse or Drag & Drop File here</h4>
                                <p>Accepted Formats: <strong>.pdf</strong>, <strong>.doc</strong>, <strong>.docx</strong> (Max 25MB)</p>
                            </div>
                            <div class="dropzone-selected-file" id="modal-dropzone-file-preview" style="display:none;">
                                <div class="file-icon-wrap" id="modal-asg-file-type-icon">
                                    <i class="fa-solid fa-file-pdf text-danger"></i>
                                </div>
                                <div class="file-info-meta">
                                    <h5 id="modal-asg-preview-filename">Assignment_Document.pdf</h5>
                                    <span id="modal-asg-preview-filesize">2.1 MB</span> • <span class="text-success"><i class="fa-solid fa-circle-check"></i> Document Attached</span>
                                </div>
                                <button type="button" class="btn-remove-file" id="modal-btn-remove-selected-file" title="Remove file"><i class="fa-solid fa-xmark"></i></button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('modal-submit-assignment')">Cancel</button>
                    <button type="submit" class="btn btn-primary" id="btn-modal-submit-asg">
                        <i class="fa-solid fa-paper-plane"></i> <span>Submit Document to Faculty</span>
                    </button>
                </div>
            </form>
        </div>
    </div>
"""

if 'id="modal-submit-assignment"' not in html:
    html = html.replace('</body>', modal_submit_html + '\n</body>')
    print("Added dedicated Assignment Submission Modal to index.html")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated templates/index.html successfully!")

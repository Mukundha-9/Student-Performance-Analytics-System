# update_index_attendance_and_meetings.py
import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

student_attendance_tab_html = """
                <!-- TAB: Student Subject-Wise Attendance & Smart Calculator -->
                <section class="tab-content" id="student-attendance-tab">
                    <!-- Top Attendance KPI Summary -->
                    <div class="kpi-grid mb-3">
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-blue"><i class="fa-solid fa-clipboard-user"></i></div>
                            <div class="kpi-data">
                                <span>Overall Attendance</span>
                                <h3 id="att-overall-pct">98.0%</h3>
                                <small id="att-overall-status" class="text-success"><i class="fa-solid fa-circle-check"></i> Eligible for Exams (>=75%)</small>
                            </div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-emerald"><i class="fa-solid fa-calendar-check"></i></div>
                            <div class="kpi-data">
                                <span>Attended / Conducted</span>
                                <h3 id="att-total-counts">217 / 221</h3>
                                <small id="att-absent-count" class="text-muted">4 Classes Absent</small>
                            </div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-purple"><i class="fa-solid fa-calculator"></i></div>
                            <div class="kpi-data">
                                <span>Bunk / Recovery Margin</span>
                                <h3 id="att-margin-stat" style="color:var(--primary-light);">68 Classes</h3>
                                <small id="att-margin-desc" class="text-success">Safe Missable Margin</small>
                            </div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-icon-wrap bg-amber"><i class="fa-solid fa-triangle-exclamation"></i></div>
                            <div class="kpi-data">
                                <span>Missed Periods (Recent)</span>
                                <h3 id="att-recent-absences-count">2 Periods</h3>
                                <small class="text-warning">Past 5 Academic Days</small>
                            </div>
                        </div>
                    </div>

                    <!-- Subject-Wise Attendance Breakdown & 75% Rule Planner -->
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-book-open-reader text-primary"></i> Subject-Wise Attendance & 75% Mandatory Examination Rule</h3>
                                <p class="text-muted" style="font-size:12.5px;">University Regulation: Minimum 75.0% attendance in each individual subject is strictly required to appear for Semester Examinations.</p>
                            </div>
                            <span class="badge badge-info" style="font-size:12px;"><i class="fa-solid fa-shield-halved"></i> 75% Examination Criterion</span>
                        </div>
                        <div class="subject-attendance-grid" id="student-subject-attendance-cards">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>

                    <!-- Period-by-Period Daily Attendance Tracker & 4-Day Back Log -->
                    <div class="grid-2-columns">
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-clock-rotate-left text-primary"></i> Class-Wise Period Attendance Diary</h3>
                                    <p class="text-muted" style="font-size:12px;">Period-by-period tracking for Today and previous 4 academic days</p>
                                </div>
                            </div>
                            
                            <!-- Day Selector Buttons -->
                            <div class="att-day-selector mb-3" id="att-day-selector-btns">
                                <!-- Populated dynamically via JS -->
                            </div>

                            <div class="table-responsive">
                                <table class="data-table table-sm" id="att-period-diary-table">
                                    <thead>
                                        <tr>
                                            <th>Period & Time</th>
                                            <th>Subject Taught</th>
                                            <th>Faculty & Venue</th>
                                            <th>Attendance Status</th>
                                        </tr>
                                    </thead>
                                    <tbody id="att-period-diary-tbody"></tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Period Absence Alerts & Notification Feed -->
                        <div class="panel-card">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-bell text-danger"></i> Period Absence Alerts & Immediate Warnings</h3>
                                    <p class="text-muted" style="font-size:12px;">Instant notifications for individual missed class periods</p>
                                </div>
                            </div>
                            <div class="absence-alerts-feed" id="student-absence-alerts-list">
                                <!-- Populated dynamically via JS -->
                            </div>
                        </div>
                    </div>
                </section>
"""

# Insert student_attendance_tab_html right before <!-- TAB: Student Notifications & Circulars Hub -->
if 'id="student-attendance-tab"' not in html:
    html = html.replace('<!-- TAB: Student Notifications & Circulars Hub -->', student_attendance_tab_html + '\n                <!-- TAB: Student Notifications & Circulars Hub -->')
    print("Inserted student-attendance-tab into index.html")

# Enhanced proctor meetings subview with Incoming Student Meeting Requests for Faculty
old_proctor_meetings_view = """                    <!-- SUB-VIEW 2: Locked Proctor Meetings Desk -->
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
                </div>"""

new_proctor_meetings_view = """                    <!-- SUB-VIEW 2: Locked Proctor Meetings Desk & Student Booking Approvals -->
                    <div class="proctor-sub-view" id="proctor-meetings-view" style="display:none;">
                        <!-- Incoming Student Booking Requests (Pending Faculty Approval) -->
                        <div class="panel-card mb-3" style="border-left: 5px solid var(--warning);">
                            <div class="panel-header">
                                <div>
                                    <h3><i class="fa-solid fa-handshake text-warning"></i> Incoming Student Meeting Requests (Pending Your Acceptance & Slot Confirmation)</h3>
                                    <p class="text-muted" style="font-size:12.5px;">Review requests booked by your mentees and confirm / adjust the time slot and venue</p>
                                </div>
                                <span class="badge badge-warning" id="pending-meet-badge">Incoming Requests</span>
                            </div>
                            <div class="table-responsive">
                                <table class="data-table table-sm" id="faculty-pending-meetings-table">
                                    <thead>
                                        <tr>
                                            <th>Student Mentee</th>
                                            <th>Requested Date & Slot</th>
                                            <th>Purpose / Problem Category</th>
                                            <th>Student Notes</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody id="faculty-pending-meetings-tbody"></tbody>
                                </table>
                            </div>
                        </div>

                        <div class="grid-2-columns">
                            <div class="panel-card">
                                <div class="panel-header">
                                    <h3><i class="fa-solid fa-calendar-plus text-primary"></i> Lock / Schedule 1-on-1 Meeting</h3>
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
                                    <h3><i class="fa-solid fa-calendar-check"></i> Confirmed & Locked Meetings Schedule</h3>
                                </div>
                                <div class="table-responsive">
                                    <table class="data-table table-sm" id="proctor-meetings-table">
                                        <thead><tr><th>Mentee</th><th>Date & Time</th><th>Purpose & Venue</th><th>Status</th></tr></thead>
                                        <tbody id="proctor-meetings-tbody"></tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>"""

if old_proctor_meetings_view in html:
    html = html.replace(old_proctor_meetings_view, new_proctor_meetings_view)
    print("Replaced proctor meetings view with student booking approval desk.")

# Add Booking Modal at the end before </body>
modal_booking_html = """
    <!-- Modal: Request 1-on-1 Proctor Meeting (Student Side) -->
    <div class="modal" id="modal-request-meeting">
        <div class="modal-content" style="max-width: 520px;">
            <div class="modal-header">
                <h3><i class="fa-solid fa-calendar-plus text-primary"></i> Request 1-on-1 Meeting with Faculty Proctor</h3>
                <button class="modal-close" onclick="closeModal('modal-request-meeting')">&times;</button>
            </div>
            <form id="student-book-meeting-form">
                <div class="modal-body">
                    <p class="text-muted mb-3" style="font-size:12.5px;">Your meeting request will be sent directly to your assigned proctor (<strong>Dr. A. K. Sharma</strong>). Once accepted, the confirmed time slot and venue will appear in your portal.</p>
                    
                    <div class="form-group mb-3">
                        <label>Preferred Date</label>
                        <input type="date" class="form-input" id="book-meet-date" required>
                    </div>

                    <div class="form-group mb-3">
                        <label>Preferred Time Slot</label>
                        <select class="form-input" id="book-meet-slot" required>
                            <option value="09:00 AM - 09:50 AM (Morning Slot)">09:00 AM - 09:50 AM (Morning Slot)</option>
                            <option value="03:30 PM - 04:00 PM (Afternoon Slot)" selected>03:30 PM - 04:00 PM (Afternoon Slot)</option>
                            <option value="04:00 PM - 04:30 PM (Evening Slot)">04:00 PM - 04:30 PM (Evening Slot)</option>
                            <option value="04:30 PM - 05:00 PM (Post-Class Slot)">04:30 PM - 05:00 PM (Post-Class Slot)</option>
                        </select>
                    </div>

                    <div class="form-group mb-3">
                        <label>Meeting Purpose / Topic</label>
                        <select class="form-input" id="book-meet-purpose" required>
                            <option value="Academic Difficulty & Study Guidance" selected>Academic Difficulty & Study Guidance</option>
                            <option value="Attendance Shortage & Condonation Counselling">Attendance Shortage & Condonation Counselling</option>
                            <option value="Placement Readiness & Resume Verification">Placement Readiness & Resume Verification</option>
                            <option value="DAE Capstone Project Review">DAE Capstone Project Review</option>
                            <option value="Personal Counselling & General Grievance">Personal Counselling & General Grievance</option>
                        </select>
                    </div>

                    <div class="form-group mb-3">
                        <label>Specific Questions / Concerns for Faculty</label>
                        <textarea class="form-input" id="book-meet-notes" rows="3" placeholder="Briefly describe what you would like to discuss with your mentor..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline" onclick="closeModal('modal-request-meeting')">Cancel</button>
                    <button type="submit" class="btn btn-primary"><i class="fa-solid fa-paper-plane"></i> Send Meeting Request to Proctor</button>
                </div>
            </form>
        </div>
    </div>
"""

if 'id="modal-request-meeting"' not in html:
    html = html.replace('</body>', modal_booking_html + '\n</body>')
    print("Added modal-request-meeting to index.html")

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated templates/index.html with Attendance Tab, Meeting Request Modal, and Faculty Approval Desk.")

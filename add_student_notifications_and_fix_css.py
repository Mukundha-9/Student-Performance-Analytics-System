# add_student_notifications_and_fix_css.py
import re

# 1. Update templates/index.html
with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

student_notifications_section = """
                <!-- TAB: Student Notifications & Circulars Hub -->
                <section class="tab-content" id="student-notifications-tab">
                    <div class="panel-card mb-3">
                        <div class="panel-header">
                            <div>
                                <h3><i class="fa-solid fa-bell text-primary"></i> Campus Notifications & Proctor Compliance Hub</h3>
                                <p class="text-muted" style="font-size:12.5px;">Live administrative circulars and mandatory proctor compliance forms for Aditya University students</p>
                            </div>
                            <div style="display:flex; gap:8px;">
                                <button class="btn btn-sm btn-outline" onclick="loadStudentNotifications(currentUser?.id)"><i class="fa-solid fa-rotate"></i> Refresh Feed</button>
                            </div>
                        </div>

                        <!-- Filter Pill Switcher -->
                        <div class="notifications-filter-bar mb-3">
                            <button class="notif-filter-btn active" data-filter="all"><i class="fa-solid fa-layer-group"></i> All Notifications (<span id="notif-count-all">0</span>)</button>
                            <button class="notif-filter-btn" data-filter="admin"><i class="fa-solid fa-landmark"></i> University Admin Circulars (<span id="notif-count-admin">0</span>)</button>
                            <button class="notif-filter-btn" data-filter="proctor-task"><i class="fa-solid fa-clipboard-check"></i> Faculty Proctor Forms (<span id="notif-count-proctor">0</span>)</button>
                            <button class="notif-filter-btn" data-filter="proctor-meeting"><i class="fa-solid fa-calendar-check"></i> Proctor Meeting Alerts (<span id="notif-count-meeting">0</span>)</button>
                        </div>

                        <!-- Live Notifications Feed -->
                        <div class="notifications-stream-container" id="student-notifications-stream">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>
                </section>
"""

# Insert student-notifications-tab right before <!-- TAB: Student Timetable -->
if 'id="student-notifications-tab"' not in html:
    html = html.replace('<!-- TAB: Student Timetable -->', student_notifications_section + '\n                <!-- TAB: Student Timetable -->')
    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully inserted student-notifications-tab into templates/index.html")
else:
    print("student-notifications-tab already present in index.html")

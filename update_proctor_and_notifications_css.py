# update_proctor_and_notifications_css.py
css_rules = """

/* ==========================================================================
   PROCTORING LAYOUT FIX & STUDENT NOTIFICATIONS HUB STYLES
   ========================================================================== */

/* Fix layout clipping & width overflow */
#faculty-proctoring-tab,
#faculty-attendance-tab,
#faculty-marks-tab,
#faculty-remedial-tab,
#faculty-leave-tab {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
}

#faculty-proctoring-tab .panel-card,
#faculty-proctoring-tab .grid-2-columns,
#faculty-proctoring-tab .table-responsive {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

.proctor-subnav-bar {
    width: 100%;
    box-sizing: border-box;
    flex-wrap: wrap;
    gap: 8px;
}

.task-mentees-breakdown-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
    width: 100%;
    box-sizing: border-box;
}

/* Student Notifications Filter Bar */
.notifications-filter-bar {
    display: flex;
    gap: 8px;
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 6px;
    border-radius: var(--radius-sm);
    flex-wrap: wrap;
    width: 100%;
    box-sizing: border-box;
}
.notif-filter-btn {
    padding: 7px 12px;
    background: transparent;
    border: none;
    border-radius: 6px;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
}
.notif-filter-btn:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
}
.notif-filter-btn.active {
    background: var(--primary);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* Notifications Feed Cards */
.notifications-stream-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    box-sizing: border-box;
}
.notif-stream-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.notif-stream-card:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    transform: translateY(-1px);
}
.notif-stream-card.border-admin {
    border-left: 5px solid #3b82f6;
}
.notif-stream-card.border-task {
    border-left: 5px solid #f59e0b;
}
.notif-stream-card.border-task.completed {
    border-left: 5px solid #10b981;
}
.notif-stream-card.border-meeting {
    border-left: 5px solid #8b5cf6;
}

.notif-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}
.notif-card-header h4 {
    font-size: 15px;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
}
.notif-card-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    color: var(--text-muted);
}
.notif-card-body {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
}
.notif-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 4px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_rules)
print("Successfully appended notification and proctor layout CSS to static/css/style.css")

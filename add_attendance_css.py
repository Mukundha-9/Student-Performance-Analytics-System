# add_attendance_css.py
css_rules = """

/* ==========================================================================
   STUDENT SUBJECT-WISE ATTENDANCE, 75% RULE & CALCULATOR STYLES
   ========================================================================== */

.subject-attendance-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
    width: 100%;
    box-sizing: border-box;
}

.subject-att-card {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.subject-att-card:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
}

.subject-att-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
}
.subject-att-header h4 {
    font-size: 14.5px;
    color: var(--text-primary);
    font-weight: 700;
}
.subject-att-faculty {
    font-size: 11.5px;
    color: var(--text-muted);
    margin-top: 2px;
}

.subject-att-pct-display {
    display: flex;
    align-items: baseline;
    gap: 6px;
}
.subject-att-pct-display h3 {
    font-size: 22px;
    font-weight: 800;
}
.subject-att-pct-display span {
    font-size: 12px;
    color: var(--text-muted);
}

/* 75% Rule Progress Bar with Threshold Marker */
.att-progress-container {
    position: relative;
    width: 100%;
    margin: 4px 0 8px 0;
}
.att-progress-track {
    width: 100%;
    height: 10px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 5px;
    overflow: hidden;
    position: relative;
}
.att-progress-fill {
    height: 100%;
    border-radius: 5px;
    transition: width 0.5s ease;
}
.att-progress-fill.fill-safe {
    background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
}
.att-progress-fill.fill-risk {
    background: linear-gradient(90deg, #ef4444 0%, #f59e0b 100%);
}

/* 75% Target Marker */
.att-75-marker {
    position: absolute;
    top: -2px;
    left: 75%;
    width: 2px;
    height: 14px;
    background: #f59e0b;
    z-index: 2;
    box-shadow: 0 0 6px #f59e0b;
}
.att-75-marker-label {
    position: absolute;
    top: 14px;
    left: 75%;
    transform: translateX(-50%);
    font-size: 9.5px;
    font-weight: 800;
    color: #f59e0b;
    letter-spacing: 0.5px;
    white-space: nowrap;
}

/* Smart Calculator Bunk / Recovery Tag */
.att-calculator-tag {
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.4;
    display: flex;
    align-items: center;
    gap: 8px;
}
.att-calculator-tag.tag-safe {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: #34d399;
}
.att-calculator-tag.tag-risk {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.25);
    color: #f87171;
}

/* Day Selector Buttons */
.att-day-selector {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 5px;
    border-radius: var(--radius-sm);
}
.att-day-btn {
    padding: 6px 12px;
    background: transparent;
    border: none;
    border-radius: 4px;
    color: var(--text-secondary);
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
}
.att-day-btn:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.04);
}
.att-day-btn.active {
    background: var(--primary);
    color: #ffffff;
    box-shadow: 0 2px 6px rgba(59, 130, 246, 0.35);
}

/* Absence Alerts Feed */
.absence-alerts-feed {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 380px;
    overflow-y: auto;
}
.absence-alert-card {
    background: var(--bg-main);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-left: 4px solid #ef4444;
    border-radius: 6px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.absence-alert-card h5 {
    font-size: 13px;
    color: #f87171;
    display: flex;
    align-items: center;
    gap: 6px;
}
.absence-alert-meta {
    font-size: 11.5px;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_rules)

print("Successfully added attendance & calculator CSS to static/css/style.css")

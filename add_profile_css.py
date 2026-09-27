# add_profile_css.py
css_rules = """

/* ==========================================================================
   OFFICIAL STUDENT PROFILE & MULTI-SEMESTER LEDGER STYLES
   ========================================================================== */

/* Profile Hero Banner Card */
.profile-hero-card {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    display: flex;
    align-items: center;
    gap: 24px;
    position: relative;
    overflow: hidden;
}
.profile-hero-card::after {
    content: '';
    position: absolute;
    top: -50px;
    right: -50px;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.25) 0%, transparent 70%);
    pointer-events: none;
}
.profile-hero-avatar {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #2563eb, #1e40af);
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    color: #ffffff;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(37, 99, 235, 0.4);
}
.profile-hero-info {
    flex-grow: 1;
}
.profile-hero-info h2 {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.profile-hero-sub {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 2px;
}
.profile-badges-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

/* Personal Details 4-Column Grid */
.profile-details-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    width: 100%;
    box-sizing: border-box;
}
@media (max-width: 1024px) {
    .profile-details-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
    .profile-details-grid { grid-template-columns: 1fr; }
}

.prof-detail-box {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.prof-label {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}
.prof-val {
    font-size: 13px;
    color: var(--text-primary);
    font-weight: 700;
    word-break: break-word;
}

/* Prior Academic Qualifications Cards */
.prior-academic-box {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 18px 20px;
}
.prior-header {
    display: flex;
    align-items: center;
    gap: 12px;
}
.prior-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #ffffff;
    flex-shrink: 0;
}
.prior-header h4 {
    font-size: 14.5px;
    font-weight: 700;
    color: var(--text-primary);
}
.prior-header p {
    font-size: 11.5px;
    color: var(--text-muted);
}
.prior-scores-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border-color);
}
.prior-scores-grid small {
    display: block;
    font-size: 11px;
    color: var(--text-muted);
}
.prior-scores-grid strong {
    font-size: 13px;
    color: var(--text-primary);
}

/* Semester Tabs Bar & Summary */
.sem-tabs-bar {
    display: flex;
    gap: 8px;
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 6px;
    border-radius: var(--radius-sm);
    flex-wrap: wrap;
}
.sem-tab-btn {
    padding: 7px 16px;
    background: transparent;
    border: none;
    border-radius: 6px;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: var(--transition);
}
.sem-tab-btn:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
}
.sem-tab-btn.active {
    background: var(--primary);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
}

.sem-summary-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 14px 18px;
    border-radius: var(--radius-md);
    flex-wrap: wrap;
    gap: 12px;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_rules)

print("Successfully added student profile CSS to static/css/style.css")

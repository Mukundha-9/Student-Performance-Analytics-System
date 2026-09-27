# add_assignments_css.py

with open("static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

assignments_css = """

/* ==========================================================================
   BRAND TITLE ON SAME LINE: ADITYA (DARK BLUE) UNIVERSITY (ORANGE) PORTAL
   ========================================================================== */

.brand-title-same-line {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    white-space: nowrap !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    letter-spacing: 0.5px !important;
}

.brand-word-aditya {
    color: #1e3a8a !important; /* Dark Blue */
    font-weight: 900 !important;
    letter-spacing: 0.6px;
}

[data-theme="dark"] .brand-word-aditya {
    color: #3b82f6 !important; /* Vivid Blue in Dark Theme for optimal readability */
}

.brand-word-university {
    color: #ea580c !important; /* Vibrant Orange */
    font-weight: 900 !important;
    letter-spacing: 0.6px;
}

.brand-word-portal {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    opacity: 0.95;
    letter-spacing: 0.6px;
}

.nav-brand-inline {
    margin-right: 4px;
}

/* ==========================================================================
   STUDENT ASSIGNMENTS SUBMISSION DESK & FACULTY ROUTING
   ========================================================================== */

.correspondent-faculty-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: rgba(30, 58, 138, 0.08);
    border: 1.5px solid rgba(59, 130, 246, 0.25);
    border-radius: var(--radius-md);
    transition: var(--transition);
}

[data-theme="light"] .correspondent-faculty-banner {
    background: #eff6ff;
    border-color: #bfdbfe;
}

.asg-fac-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3);
}

.asg-fac-info {
    flex-grow: 1;
}

.asg-fac-sub {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.asg-fac-info h4 {
    font-size: 14.5px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 1px 0 2px 0;
}

.asg-fac-dept {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0;
}

/* Upload Dropzone */
.upload-dropzone {
    border: 2px dashed rgba(59, 130, 246, 0.4);
    border-radius: var(--radius-md);
    background: rgba(15, 23, 42, 0.4);
    padding: 24px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
}

[data-theme="light"] .upload-dropzone {
    background: #f8fafc;
    border-color: #cbd5e1;
}

.upload-dropzone:hover,
.upload-dropzone.drag-over {
    border-color: var(--primary);
    background: rgba(59, 130, 246, 0.08);
}

.dropzone-icon {
    font-size: 36px;
    color: var(--primary);
    margin-bottom: 10px;
}

.dropzone-content h4 {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.dropzone-content .browse-link {
    color: var(--primary-light);
    text-decoration: underline;
}

.dropzone-content p {
    font-size: 12px;
    color: var(--text-muted);
    margin: 0;
}

/* Selected File Preview */
.dropzone-selected-file {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    text-align: left;
}

[data-theme="light"] .dropzone-selected-file {
    background: #ffffff;
    border-color: #cbd5e1;
}

.file-icon-wrap {
    font-size: 28px;
    flex-shrink: 0;
}

.file-info-meta {
    flex-grow: 1;
}

.file-info-meta h5 {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 2px 0;
    word-break: break-all;
}

.file-info-meta span {
    font-size: 12px;
    color: var(--text-secondary);
}

.btn-remove-file {
    background: transparent;
    border: none;
    color: var(--danger);
    font-size: 18px;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: var(--transition);
}

.btn-remove-file:hover {
    background: rgba(239, 68, 68, 0.15);
}

/* Submit Button */
.btn-submit-assignment {
    width: 100%;
    padding: 13px 20px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff;
    border: none;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.5px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    transition: all 0.25s ease;
}

.btn-submit-assignment:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.45);
}

/* Active Assignments List */
.active-assignments-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.asg-item-card {
    padding: 12px 14px;
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
}

[data-theme="light"] .asg-item-card {
    background: #f8fafc;
    border-color: #e2e8f0;
}

.asg-item-info h5 {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 3px 0;
}

.asg-item-info p {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0 0 4px 0;
}

.asg-meta-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11.5px;
    color: var(--text-muted);
}

.assignment-policy-box {
    padding: 14px 16px;
    background: rgba(59, 130, 246, 0.06);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: var(--radius-md);
}

[data-theme="light"] .assignment-policy-box {
    background: #f0fdf4;
    border-color: #bbf7d0;
}

.assignment-policy-box h4 {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.assignment-policy-box ul {
    margin: 0;
    padding-left: 20px;
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.6;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(assignments_css)

print("Appended Assignments & Same-Line Brand CSS to static/css/style.css")

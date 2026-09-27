# add_cursor_and_card_css.py

with open("static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

new_styles = """

/* ==========================================================================
   INTERACTIVE MOTIONABLE CUSTOM CURSOR (UNIQUE & ATTRACTIVE UI/UX)
   ========================================================================== */

.custom-cursor-dot,
.custom-cursor-ring {
    pointer-events: none;
    position: fixed;
    border-radius: 50%;
    z-index: 9999999;
    top: 0;
    left: 0;
    transform: translate(-50%, -50%);
    user-select: none;
}

.custom-cursor-dot {
    width: 8px;
    height: 8px;
    background: #2563eb;
    box-shadow: 0 0 10px rgba(37, 99, 235, 0.8), 0 0 20px rgba(37, 99, 235, 0.4);
    transition: opacity 0.2s ease, transform 0.1s ease-out;
}

.custom-cursor-ring {
    width: 36px;
    height: 36px;
    border: 2px solid rgba(37, 99, 235, 0.65);
    background: transparent;
    transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), 
                height 0.25s cubic-bezier(0.16, 1, 0.3, 1), 
                background 0.25s ease, 
                border-color 0.25s ease, 
                transform 0.1s ease-out,
                box-shadow 0.25s ease;
}

/* Hovering on clickable elements */
body.cursor-hover .custom-cursor-ring {
    width: 54px;
    height: 54px;
    background: rgba(37, 99, 235, 0.12);
    border-color: #2563eb;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.3);
}

body.cursor-hover .custom-cursor-dot {
    transform: translate(-50%, -50%) scale(1.5);
    background: #1d4ed8;
}

/* Click Active Pulse */
body.cursor-click .custom-cursor-ring {
    transform: translate(-50%, -50%) scale(0.85);
    background: rgba(37, 99, 235, 0.25);
    border-color: #1e40af;
}

/* Hide custom cursor on mobile touch screens */
@media (hover: none) and (pointer: coarse) {
    .custom-cursor-dot,
    .custom-cursor-ring {
        display: none !important;
    }
}

/* ==========================================================================
   OFFICIAL ADITYA UNIVERSITY LOGO BRANDING PRESENTATION
   ========================================================================== */

.sidebar-official-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 4px;
}

.sidebar-brand-img {
    height: 42px;
    width: auto;
    max-width: 175px;
    object-fit: contain;
    display: block;
}

.sidebar-portal-badge {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 7px;
    border-radius: 5px;
    letter-spacing: 0.6px;
    line-height: 1;
}

.nav-official-brand {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.nav-brand-img {
    height: 32px;
    width: auto;
    max-width: 140px;
    object-fit: contain;
    display: block;
}

.nav-portal-badge {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff;
    font-size: 9.5px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}

/* ==========================================================================
   REFINED ASSIGNMENTS HUB (CLEAN, INTUITIVE & BEAUTIFUL CARDS)
   ========================================================================== */

.asg-filter-bar {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.asg-filter-pill {
    padding: 9px 18px;
    border-radius: 20px;
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    color: #475569;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 7px;
}

.asg-filter-pill:hover {
    background: #f1f5f9;
    color: #1e40af;
    border-color: #94a3b8;
}

.asg-filter-pill.active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.assignments-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
    margin-top: 10px;
}

.asg-clean-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-lg);
    padding: 22px;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
}

.asg-clean-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.12);
    border-color: #93c5fd;
}

.asg-card-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.asg-course-badge {
    font-size: 11px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.asg-card-title {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.35;
    margin: 0 0 8px 0;
}

.asg-card-instructions {
    font-size: 12.5px;
    color: #475569;
    line-height: 1.5;
    margin-bottom: 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.asg-fac-card-strip {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-md);
    margin-bottom: 14px;
}

.asg-fac-mini-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}

.asg-fac-mini-meta {
    flex-grow: 1;
}

.asg-fac-mini-meta small {
    font-size: 10.5px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
}

.asg-fac-mini-meta h6 {
    font-size: 13px;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}

.asg-card-meta-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 12px;
    border-top: 1px solid #e2e8f0;
    margin-bottom: 16px;
    font-size: 12px;
    color: #64748b;
}

.asg-card-actions {
    display: flex;
    gap: 10px;
}

.asg-card-actions .btn {
    width: 100%;
    justify-content: center;
    padding: 10px 14px;
    font-weight: 700;
    font-size: 13.5px;
}

/* Modal meta strip */
.asg-modal-meta-strip {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    padding: 12px 14px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: var(--radius-md);
}

.asg-modal-meta-strip div small {
    display: block;
    font-size: 11px;
    color: #64748b;
    margin-bottom: 2px;
}

.asg-modal-meta-strip div strong {
    font-size: 13px;
    color: #0f172a;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(new_styles)

print("Appended motion cursor, official logo, and assignments hub CSS")

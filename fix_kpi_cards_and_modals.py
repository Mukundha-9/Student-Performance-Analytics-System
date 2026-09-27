# fix_kpi_cards_and_modals.py

css_content = """

/* ==========================================================================
   KPI CARDS ULTRA-MODERN GLOWING BOX STYLES & MODAL OVERLAY FIX
   ========================================================================== */

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    width: 100%;
    margin-bottom: 20px;
    box-sizing: border-box;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: var(--primary);
    box-shadow: 0 8px 30px rgba(59, 130, 246, 0.25);
}

.kpi-icon-wrap {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.bg-blue {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(30, 58, 138, 0.5));
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.4);
}

.bg-emerald {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(6, 78, 59, 0.5));
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.bg-purple {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(88, 28, 135, 0.5));
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.4);
}

.bg-amber {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(120, 53, 15, 0.5));
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.kpi-data {
    display: flex;
    flex-direction: column;
    gap: 3px;
    min-width: 0;
}

.kpi-data span {
    font-size: 11.5px;
    color: var(--text-muted);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-data h3 {
    font-size: 24px;
    font-weight: 900;
    color: var(--text-primary);
    margin: 0;
    font-family: 'Plus Jakarta Sans', sans-serif;
    letter-spacing: -0.5px;
}

.kpi-data small {
    font-size: 11.5px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 5px;
}

/* ==========================================================================
   GLOBAL UNIVERSAL MODAL SYSTEM FIX
   ========================================================================== */

.modal, .modal-overlay {
    display: none !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    background-color: rgba(2, 6, 23, 0.82) !important;
    backdrop-filter: blur(8px) !important;
    z-index: 99999 !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 20px !important;
    box-sizing: border-box !important;
}

.modal.active, .modal.show, .modal-overlay.active {
    display: flex !important;
    animation: modalOverlayFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

@keyframes modalOverlayFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content, .modal-dialog {
    background: #0f172a !important;
    border: 1px solid rgba(59, 130, 246, 0.35) !important;
    border-radius: 16px !important;
    width: 100% !important;
    max-width: 560px !important;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.85) !important;
    overflow: hidden !important;
    position: relative !important;
    margin: auto !important;
    animation: modalPopUp 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

@keyframes modalPopUp {
    from { transform: scale(0.92) translateY(10px); opacity: 0; }
    to { transform: scale(1) translateY(0); opacity: 1; }
}

.modal-header {
    padding: 18px 24px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    background: rgba(30, 41, 59, 0.5) !important;
}

.modal-header h3 {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin: 0 !important;
}

.modal-close, .btn-close {
    background: transparent !important;
    border: none !important;
    font-size: 24px !important;
    color: #94a3b8 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.modal-close:hover, .btn-close:hover {
    background: rgba(239, 68, 68, 0.2) !important;
    color: #f87171 !important;
}

.modal-body {
    padding: 24px !important;
    max-height: 75vh !important;
    overflow-y: auto !important;
}

.modal-footer {
    padding: 16px 24px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    display: flex !important;
    justify-content: flex-end !important;
    gap: 10px !important;
    background: rgba(15, 23, 42, 0.8) !important;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_content)

print("Appended KPI Card and Modal CSS to static/css/style.css")

# Global modal helper in static/js/app.js
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

modal_helpers = """

// Universal Global Modal Handlers
window.openModal = function(modalId) {
    const el = document.getElementById(modalId);
    if (el) {
        el.classList.add('active');
        el.style.display = 'flex';
    }
};

window.closeModal = function(modalId) {
    const el = document.getElementById(modalId);
    if (el) {
        el.classList.remove('active');
        el.style.display = 'none';
    }
};

// Close modal on click outside content
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal') || e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        e.target.style.display = 'none';
    }
});

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active, .modal-overlay.active').forEach(m => {
            m.classList.remove('active');
            m.style.display = 'none';
        });
    }
});
"""

if "window.openModal" not in js:
    js += modal_helpers
    with open("static/js/app.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Injected global openModal and closeModal handlers into static/js/app.js")

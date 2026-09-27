# fix_report_endpoint.py
import re

# 1. Update app.py
with open("app.py", "r", encoding="utf-8") as f:
    app_py = f.read()

# Add import generate_report if not present
if "import generate_report" not in app_py:
    app_py = app_py.replace("import portal_manager", "import portal_manager\nimport generate_report")

# Fix get_report_markdown
old_report_route = """@app.route('/api/report/markdown', methods=['GET'])
def get_report_markdown():
    report_file = os.path.join(REPORTS_DIR, 'academic_performance_report.md')
    if not os.path.exists(report_file):
        df = data_manager.load_data()
        visualizer.save_all_visualizations(df)
    with open(report_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
@app.route('/api/faculty/remedial-plan/<faculty_id>', methods=['GET'])"""

new_report_route = """@app.route('/api/report/markdown', methods=['GET'])
def get_report_markdown():
    report_file = os.path.join(REPORTS_DIR, 'academic_performance_report.md')
    if not os.path.exists(report_file):
        df = data_manager.load_data()
        generate_report.generate_academic_report(df)
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception:
        df = data_manager.load_data()
        md_content = generate_report.generate_academic_report(df)
    return jsonify({'markdown': md_content})


@app.route('/api/faculty/remedial-plan/<faculty_id>', methods=['GET'])"""

if old_report_route in app_py:
    app_py = app_py.replace(old_report_route, new_report_route)
    print("Fixed get_report_markdown route in app.py")
else:
    # Use regex replacement if needed
    app_py = re.sub(
        r"@app\.route\('/api/report/markdown'[\s\S]*?@app\.route\('/api/faculty/remedial-plan",
        new_report_route,
        app_py
    )
    print("Replaced get_report_markdown with regex in app.py")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_py)

# 2. Update static/js/app.js
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Fix switchTab unconditioned loadStudentProctorDesk
js = js.replace("loadStudentProctorDesk(currentUser.id);", "if (currentUser && currentUser.id && (tabId === 'student-faculty-tab' || tabId === 'student-overview-tab')) loadStudentProctorDesk(currentUser.id);")

# Enhance loadAcademicReport renderer
old_load_report = """async function loadAcademicReport() {
    const viewer = document.getElementById('report-markdown-content');
    if (!viewer) return;

    try {
        const res = await fetch('/api/report/markdown');
        const data = await res.json();
        if (data.markdown) {
            let html = data.markdown
                .replace(/^# (.*$)/gim, '<h1 style="color:#1e3a8a; border-bottom:2px solid #1e3a8a; padding-bottom:8px; margin-bottom:14px;">$1</h1>')
                .replace(/^## (.*$)/gim, '<h2 style="color:#1e293b; margin-top:20px; margin-bottom:10px; font-size:18px;">$1</h2>')
                .replace(/^### (.*$)/gim, '<h3 style="color:#334155; margin-top:14px; font-size:15px;">$1</h3>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                .replace(/`([^`]+)`/gim, '<code>$1</code>')
                .replace(/\|(.+)\|/gim, (match) => {
                    const cells = match.split('|').filter(c => c.trim() !== '');
                    return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
                })
                .replace(/\n\n/gim, '<br><br>');

            viewer.innerHTML = `<div style="background:#ffffff; color:#1e293b; padding:24px; border-radius:8px; font-family:Plus Jakarta Sans, sans-serif; line-height:1.6;">${html}</div>`;
        }
    } catch (e) {}
}"""

new_load_report = """async function loadAcademicReport() {
    const viewer = document.getElementById('report-markdown-content');
    if (!viewer) return;
    viewer.innerHTML = '<div class="text-center p-4 text-muted"><i class="fa-solid fa-spinner fa-spin" style="font-size:24px;"></i><p class="mt-2">Compiling official academic performance report...</p></div>';

    try {
        const res = await fetch('/api/report/markdown');
        const data = await res.json();
        if (data.markdown) {
            let lines = data.markdown.split('\\n');
            let inTable = false;
            let htmlParts = [];

            for (let i = 0; i < lines.length; i++) {
                let line = lines[i].trim();
                
                if (line.startsWith('# ')) {
                    htmlParts.push(`<h1 style="color:#1e3a8a; border-bottom:2px solid #1e3a8a; padding-bottom:8px; margin:20px 0 12px 0; font-size:24px;">${line.substring(2)}</h1>`);
                } else if (line.startsWith('## ')) {
                    htmlParts.push(`<h2 style="color:#0f172a; border-bottom:1px solid #cbd5e1; padding-bottom:6px; margin:18px 0 10px 0; font-size:18px;">${line.substring(3)}</h2>`);
                } else if (line.startsWith('### ')) {
                    htmlParts.push(`<h3 style="color:#334155; margin:14px 0 8px 0; font-size:15px;">${line.substring(4)}</h3>`);
                } else if (line.startsWith('---')) {
                    htmlParts.push('<hr style="border:0; border-top:1px solid #e2e8f0; margin:16px 0;">');
                } else if (line.startsWith('|')) {
                    if (line.includes('---')) continue; // divider line
                    if (!inTable) {
                        inTable = true;
                        htmlParts.push('<div class="table-responsive my-2"><table class="data-table" style="background:#ffffff; color:#0f172a; width:100%; border:1px solid #cbd5e1; border-collapse:collapse; font-size:12.5px;">');
                    }
                    let cells = line.split('|').filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
                    let rowHtml = cells.map(c => `<td style="padding:7px 10px; border:1px solid #cbd5e1;">${c.trim()}</td>`).join('');
                    htmlParts.push(`<tr>${rowHtml}</tr>`);
                } else {
                    if (inTable) {
                        htmlParts.push('</table></div>');
                        inTable = false;
                    }
                    if (line.startsWith('- ')) {
                        htmlParts.push(`<li style="margin-left:20px; color:#334155; margin-bottom:4px;">${line.substring(2)}</li>`);
                    } else if (line) {
                        // format bold and italic
                        let formatted = line
                            .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                            .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                            .replace(/`([^`]+)`/g, '<code style="background:#f1f5f9; color:#1e293b; padding:2px 6px; border-radius:4px;">$1</code>');
                        htmlParts.push(`<p style="color:#334155; margin:6px 0; line-height:1.6;">${formatted}</p>`);
                    }
                }
            }
            if (inTable) htmlParts.push('</table></div>');

            viewer.innerHTML = `<div style="background:#ffffff; color:#1e293b; padding:28px 32px; border-radius:12px; font-family:'Plus Jakarta Sans', sans-serif; box-shadow:0 4px 20px rgba(0,0,0,0.15); line-height:1.6;">${htmlParts.join('')}</div>`;
        }
    } catch (e) {
        viewer.innerHTML = '<div class="text-center p-4 text-danger"><i class="fa-solid fa-triangle-exclamation" style="font-size:24px;"></i><p class="mt-2">Error loading academic performance report.</p></div>';
    }
}"""

if old_load_report in js:
    js = js.replace(old_load_report, new_load_report)
    print("Replaced loadAcademicReport in app.js")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Successfully updated app.py and app.js for Academic Report")

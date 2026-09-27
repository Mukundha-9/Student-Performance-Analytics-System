# fix_faculty_proctoring_layout.py
import re

# 1. Update static/js/app.js loadFacultyProctoring
with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

old_load_proctor = """async function loadFacultyProctoring(facultyId) {
    try {
        const res = await fetch(`/api/faculty/dashboard/${facultyId}`);
        const data = await res.json();

        const badgeAlert = document.getElementById('proctor-alert-count');
        if (badgeAlert) badgeAlert.innerText = `${data.at_risk_proctees_count || 0} Mentees Flagged At-Risk`;

        const tbody = document.getElementById('faculty-proctoring-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const proctees = data.proctees || [];
        proctees.forEach(p => {
            const tr = document.createElement('tr');
            const statusClass = p.is_at_risk ? 'text-danger' : 'text-success';
            tr.innerHTML = `
                <td><code>${p.student_id}</code></td>
                <td><strong>${p.name}</strong></td>
                <td>${p.branch}</td>
                <td class="${p.attendance < 75 ? 'badge-att-low' : ''}">${p.attendance}%</td>
                <td><strong>${p.percentage}%</strong></td>
                <td><span class="grade-badge grade-${p.grade.replace('+', '-plus')}">${p.grade}</span></td>
                <td><strong class="${statusClass}">${p.risk_reasons}</strong></td>
                <td><button class="btn btn-sm btn-primary" onclick="openProctorCounsellingModal('${p.student_id}', '${p.name}')"><i class="fa-solid fa-comments"></i> Mentor Log</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {}
}"""

new_load_proctor = """async function loadFacultyProctoring(facultyId) {
    try {
        const res = await fetch(`/api/faculty/dashboard/${facultyId}`);
        const data = await res.json();

        const badgeAlert = document.getElementById('proctor-alert-count');
        if (badgeAlert) badgeAlert.innerText = `${data.at_risk_proctees_count || 0} Mentees Flagged At-Risk`;

        const tbody = document.getElementById('faculty-proctoring-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const proctees = data.proctees || [];
        proctees.forEach(p => {
            const tr = document.createElement('tr');
            const isRisk = p.is_at_risk;
            const shortBranch = (p.branch || 'CSE')
                .replace('Computer Science & Engineering', 'CSE')
                .replace('Electronics & Communication', 'ECE')
                .replace('Information Technology', 'IT')
                .replace('Electrical & Electronics', 'EEE')
                .replace('Mechanical Engineering', 'MECH')
                .replace('Civil Engineering', 'CIVIL');

            tr.innerHTML = `
                <td><code>${p.student_id}</code></td>
                <td><strong>${p.name}</strong></td>
                <td><span class="badge badge-primary" style="font-size:10.5px;">${shortBranch}</span></td>
                <td class="${p.attendance < 75 ? 'badge-att-low' : 'badge-att-ok'}">${p.attendance}%</td>
                <td><strong>${p.percentage}%</strong></td>
                <td><span class="grade-badge grade-${p.grade.replace('+', '-plus')}">${p.grade}</span></td>
                <td>
                    <span class="badge ${isRisk ? 'badge-danger' : 'badge-success'}" style="font-size:11px; white-space:normal; max-width:180px; display:inline-block; line-height:1.3;">
                        <i class="fa-solid ${isRisk ? 'fa-triangle-exclamation' : 'fa-circle-check'}"></i> 
                        ${isRisk ? p.risk_reasons : 'Normal'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline" style="padding:4px 8px; font-size:11.5px;" onclick="openProctorCounsellingModal('${p.student_id}', '${p.name}')">
                        <i class="fa-solid fa-comment-dots"></i> Log Note
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {}
}"""

if old_load_proctor in js:
    js = js.replace(old_load_proctor, new_load_proctor)
    print("Replaced loadFacultyProctoring in app.js successfully.")
else:
    print("Warning: old loadFacultyProctoring pattern not exact match, using regex substitution.")
    js = re.sub(r"async function loadFacultyProctoring\(facultyId\) \{[\s\S]*?function initFacultyPortalEvents", new_load_proctor + "\n\nfunction initFacultyPortalEvents", js)

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

# 2. Append Layout and Width Fixes to static/css/style.css
css_fix = """
/* ==========================================================================
   FACULTY PROCTORING DESK STRICT RESPONSIVE FIT FIX
   ========================================================================== */

.main-content {
    margin-left: 270px;
    flex-grow: 1;
    padding: 20px 24px 60px 24px;
    width: calc(100vw - 270px);
    max-width: calc(100vw - 270px);
    box-sizing: border-box;
    min-width: 0;
    overflow-x: hidden;
}

#faculty-proctoring-tab {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

#faculty-proctoring-tab .panel-card {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    padding: 18px 20px;
}

#faculty-proctoring-tab .table-responsive {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow-x: auto;
    display: block;
    -webkit-overflow-scrolling: touch;
}

#faculty-proctoring-table {
    width: 100%;
    min-width: 650px;
    table-layout: auto;
}

#faculty-proctoring-table th,
#faculty-proctoring-table td {
    padding: 9px 10px;
    font-size: 12px;
}

.proctor-sub-view {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

.proctor-sub-view .grid-2-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}
"""

with open("static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_fix)

print("Successfully injected responsive fit fixes for faculty proctoring mentees into static/css/style.css")

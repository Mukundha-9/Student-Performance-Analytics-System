import os
import shutil

base = os.path.abspath('.')
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
startup = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

# 1. Copy to Desktop
src_bat = os.path.join(base, 'OPEN_ADITYA_PORTAL.bat')
dst_bat = os.path.join(desktop, 'OPEN_ADITYA_PORTAL.bat')
shutil.copyfile(src_bat, dst_bat)
print('Copied launcher to Desktop:', dst_bat)

# 2. Setup Windows Startup
if os.path.exists(startup):
    dst_vbs = os.path.join(startup, 'Aditya_Portal_AutoStart.vbs')
    service_py = os.path.join(base, 'live_service.py')
    vbs_content = 'Set WshShell = CreateObject("WScript.Shell")\n'
    vbs_content += f'WshShell.Run "py -3.13 ""{service_py}""", 0, False\n'
    with open(dst_vbs, 'w', encoding='utf-8') as f:
        f.write(vbs_content)
    print('Configured 24/7 Windows Startup Auto-Runner at:', dst_vbs)

import subprocess
import time
import os
import sys
import re
import threading
import urllib.request

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLASK_APP = os.path.join(BASE_DIR, 'app.py')
CLOUDFLARED = os.path.join(BASE_DIR, 'cloudflared.exe')
LINK_FILE = os.path.join(BASE_DIR, 'ACTIVE_PUBLIC_LINK.txt')
DESKTOP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')

current_public_url = None
url_event = threading.Event()

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    clean_msg = str(msg).encode('ascii', errors='replace').decode('ascii')
    print(f"[{t}] {clean_msg}", flush=True)

def update_desktop_shortcuts(public_url):
    try:
        # 1. Update text file in project
        with open(LINK_FILE, 'w', encoding='utf-8') as f:
            f.write(public_url)
        
        # 2. Update desktop files if Desktop exists
        if os.path.exists(DESKTOP_DIR):
            txt_path = os.path.join(DESKTOP_DIR, 'ADITYA_PORTAL_ONLINE_LINK.txt')
            url_path = os.path.join(DESKTOP_DIR, 'ADITYA_PORTAL_ONLINE.url')
            
            info_content = f"""======================================================================
ADITYA UNIVERSITY - STUDENT PERFORMANCE ANALYTICS & ERP PORTAL
======================================================================

Active Public Worldwide Link (Works on Any Phone / Mobile Data / PC):
{public_url}

Localhost PC Link:
http://localhost:5000  (or http://127.0.0.1:5000)

Login Credentials:
- Student: 25B11CS380  /  aditya@123
- Faculty: 50101       /  aditya@123
- Admin:   90001       /  aditya@123
======================================================================
"""
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(info_content)
                
            # Create Windows Internet Shortcut (.url)
            url_content = f"""[InternetShortcut]
URL={public_url}
IconIndex=0
"""
            with open(url_path, 'w', encoding='utf-8') as f:
                f.write(url_content)
            log(f"Updated Desktop Shortcuts with: {public_url}")
    except Exception as e:
        log(f"Shortcut update error: {e}")

def check_flask_healthy():
    try:
        with urllib.request.urlopen("http://127.0.0.1:5000", timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False

def start_flask():
    log("Starting Flask Server on 0.0.0.0:5000...")
    cmd = [sys.executable, FLASK_APP]
    proc = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return proc

def check_public_url_live(url):
    if not url:
        return False
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AdityaWatchdog/1.0'}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status in (200, 302, 304)
    except Exception:
        return False

def launch_tunnel():
    global current_public_url
    url_event.clear()
    log("Starting Cloudflare Secure Global Tunnel...")
    cmd = [CLOUDFLARED, 'tunnel', '--url', 'http://127.0.0.1:5000']
    proc = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='ignore',
        bufsize=1
    )

    def reader_thread():
        global current_public_url
        try:
            for line in iter(proc.stdout.readline, ''):
                clean = line.strip()
                if 'trycloudflare.com' in clean:
                    m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', clean)
                    if m and 'api.trycloudflare.com' not in m.group(0):
                        url = m.group(0)
                        if url != current_public_url:
                            current_public_url = url
                            log("="*70)
                            log(f"ACTIVE WORLDWIDE PUBLIC HTTPS LINK: {current_public_url}")
                            log("="*70)
                            update_desktop_shortcuts(current_public_url)
                            url_event.set()
        except Exception:
            pass

    t = threading.Thread(target=reader_thread, daemon=True)
    t.start()
    return proc

def run_service():
    global current_public_url
    log("=== Starting Aditya University All-Time 24/7 Live Service ===")

    # Ensure Flask is running
    flask_proc = None
    if not check_flask_healthy():
        flask_proc = start_flask()
        for _ in range(15):
            if check_flask_healthy():
                log("Flask Server is UP and healthy (200 OK)!")
                break
            time.sleep(1)
    else:
        log("Flask Server is already UP and responding on port 5000!")

    cf_proc = launch_tunnel()
    
    # Wait up to 15 seconds for initial public URL
    url_event.wait(timeout=15)

    fail_count = 0
    while True:
        time.sleep(15)

        # 1. Ensure Flask stays healthy
        if not check_flask_healthy():
            log("Flask is not responding! Reviving Flask...")
            if flask_proc and flask_proc.poll() is None:
                try:
                    flask_proc.kill()
                except Exception:
                    pass
            flask_proc = start_flask()
            time.sleep(3)

        # 2. Check Cloudflare process status
        if cf_proc.poll() is not None:
            log("Cloudflare tunnel process terminated! Restarting tunnel...")
            cf_proc = launch_tunnel()
            fail_count = 0
            continue

        # 3. Check public URL health actively
        if current_public_url:
            is_live = check_public_url_live(current_public_url)
            if not is_live:
                fail_count += 1
                log(f"Public URL probe failed ({fail_count}/3): {current_public_url}")
                if fail_count >= 3:
                    log("Public tunnel unreachable 3 consecutive times! Restarting fresh Cloudflare tunnel...")
                    try:
                        cf_proc.kill()
                    except Exception:
                        pass
                    cf_proc = launch_tunnel()
                    fail_count = 0
            else:
                if fail_count > 0:
                    log("Public URL probe succeeded again.")
                fail_count = 0

if __name__ == '__main__':
    run_service()

"""
Small desktop launcher for CyberVisionAI.

This script starts the Django development server in a background thread and
opens an embedded Chromium/Edge window using pywebview pointed at the
voice chat UI (`/chat/voice/`).

Build an executable using the provided `scripts/build_exe.ps1` script.

Notes:
- This is intended for local desktop usage. For production use a proper
  ASGI/WSGI server and packaging strategy is recommended.
"""
import os
import sys
import threading
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

def run_django():
    # Start the Django development server programmatically
    try:
        # Import here so Django settings are picked up after the env var
        from django.core.management import call_command
        call_command('runserver', '127.0.0.1:8000')
    except Exception as e:
        print('Error starting Django server:', e)


def wait_for_server(url='http://127.0.0.1:8000/', timeout=30.0):
    import requests
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def main():
    # Start Django server in background thread
    t = threading.Thread(target=run_django, daemon=True)
    t.start()

    # Wait for server to be ready
    print('Waiting for Django to start...')
    ok = wait_for_server('http://127.0.0.1:8000/')
    if not ok:
        print('Warning: Django server did not respond within timeout. The window may show an error.')

    # Launch embedded browser window
    try:
        import webview
    except Exception as e:
        print('pywebview is required to run the desktop app (pip install pywebview requests)')
        raise

    url = 'http://127.0.0.1:8000/chat/voice/'
    print('Opening UI at', url)
    webview.create_window('CyberVisionAI', url, width=1200, height=800)
    webview.start()


if __name__ == '__main__':
    main()

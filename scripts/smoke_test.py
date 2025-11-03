import os
import sys
import django
import json

# Ensure DJANGO_SETTINGS_MODULE is set to project settings (matches desktop_app.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Ensure repo root is on sys.path so 'project' package can be imported when this script
# is executed from the scripts/ directory or any other working directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

def main():
    try:
        django.setup()
    except Exception as e:
        print('Failed to setup Django environment:', e)
        sys.exit(2)

    # Use Django test client to call the AI endpoint in-process (bypasses CSRF/cookies)
    try:
        # Instead of calling the login-protected view, call the toolkit directly to validate
        # the assistant/backends are available and working.
        try:
            from genReport.toolkit import get_assistant_response
            print('Calling get_assistant_response(...)')
            reply = get_assistant_response('Smoke test prompt: Hello', '<o>{answer}</o>', model='X')
            print('Assistant reply:')
            print(reply)
        except Exception as e:
            print('Failed to call get_assistant_response:', e)
    except Exception as e:
        print('Smoke test POST failed:', e)
        sys.exit(3)

if __name__ == '__main__':
    main()

# Cyber Vision AI

<p align="center">
  <img src="./IMage_ghp/award.png" alt="Award" width="300"/>
</p>

A First-Place Award-Winning Graduation Project from the Faculty of Science, Zagazig University, Computer Science Department.

<p align="center">
  <img src="./IMage_ghp/x_logo.png" alt="X Model Logo" width="200"/>
</p>

<p align="center">
  <a href="https://github.com/bx0-0/CyberVisionAI"><img src="https://img.shields.io/github/stars/bx0-0/CyberVisionAI?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/bx0-0/CyberVisionAI"><img src="https://img.shields.io/github/forks/bx0-0/CyberVisionAI?style=social" alt="GitHub forks"></a>
  <a href="https://github.com/bx0-0/CyberVisionAI/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
</p>

---

## Overview

Cyber Vision AI is an advanced, open-source AI-powered assistant designed specifically for the cybersecurity community. This project, which won first place in the university's scientific conference for the Mathematics Division, was developed to overcome the limitations of conventional AI tools that often restrict security-related queries.

Our platform provides an unrestricted yet ethically-safeguarded environment for tasks such as vulnerability analysis, exploit explanation, and proof-of-concept code generation.

- **Fine-tuning Dataset:** The model was fine-tuned on a specialized dataset available at [saberbx/X-mini-datasets](https://huggingface.co/datasets/saberbx/X-mini-datasets).
- **Core Model:** The primary model used is [saberbx/XO](https://huggingface.co/saberbx/XO).

---

## Core Features

- **Deep Thinking Mode:** Delivers nuanced, analytically rich responses for complex cybersecurity problems.
- **Retrieval-Augmented Generation (RAG):** Provides highly personalized answers by searching your private vector database.
- **Deep Search & Multi-Agent Framework:** Conducts comprehensive, multi-stage searches and compiles in-depth, structured reports.
- **Voice Interaction:** Features high-accuracy speech-to-text and text-to-speech capabilities.
- **MindMap Generation:** Dynamically visualizes complex topics and plans as interactive mind maps using [Markmap-CLI](https://markmap.js.org/).
- **Live Web Search & Multi-AI Support:** Augments answers with real-time web data and insights from multiple top-tier AI models.

---

## Prerequisites

Before you begin, ensure you have the following installed and configured:

- Python 3.12+ and pip.
- **[Ollama](https://ollama.com/):** Install from [ollama.com](https://ollama.com/).
- **[Markmap-CLI](https://www.npmjs.com/package/markmap-cli):** Required for MindMap generation. Install it globally:
  ```bash
  npm install -g markmap-cli
  ```

---

## Step-by-Step Installation and Setup Guide

### Step 1: Set Up the AI Model with Ollama

- **Create the Model in Ollama:** The project expects a model named `X`.
- A ready-to-use Modelfile is available on the model's [Hugging Face page](https://huggingface.co/saberbx/XO).
- Run the following command in a new terminal to create the model. Ollama will automatically download it.
  ```bash
  ollama create X -f /path/to/your/Modelfile
  ```
  *Note: Replace the path with the actual location of your Modelfile.*
- **Verify:** Confirm the model is installed by running:
  ```bash
  ollama list
  ```
  You should see `X` in the list.

### Step 2: Set Up the Project and Environment

- **Clone the Repository:**
  ```bash
  git clone https://github.com/bx0-0/CyberVisionAI.git
  cd CyberVisionAI
  ```
- **Create and Activate a Virtual Environment:**
  ```bash
  python -m venv venv
  # On Windows
  .\venv\Scripts\activate
  ```
  *Important: Ensure the virtual environment (venv) is activated in every new terminal you use for running project commands.*
- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

### Step 3: Configure the Frontend Environment

- **Create a .env file:** Inside the `chat/streamlit_stricture` directory, create a new file named `.env`.
- **Add a Secret Key:** Open the `.env` file and add the following line. This key is used to encrypt and secure the initial communication between the Django and Streamlit servers. You can use the provided key or generate your own secure key.
  ```env
  SECRET_KEY=121f9d63c642ddd73325274068f4196aacd110b5f9ff3f882ff537046e81698b
  ```

### Step 4: Set Up the Django Database

- **Database Migrations:**
  ```bash
  # (Ensure venv is activated)
  python manage.py makemigrations
  python manage.py migrate
  ```
- **Create a Superuser:**
  ```bash
  python manage.py createsuperuser
  ```
  Follow the prompts to set up your admin credentials.

---

## How to Run the Application

To run Cyber Vision AI, you need to start several services in separate terminals.

### Core Services (Always Required)

- **Terminal 1: Start Ollama Server**
  ```bash
  ollama serve
  ```
- **Terminal 2: Start Django Backend Server**
  ```bash
  # (Ensure venv is activated)
  python manage.py runserver 8080
  ```
  The backend will now be running at http://localhost:8080.
- **Terminal 3: Start Streamlit Frontend**
  ```bash
  # (Ensure venv is activated)
  cd chat/streamlit_stricture
  streamlit run streamlit_chat.py --server.enableXsrfProtection false
  ```
  The frontend will now be running at http://localhost:8501.

### Optional Services (for RAG Feature)

If you wish to use the Retrieval-Augmented Generation (RAG) feature, you will need to run the following two servers in two additional terminals.

- **Terminal 4: Start Redis Server**
  (We recommend installing and running it via WSL):
  ```bash
  wsl
  redis-server
  ```
- **Terminal 5: Start Celery Worker**
  From the project's root directory:
  ```bash
  # (Ensure venv is activated)
  celery -A project worker --pool=solo --loglevel=info
  ```

---

## Accessing and Logging into the Application

- **Start with the Django Interface:**
  - Open your browser and navigate to http://localhost:8080.
  - Log in or create a new account.
- **Automatic Redirect:**
  - Upon successful login, the Django interface will automatically redirect you to the Streamlit application (http://localhost:8501).
  - Your authentication token will be passed securely in the background, ensuring you are logged in and ready to use the app without any manual steps.

---

## Quick Desktop Launcher (Windows)

You can start the app like a normal desktop app on Windows. From the project root there is a small helper script that opens separate PowerShell windows for the Django server and Celery worker and opens your browser.

1. Make sure the virtual environment `venv` exists and is created as described above.
2. From an elevated PowerShell run once to create a desktop shortcut:

```powershell
cd path\to\CyberVisionAI\scripts
.\create_desktop_shortcut.ps1
```

3. Double-click the `CyberVisionAI` shortcut on your Desktop. It will:
  - Open a PowerShell window running the Django server
  - Open a PowerShell window running the Celery worker
  - Open your default browser at http://localhost:8000

If you prefer to run manually, use:

```powershell
cd path\to\CyberVisionAI
.\scripts\start_app.ps1
```

Note: The scripts assume `venv` is in the project root and PowerShell execution policy allows running scripts. If blocked, run PowerShell as Administrator and allow execution for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Voice AI Chat

A lightweight voice-enabled chat page is available at `/chat/voice/` after you log in. It uses your browser's Web Speech API for speech-to-text and text-to-speech and sends prompts to the backend AI endpoint.

- Speak into your microphone, the page will transcribe and send the prompt to the AI.
- The assistant's reply will be shown and read aloud using your browser's TTS.

If you want to customize the backend AI model used, the endpoint `POST /chat/api/ai_chat/` accepts JSON `{ "prompt": "...", "model": "X" }` and returns `{ "response": "..." }`.

## Build a single-executable Desktop App (Windows)

If you want a single-folder or single-exe to distribute locally, you can bundle the small desktop launcher with PyInstaller. This script will start Django and show an embedded window using `pywebview`.

1. Install build dependencies in your activated venv:

```powershell
pip install pywebview requests pyinstaller
```

2. From the project root run the helper build script:

```powershell
cd scripts
.\build_exe.ps1
```

3. After the build completes, you'll find a `dist\CyberVisionAI_Desktop` folder. Copy the entire folder to the target machine. The Django project files (templates, static, media) should remain in their relative locations to the exe so the server can serve them.

Notes:
- I recommend using `--onedir` (the provided script) rather than `--onefile` because Django needs template/static files available on disk. If you want a true single-file bundle, you'll need additional packaging work to embed templates and static assets inside the executable, which is more complex.
- The resulting EXE runs the development server and is intended for local/offline use only.



## Configuration and Customization

- [`project/settings.py`](./project/settings.py): Main Django configuration. Here you can adjust the database, Redis broker URL for Celery, and other backend settings.
- [`chat/streamlit_stricture/streamlit_chat.py`](./chat/streamlit_stricture/streamlit_chat.py): Customize the Streamlit frontend, change the default Ollama model name, or adjust other UI/AI parameters.
- [`chat/streamlit_stricture/.env`](./chat/streamlit_stricture/.env): Stores the secret key for securing the initial server-to-server communication.

---

## A Note on the Audio (TTS) Feature

- The Text-to-Speech (TTS) feature in the current code was designed for an older version of the Kokoro model.
- The application will run perfectly without the TTS feature.
- If you wish to enable it, you will need to adapt the code in `tts.py` to work with the new version of the model.

---

## License

This project is licensed under the [MIT License](https://github.com/bx0-0/CyberVisionAI/blob/main/LICENSE).

---

## Troubleshooting (Redis, Celery & PyWebView on Windows)

- Redis not running / Celery can't connect:
  - On Windows it's easiest to run Redis via Docker:
    - Install Docker Desktop, then the provided `scripts\start_app.ps1` will attempt to start a Redis container named `cybervision_redis` automatically.
    - If you prefer WSL, install Redis inside your WSL distribution and run `redis-server` there.
  - If you can't run Redis, you can run Celery in a local-development mode by using the `--pool=solo` option (already used in our scripts) and avoid task dispatching that requires a broker. However, many async background tasks will not work without a broker.

- PyWebView / PyInstaller / pythonnet build errors when building the desktop EXE:
  - Building a Windows executable that imports `pywebview` can trigger the compilation of `pythonnet` on some systems, which requires MSBuild and .NET toolchain (and can fail during pip builds).
  - Workarounds:
    - Build on a machine with Visual Studio Build Tools (MSBuild) installed.
    - Use the provided `scripts\build_exe.ps1` but be prepared to install additional build tools if errors reference MSBuild or NuGet packages.
    - If you only need a local desktop launcher for development, install `pywebview` into your venv (`pip install pywebview requests`) and use `python desktop_app.py` instead of building an EXE.
    - If packaging continued to fail, consider distributing the `scripts\desktop_app.py` script and a small launcher that runs the project with an existing Python environment instead of a single exe.

If you want, I can:

- Walk you through installing Redis (Docker or WSL) and test Celery connectivity.
- Attempt a local build of the desktop EXE and iterate on any build failures (I can add helper scripts to gather full build logs and handle common MSBuild issues).

## USB hardware unlock (developer convenience)

You can provision a USB stick to act as a local unlock key for your project. This is a developer convenience mechanism (not a replacement for proper hardware security modules) and works offline.

Files added:
- `scripts/provision_usb.py` — create an encrypted file `cybervision_unlock.bin` on the USB root. Keep the password safe.
- `scripts/check_usb.py` — verify and decrypt the file using the password and print the unlock token.
- `scripts/usb_unlock.ps1` — interactive PowerShell wrapper for Windows which runs the check and stores the token to `.cybervision_unlock_token` in the repo root.

Quick usage (Windows PowerShell):

1. Provision a USB drive (run once):

```powershell
# from project root
python .\scripts\provision_usb.py --drive D: --password "YourStrongPassword"
```

2. Unlock (on any machine with the USB inserted):

```powershell
.\scripts\usb_unlock.ps1
# follow prompts for drive letter and password
```

The PowerShell helper writes the decrypted token to `.cybervision_unlock_token` in the repo root — other scripts can read that file to confirm the unlock state.

Security notes:
- The token is stored encrypted on the USB and protected by the password you choose. Keep the USB and password safe.
- This is intended for local developer convenience. For production-grade hardware-based keys consider using a YubiKey, a TPM-backed HSM, or platform-specific APIs.


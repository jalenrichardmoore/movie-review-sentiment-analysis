# Library imports
import subprocess
import sys
import os
import platform

# Creates a virtual environment
def create_venv():
    if not os.path.isdir('venv'):
        print("Creating virtual environment")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        print("Virtual environment already exists")

# Checks if dependencies are installed and, if not, installs them
def install_dependencies():
    print("Installing dependencies...")

    if platform.system() == "Windows": pip_path = os.path.join("venv", "Scripts", "pip.exe")
    else: pip_path = os.path.join("venv", "bin", "pip")

    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])

# Runs the streamlit app
def run_app():
    print("Launching Streamlit app...")

    if platform.system() == "Windows": python_path = os.path.join("venv", "Scripts", "python.exe")
    else: python_path = os.path.join("venv", "bin", "python")

    subprocess.check_call([python_path, "-m", "streamlit", "run", "app/app.py"])


if __name__ == "__main__":
    create_venv()
    install_dependencies()
    run_app()
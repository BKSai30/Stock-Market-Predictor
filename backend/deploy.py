import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True

def run_setup():
    """Run environment setup"""
    try:
        subprocess.check_call([sys.executable, "setup_environment.py"])
        print("Environment setup completed")
    except subprocess.CalledProcessError as e:
        print(f"Error running setup: {e}")
        return False
    return True

def start_application():
    """Start the Flask application"""
    try:
        print("Starting Stock Market Predictor application...")
        print("Application will be available at: http://localhost:5000")
        subprocess.check_call([sys.executable, "run.py"])
    except KeyboardInterrupt:
        print("Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")

if __name__ == '__main__':
    print("Deploying Stock Market Predictor...")
    
    if install_requirements() and run_setup():
        start_application()
    else:
        print("Deployment failed!")
        sys.exit(1)

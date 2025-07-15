#!/usr/bin/env python3
"""
Launch script for the Healthcare SQL Analytics Platform
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    required_packages = [
        "streamlit",
        "sqlparse",
        "pandas",
        "langchain",
        "langchain-google-genai",
        "tiktoken",
        "python-dotenv"
    ]
    
    print("🔧 Installing required packages...")
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def launch_app():
    """Launch the Streamlit app"""
    print("🚀 Launching Healthcare SQL Analytics Platform...")
    print("📱 The app will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.serverAddress", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Healthcare SQL Analytics Platform!")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    print("🏥 Healthcare SQL Analytics Platform Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run from the project directory.")
        sys.exit(1)
    
    # Install requirements (optional)
    if "--install" in sys.argv:
        install_requirements()
    
    # Launch the app
    launch_app()

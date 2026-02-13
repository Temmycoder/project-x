#!/usr/bin/env python3
"""
Setup script for X-Share
Installs dependencies for both backend and frontend
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a shell command and report status"""
    if description:
        print(f"\n📦 {description}")
    print(f"   Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"   ✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed: {e.stderr}")
        return False

def setup_backend():
    """Setup Python backend"""
    print("\n" + "="*50)
    print("🐍 Setting up Python Backend")
    print("="*50)
    
    # Navigate to backend
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_path)
    
    # Check Python version
    version_check = subprocess.run(
        [sys.executable, '--version'],
        capture_output=True,
        text=True
    )
    print(f"\n✨ Python Version: {version_check.stdout.strip()}")
    
    # Install requirements
    if not run_command(
        [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
        "Installing Python dependencies..."
    ):
        return False
    
    return True

def setup_frontend():
    """Setup Electron/React frontend"""
    print("\n" + "="*50)
    print("⚛️  Setting up Electron/React Frontend")
    print("="*50)
    
    # Navigate to electron app
    frontend_path = os.path.join(
        os.path.dirname(__file__), 
        'electron-app'
    )
    os.chdir(frontend_path)
    
    # Check Node version
    version_check = subprocess.run(
        ['node', '--version'],
        capture_output=True,
        text=True
    )
    print(f"\n✨ Node Version: {version_check.stdout.strip()}")
    
    # Install dependencies
    if not run_command(
        ['npm', 'install'],
        "Installing Node dependencies..."
    ):
        return False
    
    return True

def main():
    """Main setup function"""
    print("""
    ╔════════════════════════════════════╗
    ║       X-Share Setup Wizard          ║
    ║   Professional Screen Sharing       ║
    ╚════════════════════════════════════╝
    """)
    
    # Check system
    system = platform.system()
    print(f"💻 System: {system}")
    print(f"🐍 Python: {sys.executable}")
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed!")
        sys.exit(1)
    
    # Success
    print("\n" + "="*50)
    print("✅ Setup Complete!")
    print("="*50)
    print("""
    Next steps:
    
    1. Start Python Server (Terminal 1):
       cd backend
       python server.py
    
    2. Start Electron App (Terminal 2):
       cd electron-app
       npm run dev
    
    3. Open http://localhost:3000 in your browser
    
    For production build:
       npm run build
    
    Happy streaming! 🚀
    """)

if __name__ == '__main__':
    main()

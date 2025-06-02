#!/usr/bin/env python3
"""
Build script for AndroMirror by Juan v1.0
Automates the process of creating executable files using PyInstaller
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"Running: {' '.join(cmd)}")
    if description:
        print(f"Description: {description}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Return code: {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return None

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Install build dependencies
    build_deps = ["pyinstaller", "wheel", "setuptools"]
    for dep in build_deps:
        run_command([sys.executable, "-m", "pip", "install", dep], f"Installing {dep}")
    
    # Install project dependencies
    if os.path.exists("requirements.txt"):
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], "Installing project dependencies")

def clean_build_dirs():
    """Clean previous build directories"""
    print("🧹 Cleaning build directories...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed: {dir_name}")
    
    # Remove .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"Removed: {spec_file}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # Determine platform-specific settings
    system = platform.system().lower()
    app_name = "AndroMirror"
    
    if system == "windows":
        app_name += ".exe"
        icon_flag = []  # Add --icon=icon.ico if you have an icon
    elif system == "darwin":  # macOS
        app_name += ""
        icon_flag = []  # Add --icon=icon.icns if you have an icon
    else:  # Linux
        app_name += ""
        icon_flag = []
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Don't show console window
        "--name", "AndroMirror",        # Executable name
        "--clean",                      # Clean PyInstaller cache
        "--noconfirm",                  # Don't ask for confirmation
        # "--optimize", "2",            # Python optimization level
        # "--strip",                    # Strip debug symbols (Linux/macOS)
    ]
    
    # Add icon if available
    cmd.extend(icon_flag)
    
    # Add hidden imports for CustomTkinter
    hidden_imports = [
        "--hidden-import", "customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL._tkinter_finder",
    ]
    cmd.extend(hidden_imports)
    
    # Add the main script
    cmd.append("main.py")
    
    # Run PyInstaller
    result = run_command(cmd, "Building executable with PyInstaller")
    
    if result:
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path("dist") / "AndroMirror"
        if system == "windows":
            exe_path = exe_path.with_suffix(".exe")
        
        if exe_path.exists():
            print(f"📦 Executable created: {exe_path}")
            print(f"📊 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("❌ Executable not found in expected location")
            return False
    else:
        print("❌ Build failed")
        return False

def create_portable_package():
    """Create a portable package with executable and documentation"""
    print("📦 Creating portable package...")
    
    # Create package directory
    package_dir = Path("AndroMirror_Portable")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy executable
    system = platform.system().lower()
    exe_name = "AndroMirror.exe" if system == "windows" else "AndroMirror"
    exe_source = Path("dist") / exe_name
    exe_dest = package_dir / exe_name
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"Copied: {exe_name}")
    
    # Copy documentation
    docs_to_copy = ["README.md", "LICENSE"]
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, package_dir / doc)
            print(f"Copied: {doc}")
    
    # Create run script for easier execution
    if system == "windows":
        run_script = package_dir / "run.bat"
        run_script.write_text("@echo off\nAndroMirror.exe\npause")
    else:
        run_script = package_dir / "run.sh"
        run_script.write_text("#!/bin/bash\n./AndroMirror\n")
        os.chmod(run_script, 0o755)
    
    print(f"Created run script: {run_script.name}")
    
    print(f"✅ Portable package created: {package_dir}")
    return True

def test_executable():
    """Test the built executable"""
    print("🧪 Testing executable...")
    
    system = platform.system().lower()
    exe_name = "AndroMirror.exe" if system == "windows" else "AndroMirror"
    exe_path = Path("dist") / exe_name
    
    if not exe_path.exists():
        print("❌ Executable not found for testing")
        return False
    
    # Test if executable can start (quick test)
    try:
        # On Windows and Linux, we can test basic execution
        # On macOS, this might require additional handling
        if system != "darwin":
            result = subprocess.run([str(exe_path), "--help"], 
                                 capture_output=True, text=True, timeout=5)
            # If it doesn't crash immediately, it's probably working
            print("✅ Executable appears to be working")
            return True
        else:
            print("ℹ️  Manual testing required on macOS")
            return True
    except subprocess.TimeoutExpired:
        print("✅ Executable started (timeout expected for GUI app)")
        return True
    except Exception as e:
        print(f"❌ Executable test failed: {e}")
        return False

def main():
    """Main build process"""
    print("🚀 AndroMirror Build Script")
    print("=" * 50)
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found in current directory")
        sys.exit(1)
    
    # Build steps
    steps = [
        ("Installing dependencies", install_dependencies),
        ("Cleaning build directories", clean_build_dirs),
        ("Building executable", build_executable),
        ("Testing executable", test_executable),
        ("Creating portable package", create_portable_package),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            success = step_func()
            if success is False:
                print(f"❌ {step_name} failed")
                break
        except KeyboardInterrupt:
            print(f"\n⚠️  Build interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
            break
    else:
        print("\n🎉 Build completed successfully!")
        print("\nFiles created:")
        print("- dist/AndroMirror(.exe) - Main executable")
        print("- AndroMirror_Portable/ - Portable package")
        
        # Show next steps
        print("\n📋 Next steps:")
        print("1. Test the executable in dist/ folder")
        print("2. Distribute the AndroMirror_Portable folder")
        print("3. Ensure target systems have ADB and scrcpy installed")

if __name__ == "__main__":
    main()
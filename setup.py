#!/usr/bin/env python3
"""
Setup configuration for AndroMirror by Juan v1.0
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="andromirror",
    version="1.0.0",
    author="Juan Madhy",
    author_email="juanmadhy425@gmail.com",
    description="Modern GUI frontend for scrcpy with Android device mirroring capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/andromirror",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/andromirror/issues",
        "Source": "https://github.com/yourusername/andromirror",
        "Developer Instagram": "https://instagram.com/jeyy_prtf",
        "Developer LinkedIn": "https://www.linkedin.com/in/inijuan/",
    },
    packages=find_packages(),
    py_modules=["main"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Topic :: Desktop Environment",
        "Topic :: System :: Hardware",
        "Topic :: Multimedia :: Graphics :: Viewers",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pyinstaller>=5.0",
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
        "build": [
            "pyinstaller>=5.0",
            "nuitka>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "andromirror=main:main",
        ],
        "gui_scripts": [
            "andromirror-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    zip_safe=False,
    keywords=[
        "android", "scrcpy", "screen-mirroring", "adb", "gui", 
        "device-control", "remote-control", "mobile", "debugging",
        "customtkinter", "cross-platform"
    ],
    platforms=["Windows", "Linux", "macOS"],
)
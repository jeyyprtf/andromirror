#!/usr/bin/env python3
"""
AndroMirror by Juan v1.0
Modern GUI frontend for scrcpy with Android device mirroring capabilities
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import time
import sys
import os
import webbrowser
from typing import List, Dict, Optional

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AndroMirrorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AndroMirror by Juan v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        
        # Variables
        self.devices = []
        self.selected_device = None
        self.scrcpy_process = None
        
        # Settings variables
        self.resolution = ctk.StringVar(value="HD (720p)")
        self.fps = ctk.StringVar(value="60")
        self.video_codec = ctk.StringVar(value="h264")
        self.bitrate = ctk.StringVar(value="8M")
        self.audio_enabled = ctk.BooleanVar(value=True)
        self.audio_quality = ctk.StringVar(value="Medium")
        self.stay_awake = ctk.BooleanVar(value=True)
        self.screen_off = ctk.BooleanVar(value=False)
        self.keyboard_mode = ctk.StringVar(value="uhid")
        self.mouse_mode = ctk.StringVar(value="uhid")
        self.theme_mode = ctk.StringVar(value="System")
        
        self.setup_ui()
        self.refresh_devices()
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header frame
        self.create_header()
        
        # Main content frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Add tabs
        self.tabview.add("Device Connection")
        self.tabview.add("Settings")
        self.tabview.add("About")
        
        # Setup each tab
        self.setup_connection_tab()
        self.setup_settings_tab()
        self.setup_about_tab()
        
    def create_header(self):
        """Create the header with title and theme toggle"""
        header_frame = ctk.CTkFrame(self.root)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # App title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="AndroMirror by Juan v1.0",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=15)
        
        # Theme toggle
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.grid(row=0, column=2, padx=20, pady=15)
        
        ctk.CTkLabel(theme_frame, text="Theme:").grid(row=0, column=0, padx=(0, 10))
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_mode,
            values=["System", "Light", "Dark"],
            command=self.change_theme
        )
        theme_menu.grid(row=0, column=1)
        
    def setup_connection_tab(self):
        """Setup the device connection tab"""
        tab = self.tabview.tab("Device Connection")
        tab.grid_columnconfigure(1, weight=1)
        
        # Left side - Device list
        device_frame = ctk.CTkFrame(tab)
        device_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        device_frame.grid_columnconfigure(0, weight=1)
        
        # Device list header
        header_frame = ctk.CTkFrame(device_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame, 
            text="Connected Devices",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        self.refresh_btn = ctk.CTkButton(
            header_frame,
            text="Refresh",
            width=80,
            command=self.refresh_devices
        )
        self.refresh_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Device listbox
        self.device_listbox = tk.Listbox(
            device_frame,
            height=8,
            font=("SF Pro Display", 11) if sys.platform == "darwin" else ("Segoe UI", 10),
            selectmode=tk.SINGLE
        )
        self.device_listbox.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.device_listbox.bind('<<ListboxSelect>>', self.on_device_select)
        
        # Connection controls
        connection_frame = ctk.CTkFrame(device_frame, fg_color="transparent")
        connection_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        connection_frame.grid_columnconfigure(0, weight=1)
        
        self.connect_btn = ctk.CTkButton(
            connection_frame,
            text="Connect",
            height=40,
            state="disabled",
            command=self.connect_device
        )
        self.connect_btn.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(connection_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(connection_frame, text="Select a device to connect")
        self.status_label.grid(row=2, column=0, pady=(10, 0))
        
        # Right side - Wireless connection
        wireless_frame = ctk.CTkFrame(tab)
        wireless_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        ctk.CTkLabel(
            wireless_frame,
            text="Wireless Connection",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15))
        
        ctk.CTkLabel(wireless_frame, text="IP Address:").grid(row=1, column=0, padx=(20, 10), pady=5, sticky="w")
        self.ip_entry = ctk.CTkEntry(wireless_frame, placeholder_text="192.168.1.100")
        self.ip_entry.grid(row=1, column=1, padx=(0, 20), pady=5, sticky="ew")
        
        ctk.CTkLabel(wireless_frame, text="Port:").grid(row=2, column=0, padx=(20, 10), pady=5, sticky="w")
        self.port_entry = ctk.CTkEntry(wireless_frame, placeholder_text="5555")
        self.port_entry.grid(row=2, column=1, padx=(0, 20), pady=5, sticky="ew")
        
        self.wireless_connect_btn = ctk.CTkButton(
            wireless_frame,
            text="Connect Wireless",
            command=self.connect_wireless
        )
        self.wireless_connect_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        
        # Instructions
        instructions = """Instructions:
1. Enable USB Debugging on your Android device
2. Connect via USB or use wireless connection
3. Select device from the list
4. Configure settings in Settings tab
5. Click Connect to start mirroring"""
        
        ctk.CTkLabel(
            wireless_frame,
            text=instructions,
            justify="left",
            wraplength=300
        ).grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 20), sticky="w")
        
    def setup_settings_tab(self):
        """Setup the settings tab"""
        tab = self.tabview.tab("Settings")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(tab)
        scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Video Settings
        ctk.CTkLabel(
            scrollable_frame,
            text="Video Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=row, column=0, columnspan=2, padx=20, pady=(20, 15), sticky="w")
        row += 1
        
        # Resolution
        ctk.CTkLabel(scrollable_frame, text="Resolution:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.resolution,
            values=["SD (540p)", "HD (720p)", "FHD (1080p)", "4K"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
        # FPS
        ctk.CTkLabel(scrollable_frame, text="FPS:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.fps,
            values=["30", "60", "120"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
        # Video Codec
        ctk.CTkLabel(scrollable_frame, text="Video Codec:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.video_codec,
            values=["h264", "h265"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
        # Bitrate
        ctk.CTkLabel(scrollable_frame, text="Video Bitrate:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.bitrate,
            values=["4M", "8M", "16M", "30M"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
        # Audio Settings
        ctk.CTkLabel(
            scrollable_frame,
            text="Audio Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=row, column=0, columnspan=2, padx=20, pady=(30, 15), sticky="w")
        row += 1
        
        # Audio Enable/Disable
        ctk.CTkLabel(scrollable_frame, text="Audio:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkSwitch(
            scrollable_frame,
            text="Enable Audio",
            variable=self.audio_enabled
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="w")
        row += 1
        
        # Audio Quality
        ctk.CTkLabel(scrollable_frame, text="Audio Quality:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.audio_quality,
            values=["Low", "Medium", "High"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
        # Device Settings
        ctk.CTkLabel(
            scrollable_frame,
            text="Device Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=row, column=0, columnspan=2, padx=20, pady=(30, 15), sticky="w")
        row += 1
        
        # Stay Awake
        ctk.CTkLabel(scrollable_frame, text="Stay Awake:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkSwitch(
            scrollable_frame,
            text="Keep device awake",
            variable=self.stay_awake
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="w")
        row += 1
        
        # Screen Off
        ctk.CTkLabel(scrollable_frame, text="Screen Off:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkSwitch(
            scrollable_frame,
            text="Turn off device screen",
            variable=self.screen_off
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="w")
        row += 1
        
        # Input Settings
        ctk.CTkLabel(
            scrollable_frame,
            text="Input Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=row, column=0, columnspan=2, padx=20, pady=(30, 15), sticky="w")
        row += 1
        
        # Keyboard Mode
        ctk.CTkLabel(scrollable_frame, text="Keyboard Mode:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.keyboard_mode,
            values=["uhid", "sdk"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
        # Mouse Mode
        ctk.CTkLabel(scrollable_frame, text="Mouse Mode:").grid(row=row, column=0, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkOptionMenu(
            scrollable_frame,
            variable=self.mouse_mode,
            values=["uhid", "sdk"]
        ).grid(row=row, column=1, padx=(0, 20), pady=5, sticky="ew")
        row += 1
        
    def setup_about_tab(self):
        """Setup the about tab"""
        tab = self.tabview.tab("About")
        
        # Main container
        about_frame = ctk.CTkFrame(tab, fg_color="transparent")
        about_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        about_frame.grid_columnconfigure(0, weight=1)
        
        # App info
        ctk.CTkLabel(
            about_frame,
            text="AndroMirror by Juan v1.0",
            font=ctk.CTkFont(size=28, weight="bold")
        ).grid(row=0, column=0, pady=(0, 10))
        
        ctk.CTkLabel(
            about_frame,
            text="Modern GUI frontend for scrcpy",
            font=ctk.CTkFont(size=16)
        ).grid(row=1, column=0, pady=(0, 30))
        
        # Developer info
        ctk.CTkLabel(
            about_frame,
            text="Developer Contact",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=2, column=0, pady=(0, 15))
        
        # Social media buttons
        social_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        social_frame.grid(row=3, column=0, pady=(0, 20))
        
        # Instagram
        ctk.CTkButton(
            social_frame,
            text="📷 Instagram: @jeyy_prtf",
            command=lambda: webbrowser.open("https://instagram.com/jeyy_prtf"),
            width=250
        ).grid(row=0, column=0, pady=5)
        
        # LinkedIn
        ctk.CTkButton(
            social_frame,
            text="💼 LinkedIn Profile",
            command=lambda: webbrowser.open("https://www.linkedin.com/in/inijuan/"),
            width=250
        ).grid(row=1, column=0, pady=5)
        
        # TikTok
        ctk.CTkButton(
            social_frame,
            text="🎵 TikTok: @jeyy_prtf",
            command=lambda: webbrowser.open("https://tiktok.com/@jeyy_prtf"),
            width=250
        ).grid(row=2, column=0, pady=5)
        
        # Email
        ctk.CTkButton(
            social_frame,
            text="📧 Email: juanmadhy425@gmail.com",
            command=lambda: webbrowser.open("mailto:juanmadhy425@gmail.com"),
            width=250
        ).grid(row=3, column=0, pady=5)
        
        # WhatsApp
        ctk.CTkButton(
            social_frame,
            text="📱 WhatsApp: 088805385353",
            command=lambda: webbrowser.open("https://wa.me/6288805385353"),
            width=250
        ).grid(row=4, column=0, pady=5)
        
        # Credits
        credits_text = """Built with Python & CustomTkinter
Powered by scrcpy for Android mirroring
Made with ❤️ for the Android development community"""
        
        ctk.CTkLabel(
            about_frame,
            text=credits_text,
            justify="center",
            font=ctk.CTkFont(size=12)
        ).grid(row=4, column=0, pady=(30, 0))
        
    def change_theme(self, mode):
        """Change the application theme"""
        ctk.set_appearance_mode(mode)
        
    def refresh_devices(self):
        """Refresh the list of connected devices"""
        self.refresh_btn.configure(state="disabled", text="Refreshing...")
        self.status_label.configure(text="Refreshing devices...")
        
        def refresh_thread():
            try:
                # Run adb devices command
                result = subprocess.run(
                    ["adb", "devices"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    devices = []
                    
                    for line in lines:
                        if line.strip() and '\t' in line:
                            device_id, status = line.strip().split('\t')
                            if status == 'device':
                                devices.append(device_id)
                    
                    # Update UI in main thread
                    self.root.after(0, self.update_device_list, devices)
                else:
                    self.root.after(0, self.show_error, "ADB not found or not in PATH")
                    
            except subprocess.TimeoutExpired:
                self.root.after(0, self.show_error, "ADB command timed out")
            except FileNotFoundError:
                self.root.after(0, self.show_error, "ADB not found. Please install Android SDK Platform Tools")
            except Exception as e:
                self.root.after(0, self.show_error, f"Error refreshing devices: {str(e)}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
        
    def update_device_list(self, devices):
        """Update the device list in the UI"""
        self.devices = devices
        self.device_listbox.delete(0, tk.END)
        
        if devices:
            for device in devices:
                self.device_listbox.insert(tk.END, device)
            self.status_label.configure(text=f"Found {len(devices)} device(s)")
        else:
            self.device_listbox.insert(tk.END, "No devices found")
            self.status_label.configure(text="No devices connected")
            
        self.refresh_btn.configure(state="normal", text="Refresh")
        self.update_connect_button()
        
    def show_error(self, message):
        """Show error message"""
        self.status_label.configure(text=message)
        self.refresh_btn.configure(state="normal", text="Refresh")
        messagebox.showerror("Error", message)
        
    def on_device_select(self, event):
        """Handle device selection"""
        selection = self.device_listbox.curselection()
        if selection and self.devices:
            self.selected_device = self.devices[selection[0]]
            self.status_label.configure(text=f"Selected: {self.selected_device}")
        else:
            self.selected_device = None
            self.status_label.configure(text="No device selected")
            
        self.update_connect_button()
        
    def update_connect_button(self):
        """Update the connect button state"""
        if self.selected_device and self.selected_device in self.devices:
            self.connect_btn.configure(state="normal")
        else:
            self.connect_btn.configure(state="disabled")
            
    def connect_wireless(self):
        """Connect to device wirelessly"""
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip() or "5555"
        
        if not ip:
            messagebox.showerror("Error", "Please enter IP address")
            return
            
        self.wireless_connect_btn.configure(state="disabled", text="Connecting...")
        
        def connect_thread():
            try:
                # Connect to wireless device
                result = subprocess.run(
                    ["adb", "connect", f"{ip}:{port}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 and ("connected" in result.stdout.lower() or "already connected" in result.stdout.lower()):
                    self.root.after(0, lambda: self.wireless_connect_btn.configure(state="normal", text="Connect Wireless"))
                    self.root.after(0, self.refresh_devices)
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"Connected to {ip}:{port}"))
                else:
                    error_msg = result.stdout or result.stderr or "Connection failed"
                    self.root.after(0, lambda: messagebox.showerror("Connection Failed", error_msg))
                    self.root.after(0, lambda: self.wireless_connect_btn.configure(state="normal", text="Connect Wireless"))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Connection error: {str(e)}"))
                self.root.after(0, lambda: self.wireless_connect_btn.configure(state="normal", text="Connect Wireless"))
        
        threading.Thread(target=connect_thread, daemon=True).start()
        
    def connect_device(self):
        """Connect to the selected device using scrcpy"""
        if not self.selected_device:
            return
            
        self.connect_btn.configure(state="disabled", text="Connecting...")
        self.progress_bar.set(0.2)
        self.status_label.configure(text="Starting scrcpy...")
        
        def connect_thread():
            try:
                # Build scrcpy command
                cmd = ["scrcpy", "-s", self.selected_device]
                
                # Add video settings
                resolution_map = {
                    "SD (540p)": "540",
                    "HD (720p)": "720", 
                    "FHD (1080p)": "1080",
                    "4K": "2160"
                }
                if self.resolution.get() in resolution_map:
                    cmd.extend(["-m", resolution_map[self.resolution.get()]])
                
                # FPS
                cmd.extend(["--max-fps", self.fps.get()])
                
                # Video codec
                cmd.extend(["--video-codec", self.video_codec.get()])
                
                # Bitrate
                cmd.extend(["-b", self.bitrate.get()])
                
                # Audio settings
                if not self.audio_enabled.get():
                    cmd.append("--no-audio")
                else:
                    audio_bitrate_map = {"Low": "64K", "Medium": "128K", "High": "320K"}
                    cmd.extend(["--audio-bit-rate", audio_bitrate_map[self.audio_quality.get()]])
                
                # Device settings
                if self.stay_awake.get():
                    cmd.append("--stay-awake")
                    
                if self.screen_off.get():
                    cmd.append("--turn-screen-off")
                
                # Input settings
                cmd.extend(["--keyboard", self.keyboard_mode.get()])
                cmd.extend(["--mouse", self.mouse_mode.get()])
                
                self.root.after(0, lambda: self.progress_bar.set(0.6))
                
                # Start scrcpy
                self.scrcpy_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                
                self.root.after(0, lambda: self.progress_bar.set(1.0))
                self.root.after(0, lambda: self.status_label.configure(text="scrcpy started successfully!"))
                self.root.after(0, lambda: self.connect_btn.configure(state="normal", text="Disconnect"))
                
                # Wait for process to complete
                self.scrcpy_process.wait()
                
                # Reset UI when scrcpy closes
                self.root.after(0, self.reset_connection_ui)
                
            except FileNotFoundError:
                self.root.after(0, lambda: messagebox.showerror("Error", "scrcpy not found. Please install scrcpy and add it to PATH"))
                self.root.after(0, self.reset_connection_ui)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}"))
                self.root.after(0, self.reset_connection_ui)
        
        if self.scrcpy_process and self.scrcpy_process.poll() is None:
            # Disconnect current session
            self.scrcpy_process.terminate()
            self.scrcpy_process = None
            self.reset_connection_ui()
        else:
            # Start new connection
            threading.Thread(target=connect_thread, daemon=True).start()
            
    def reset_connection_ui(self):
        """Reset the connection UI to initial state"""
        self.connect_btn.configure(state="normal" if self.selected_device else "disabled", text="Connect")
        self.progress_bar.set(0)
        self.status_label.configure(text="Ready to connect" if self.selected_device else "Select a device to connect")
        
    def run(self):
        """Start the application"""
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the main loop
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        if self.scrcpy_process and self.scrcpy_process.poll() is None:
            self.scrcpy_process.terminate()
        self.root.quit()
        self.root.destroy()

def main():
    """Main entry point"""
    try:
        app = AndroMirrorApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")

if __name__ == "__main__":
    main()
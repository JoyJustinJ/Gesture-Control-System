Gesture Control System

A real-time computer vision-based gesture recognition system that enables touchless interaction with a computer using hand gestures. This project uses Python, OpenCV, MediaPipe, and PyAutoGUI to detect hand landmarks and map gestures to system-level actions.

Overview

The Gesture Control System captures live video input from a webcam and detects hand landmarks using MediaPipe. Based on the relative positions of detected landmarks, specific gestures are identified and mapped to predefined system commands such as opening applications, switching windows, or taking screenshots.

The system includes a cooldown mechanism to prevent repeated triggering of actions and supports multiple gesture types for enhanced interaction.

Features

Real-time hand tracking and gesture recognition
Landmark-based gesture detection
Touchless system control
Application launching through gestures
Window management functionality
Screenshot capture
Multi-hand gesture detection
Cooldown mechanism to prevent repeated commands

Supported Gestures and Actions
Gesture	Action

Palm Open	Open Notepad
Peace Sign	Open Calculator
Thumb Up	Open Browser
Ring Finger Up	Take Screenshot
Swipe Up	Close Active Window
Swipe Left	Switch to Next Window
Swipe Right	Switch to Previous Window
Two Index Fingers	Minimize Window
Two Middle Fingers	Maximize Window

Technologies Used

Python
OpenCV (video capture and frame processing)
MediaPipe Hands (hand landmark detection)
PyAutoGUI (system automation and keyboard shortcuts)
OS module (application launching)
Time module (gesture cooldown handling)
System Architecture
Capture live webcam feed using OpenCV.
Process frames using MediaPipe to detect 21 hand landmarks.
Analyze landmark positions to classify gestures.
Map detected gestures to predefined system actions.
Execute commands using PyAutoGUI or OS-level calls.
Apply cooldown timing to ensure stable performance.

Installation

Clone the Repository
git clone https://github.com/JoyJustinJ/Gesture-Control-System.git
cd gesture-control-system

Install Dependencies
pip install opencv-python mediapipe pyautogui

Running the Application
python gesture_control.py


Press Q to exit the application.

System Requirements

Windows operating system
Python 3.8 or higher
Webcam

Note: Some application-launch commands are configured specifically for Windows (e.g., notepad.exe, calc.exe, chrome.exe).

Project Highlights

Real-time computer vision application
Landmark-based gesture classification
Integration of computer vision with system automation
Clean modular structure for future expansion
Practical human-computer interaction implementation

Future Enhancements

Cross-platform compatibility (Linux and macOS)
Custom gesture configuration
Volume and brightness control
Presentation control mode
Machine learning-based gesture classifier
Graphical user interface

Use Cases

Touchless computing environments
Accessibility support
Smart presentation systems
Interactive kiosks
Human-computer interaction research



Author

Joy Justin J
B.Tech – Artificial Intelligence and Data Science

jkjustin1805@gmail.com

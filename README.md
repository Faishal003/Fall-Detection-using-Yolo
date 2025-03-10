# Fall-Detection-using-Yolo

This is a fall detection system designed to detect human falls in real-time using a Raspberry Pi, a camera, and computer vision techniques. The system uses YOLOv5 for human detection, calculates motion parameters (speed, angle, aspect ratio), and triggers actions such as playing a sound and sending an email alert when a fall is detected.

# 💥 Features 💥
* Real-time human fall detection using YOLOv5 model.
* Sends an email alert upon detecting a fall.
* Plays an alert sound when a fall is detected.
* Records the detection video with bounding boxes and fall status.

# Setup Instructions
# 1. Clone the Repository
```
https://github.com/Faishal003/Fall-Detection-using-Yolo.git
cd fall-detection
```
# 2. Create and Activate a Virtual Environment
Creating a virtual environment ensures that the project dependencies are isolated from your system's global Python packages.
 
 - **Create a virtual environment:**

   For Linux/macOS:
   ```
   python3 -m venv fall
   ```

   For Windows:
   ```
   python -m venv fall
   ```
- **Activate the virtual environment:**

  For Linux/macOS:
  ```
  source fall/bin/activate
  ```

  For Windows:
  ```
  .\fall\Scripts\activate
  ```

# 2. Install Dependencies
 Make sure you have Python version `3.10.x or upper` 👈<br>
```
pip install -r requirements.txt
```
This will install all the necessary libraries, including `opencv-python`, `pygame`, `smptlib`, `ultralytics`, and more.
# 3. Set Up Email Configuration
# 4. Set Up Camera
For real-time detection, connect a Raspberry Pi Camera or Webcam. The system will automatically use it to capture video for detection.

# Usage
# 1. Start the Fall Detection System
Once everything is set up, you can start the fall detection script:
```
python Project.py
```
## Watch the Demo
You can download and watch the fall detection demo video:

[https://github.com/user-attachments/assets/0ff74cfc-f977-4b73-bf4f-c730821cb19c](https://github.com/user-attachments/assets/9889809a-06ab-4bae-a858-86bebeff3c54)
# Note
This project is just a basic foundation. Many features should be added in the future and more responsive ui also.🤞

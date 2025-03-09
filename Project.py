import cv2
import cvzone
import math
import time
import pygame
import smtplib
from email.mime.text import MIMEText
from ultralytics import YOLO
from threading import Thread

# Email Configuration
SENDER_EMAIL = "1801003@iot.bdu.ac.bd"
APP_PASSWORD = "your_generated_app_password"  # Use the App Password instead
RECIPIENT_EMAIL = "emonahmed8819@gmail.com"

# Initialize pygame for sound playback
pygame.mixer.init()
fall_sound = pygame.mixer.Sound("fall_detected.mp3")  # Ensure this file exists

# Load video file (Replace with your actual video file path)
cap = cv2.VideoCapture('D:\\WORK FILE\\PYTHON\\Human Fall Detection\\Human Fall Detection\\fall.mp4')  # Replace with your recorded video file

# Load YOLO model
model = YOLO('yolov5nu.pt')  # Ensure this model file exists

# Load class names
classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()

# Tracking previous positions
previous_positions = {}
fall_confirmed = False
fall_start_time = None
sound_played = False
email_sent = False  # Flag to prevent multiple emails

# Fall detection parameters
SPEED_THRESHOLD = 20  
ANGLE_THRESHOLD = 100  
ASPECT_RATIO_THRESHOLD = 2.5  
FALL_CONFIRMATION_FRAMES = 4  
Y_POSITION_THRESHOLD = 100  

fall_frames = {}

# Initialize VideoWriter to save the processed output
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video writing
out = cv2.VideoWriter('fall_detection_output.avi', fourcc, 30, (640, 640))  # Save in 640x640 resolution

def send_email():
    """Send an email alert when a fall is detected."""
    global email_sent
    subject = "Fall Detected Alert!"
    body = "A human fall has been detected by your Raspberry Pi fall detection system."
    
    msg = MIMEText(body)
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        email_sent = True  
    except Exception as e:
        print("Error sending email:", e)

def play_sound():
    """Play the fall detection sound."""
    global sound_played
    if not sound_played and not pygame.mixer.get_busy():
        fall_sound.play()
        sound_played = True  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop when the video ends

    frame = cv2.resize(frame, (640, 640))  # Resize for faster processing
    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = int(box.cls[0])
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            height = y2 - y1
            width = x2 - x1
            aspect_ratio = height / width
            center_y = (y1 + y2) // 2

            person_id = box.id if hasattr(box, 'id') else 0  
            prev_center_y = previous_positions.get(person_id, center_y)
            speed = abs(center_y - prev_center_y)
            previous_positions[person_id] = center_y

            # Body angle
            angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))

            if conf > 80 and class_detect == 'person':
                cvzone.cornerRect(frame, [x1, y1, width, height], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=2)

                # Fall detection conditions
                fall_conditions = (
                    aspect_ratio > ASPECT_RATIO_THRESHOLD and  
                    speed > SPEED_THRESHOLD and  
                    angle > ANGLE_THRESHOLD  
                )

                # Check for significant vertical movement
                if center_y - prev_center_y > Y_POSITION_THRESHOLD:
                    fall_conditions = True

                # Fall confirmation logic
                if fall_conditions:
                    fall_frames[person_id] = fall_frames.get(person_id, 0) + 1

                    if fall_frames[person_id] >= FALL_CONFIRMATION_FRAMES:
                        if not fall_confirmed:
                            fall_confirmed = True
                            fall_start_time = time.time()
                            print("Fall Detected!")

                            # Start sound in a separate thread
                            Thread(target=play_sound).start()

                            if not email_sent:
                                # Send email in a separate thread
                                Thread(target=send_email).start()

                else:
                    fall_frames[person_id] = max(0, fall_frames.get(person_id, 0) - 1)

    # Display fall status
    if fall_confirmed:
        cvzone.putTextRect(frame, 'Fall Detected', [50, 50], thickness=2, scale=2, colorR=(0, 0, 255))
    else:
        cvzone.putTextRect(frame, 'No Fall Detected', [50, 50], thickness=2, scale=2, colorR=(0, 255, 0))

    # Reset fall detection after 5 seconds
    if fall_confirmed and time.time() - fall_start_time > 5:
        fall_confirmed = False
        sound_played = False  
        email_sent = False  

    # Show frame using OpenCV
    cv2.imshow('Fall Detection', frame)

    # Write the frame to output video
    out.write(frame)

    # Delay to control video playback speed (adjust as needed)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()

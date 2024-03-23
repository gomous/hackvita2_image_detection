import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time

def resize_template(template, scale):
    """Resize the template image."""
    width = int(template.shape[1] * scale)
    height = int(template.shape[0] * scale)
    return cv2.resize(template, (width, height))

def detect_template_in_video(video_path, template_path, threshold=0.8, scale_range=(0.5, 2.0), step=0.1, frame_skip=10):
    """Detect the template in a video with frame skipping."""
    # Load the template image
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    # Load the video
    video_capture = cv2.VideoCapture(video_path)
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    
    # Define the scale range for resizing the template
    min_scale, max_scale = scale_range
    
    # Initialize frame counter
    frame_counter = 0
    
    last_entry_time = None
    last_exit_time = None
    detection_duration_threshold = 10  # in seconds
    
    # Iterate over each frame of the video
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Increment frame counter
        frame_counter += 1
        
        # Skip frames if necessary
        if frame_counter % frame_skip != 0:
            continue
        
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Perform template matching at multiple scales
        template_detected = False
        for scale in np.arange(min_scale, max_scale, step):
            resized_template = resize_template(template, scale)
            result = cv2.matchTemplate(gray_frame, resized_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            
            # Draw bounding boxes around matched regions
            for pt in zip(*loc[::-1]):
                cv2.rectangle(frame, pt, (pt[0] + resized_template.shape[1], pt[1] + resized_template.shape[0]), (0, 255, 0), 2)
                template_detected = True
        
        # Display the frame with detected template
        cv2.imshow('Video', frame)
        
        # Check for template detection
        if template_detected:
            # Template is detected in the frame
            if last_entry_time is None:
                # Register entry time if not already registered
                last_entry_time = time.time()
                print(f"Object detected, entry time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_entry_time))}")
            else:
                # Check if the duration since the last detection exceeds the threshold
                current_time = time.time()
                if current_time - last_entry_time >= detection_duration_threshold:
                    # Register exit time and reset entry time
                    if last_exit_time is not None:
                        print(f"Object detected, exit time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_exit_time))}")
                    last_exit_time = current_time
                    last_entry_time = current_time
                    print(f"Object detected, entry time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_entry_time))}")
        else:
            # Template is not detected in the frame
            if last_entry_time is not None:
                # Register exit time if entry time is registered
                last_exit_time = time.time()
                print(f"Object not detected, exit time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_exit_time))}")
                last_entry_time = None
        
        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

def select_template_image():
    global template_path
    template_path = filedialog.askopenfilename()

def select_video_file():
    global video_path
    video_path = filedialog.askopenfilename()

# Create main window
root = tk.Tk()
root.title("Template Matching UI")

# Create template image selection button
template_button = tk.Button(root, text="Select Template Image", command=select_template_image)
template_button.pack()

# Create video file selection button
video_button = tk.Button(root, text="Select Video File", command=select_video_file)
video_button.pack()

# Button to start template matching process
match_button = tk.Button(root, text="Start Template Matching", command=lambda: detect_template_in_video(video_path, template_path, threshold=0.8, scale_range=(0.5, 2.0), step=0.1))
match_button.pack()

root.mainloop()

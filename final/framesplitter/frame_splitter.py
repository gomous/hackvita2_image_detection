import cv2
import tkinter as tk
from tkinter import filedialog

def save_frames(video_path, output_folder):
    capture = cv2.VideoCapture(video_path)
    frame_nr = 0

    while True:
        success, frame = capture.read()

        if success:
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f'{output_folder}/frame_{frame_nr}.jpg', gray_frame)
        else:
            break

        frame_nr += 1

    capture.release()
    print("Frames saved successfully.")

def select_video():
    global video_path
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi")])

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")

def start_process():
    if video_path and output_folder:
        save_frames(video_path, output_folder)
    else:
        print("Please select both a video file and an output folder.")

# Create main window
root = tk.Tk()
root.title("Video to Frames Converter")

# Create button to select video file
video_button = tk.Button(root, text="Select Video", command=select_video)
video_button.pack()

# Create button to select output folder
folder_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
folder_button.pack()

# Create button to start the process
start_button = tk.Button(root, text="Start Process", command=start_process)
start_button.pack()

root.mainloop()

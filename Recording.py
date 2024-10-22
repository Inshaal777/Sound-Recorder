import tkinter as tk
import time
import pyautogui
import threading
import numpy as np
import cv2
from tkinter import messagebox

class ScreenRecording:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.time_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.time_label.pack(pady=10)

        self.recording = False
        self.start_time = 0
        self.video_writer = None

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.start_time = time.time()
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.recording_thread.join()
        self.video_writer.release()

        elapsed_time = time.time() - self.start_time
        print(f"Recording Duration: {elapsed_time:.2f} seconds")
        self.time_label.config(text="Recording stopped")

        self.save_video()

    def record_screen(self):
        screen_width, screen_height = pyautogui.size()
        self.video_writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (screen_width, screen_height))

        while self.recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
            self.video_writer.write(frame)

            elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"Recording time: {elapsed_time:.2f} seconds")
            self.time_label.update()

    def save_video(self):
        # Rename the recorded file with a timestamp
        current_time = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"recorded_{current_time}.avi"
        try:
            import os
            os.rename("output.avi", file_name)
            print(f"Video saved as: {file_name}")
            messagebox.showinfo("Video Saved", f"Video saved as: {file_name}")
        except Exception as e:
            print(f"Failed to save the video: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecording(root)
    root.mainloop()

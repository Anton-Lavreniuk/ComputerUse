import io
from time import sleep

import customtkinter as ctk
import pyautogui
from PIL import Image
import os
from dotenv import load_dotenv

from .models import Model

load_dotenv()

from .processor import Processor


class GUI:
    def __init__(self, model):
        # Set appearance mode to dark
        self.current_screenshot = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("GUI")
        self.root.geometry("800x600")
        # self.root.attributes("-fullscreen", "True")
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create left frame for task input and submission
        left_frame = ctk.CTkFrame(self.root)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(2, weight=1)  # Make text display expandable
        
        # Task input
        self.task_label = ctk.CTkLabel(left_frame, text="Enter Task:")
        self.task_label.grid(row=0, column=0, pady=5, sticky="w")
        
        self.task_entry = ctk.CTkTextbox(left_frame, height=100)
        self.task_entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        
        # Submit button
        self.submit_button = ctk.CTkButton(
            left_frame, 
            text="Submit Task", 
            command=self.submit_task
        )
        self.submit_button.grid(row=2, column=0, pady=10)
        
        # Text display
        self.text_display = ctk.CTkTextbox(left_frame)
        self.text_display.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
        
        # Create right frame for image display
        right_frame = ctk.CTkFrame(self.root)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)
        
        # Image display label
        self.image_label = ctk.CTkLabel(right_frame, text="")
        self.image_label.grid(row=0, column=0, sticky="nsew")
        
        # Bind resize event
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Set placeholder image
        self.current_image_path = ""
        self.update_image()
        self.processor = Processor(model=model)
        
    def on_window_resize(self, event):
        # Update image size when window is resized
        self.update_image()

    def update_image(self):
        screenshot = pyautogui.screenshot()

        frame_width = self.root.winfo_width() // 2 - 40
        frame_height = self.root.winfo_height() - 40

        original_width, original_height = screenshot.size
        aspect_ratio = original_width / original_height

        if frame_width / frame_height > aspect_ratio:
            new_height = frame_height
            new_width = int(frame_height * aspect_ratio)
        else:
            new_width = frame_width
            new_height = int(frame_width / aspect_ratio)

        resized_image = screenshot.resize((new_width, new_height))
        ctk_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(new_width, new_height))

        self.image_label.configure(image=ctk_image)
        self.image_label._image = ctk_image
        self.current_screenshot = screenshot

    def submit_task(self):
        task = self.task_entry.get("1.0", "end-1c")
        self.text_display.insert("end", f"Submitted Task: {task}\n")
        self.text_display.see("end")
        sleep(1)

        buffer = io.BytesIO()
        self.current_screenshot.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        for progress in self.processor.process_task(task, image_bytes, None):
            self.text_display.insert("end", f"Response: {progress}\n")
        
    def run(self):
        def update():
            self.root.update_idletasks()
            self.root.after(100, update)
        self.root.after(100, update)
        self.root.mainloop()

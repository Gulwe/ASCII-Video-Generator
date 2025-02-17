import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageTk
from moviepy.editor import ImageSequenceClip
import threading
import concurrent.futures
import logging

# Extended set of ASCII characters (from very light to very "dense")
ASCII_CHARS = " .:-=+*#%@"

# Precompute lookup table for each possible grayscale value (0-255)
LUT = [ASCII_CHARS[p * (len(ASCII_CHARS) - 1) // 255] for p in range(256)]

# Default font
FONT = ImageFont.load_default()

# Setup logging
logging.basicConfig(filename='ascii_art_generator.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    """Adjusts the brightness and contrast of an image."""
    beta = brightness
    alpha = contrast / 127 + 1  # Contrast scale (1.0 means no change)
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def adjust_image(gray, gamma=0.4):
    """Gamma correction and histogram equalization for a grayscale image."""
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_corrected = cv2.LUT(gray, table)
    equalized = cv2.equalizeHist(gamma_corrected)
    return equalized

def frame_to_ascii_text(frame, new_width=300, gamma=0.4, brightness=0, contrast=0, ascii_table=LUT):
    """Converts a single frame to ASCII text."""
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    frame = cv2.resize(frame, (new_width, new_height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Adjust brightness and contrast
    gray = adjust_brightness_contrast(gray, brightness, contrast)

    # Apply gamma correction and histogram equalization
    gray = adjust_image(gray, gamma)

    ascii_str = "".join(ascii_table[p] for p in gray.flatten())
    ascii_image = "\n".join(ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width))
    return ascii_image

def ascii_text_to_image(text, font=FONT, text_color=(0, 255, 0), bg_color=(0, 0, 0)):
    """Renders ASCII text to an image using the specified font and colors."""
    lines = text.split("\n")
    max_width = max(font.getsize(line)[0] for line in lines)
    line_height = font.getsize("A")[1]
    total_height = line_height * len(lines)

    image = Image.new("RGB", (max_width, total_height), bg_color)
    draw = ImageDraw.Draw(image)
    y = 0
    for line in lines:
        draw.text((0, y), line, fill=text_color, font=font)
        y += line_height
    return np.array(image)

def process_frame(frame, new_width, gamma, brightness, contrast, ascii_table, font, text_color):
    """Process a single frame to ASCII art and render as an image."""
    ascii_text = frame_to_ascii_text(frame, new_width, gamma, brightness, contrast, ascii_table)
    return ascii_text_to_image(ascii_text, font=font, text_color=text_color)

def frame_generator_sequential(video_path, new_width=300, frame_skip=1, gamma=0.4, brightness=0, contrast=0, r=0, g=255, b=0, status_callback=None):
    """
    Generator that reads frames from a video, converts them to ASCII,
    and renders them as images sequentially.
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue
        if status_callback:
            status_callback(f"Processing frame {frame_count}/{total_frames}")
        logging.debug(f"Processing frame {frame_count}")
        yield process_frame(frame, new_width, gamma, brightness, contrast, LUT, FONT, (r, g, b))
        frame_count += 1

    cap.release()

import gc
import tracemalloc

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Video Generator")
        self.video_path = None
        self.file_name = ""
        self.font_path = None

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        settings_frame = tk.LabelFrame(self.root, text="Settings")
        settings_frame.pack(pady=10, padx=10, fill="x")

        # File selection and font loading
        file_font_frame = tk.Frame(settings_frame)
        file_font_frame.pack(fill="x")

        self.btn_select = tk.Button(file_font_frame, text="Select Video File", command=self.select_file)
        self.btn_select.pack(side="left", padx=5)

        self.lbl_file = tk.Label(file_font_frame, text="No file selected")
        self.lbl_file.pack(side="left", padx=5)

        self.btn_font = tk.Button(file_font_frame, text="Load Custom Font", command=self.select_font)
        self.btn_font.pack(side="left", padx=5)

        # Font size and output size
        size_frame = tk.Frame(settings_frame)
        size_frame.pack(fill="x", pady=5)

        self.font_size_slider = tk.Scale(size_frame, from_=4, to=20, resolution=1, orient=tk.HORIZONTAL,
                                          label="Font Size", command=lambda val: self.update_preview())
        self.font_size_slider.set(6)
        self.font_size_slider.pack(side="left", padx=5)

        self.size_slider = tk.Scale(size_frame, from_=100, to=1000, resolution=10, orient=tk.HORIZONTAL,
                                     label="Output Size", command=lambda val: self.update_preview())
        self.size_slider.set(300)
        self.size_slider.pack(side="left", padx=5)
        
        # ASCII characters settings
        ascii_frame = tk.LabelFrame(size_frame, text="ASCII Characters")
        ascii_frame.pack(side="left", padx=5)
        
        self.ascii_chars = tk.StringVar(value=ASCII_CHARS)
        self.ascii_entry = tk.Entry(ascii_frame, textvariable=self.ascii_chars)
        self.ascii_entry.pack(padx=5,side="left", pady=9)

        # Graphics settings
        graphics_frame = tk.LabelFrame(settings_frame, text="Graphics Settings")
        graphics_frame.pack(fill="x", pady=5)

        self.gamma_slider = tk.Scale(graphics_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                     label="Gamma", command=lambda val: self.update_preview())
        self.gamma_slider.set(0.4)
        self.gamma_slider.pack(side="left", padx=5)

        self.contrast_slider = tk.Scale(graphics_frame, from_=0.0, to=127.0, resolution=0.1, orient=tk.HORIZONTAL,
                                     label="Contrast", command=lambda val: self.update_preview())
        self.contrast_slider.set(0.0)
        self.contrast_slider.pack(side="left", padx=5)

        self.brightness_slider = tk.Scale(graphics_frame, from_=0.0, to=127.0, resolution=0.1, orient=tk.HORIZONTAL,
                                     label="Brightness", command=lambda val: self.update_preview())
        self.brightness_slider.set(0.0)
        self.brightness_slider.pack(side="left", padx=5)

        # RGB settings
        rgb_frame = tk.LabelFrame(settings_frame, text="RGB Colors")
        rgb_frame.pack(fill="x", pady=5)

        self.r_slider = tk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="R", command=lambda val: self.update_preview())
        self.r_slider.pack(side="left", padx=5)

        self.g_slider = tk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="G", command=lambda val: self.update_preview())
        self.g_slider.set(255)
        self.g_slider.pack(side="left", padx=5)

        self.b_slider = tk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="B", command=lambda val: self.update_preview())
        self.b_slider.pack(side="left", padx=5)

        # Video settings
        video_frame = tk.LabelFrame(settings_frame, text="Video Settings")
        video_frame.pack(fill="x", pady=5)
        
        self.frame_skip_slider = tk.Scale(video_frame, from_=1, to=10, resolution=1, orient=tk.HORIZONTAL,
                                          label="Frame Skip", command=lambda val: self.update_preview())
        self.frame_skip_slider.set(1)
        self.frame_skip_slider.pack(side="left", padx=5)

        self.fps_slider = tk.Scale(video_frame, from_=1, to=60, resolution=1, orient=tk.HORIZONTAL,
                                   label="Output FPS", command=lambda val: self.update_preview())
        self.fps_slider.set(15)
        self.fps_slider.pack(side="left", padx=5)

        self.match_fps_var = tk.BooleanVar()
        self.match_fps_check = tk.Checkbutton(video_frame, text="Match Original FPS", variable=self.match_fps_var, command=self.update_fps_option)
        self.match_fps_check.pack(side="left", padx=5)

        # Preview section
        preview_frame = tk.LabelFrame(self.root, text="Preview", width=600, height=400)
        preview_frame.pack(padx=10, pady=10, fill="both", expand=True)
        preview_frame.pack_propagate(False)
        self.preview_label = tk.Label(preview_frame)
        self.preview_label.pack(padx=5, pady=5)
        self.size_label = tk.Label(self.root, text="")
        self.size_label.pack(pady=5)

        self.btn_start = tk.Button(self.root, text="Convert", command=self.start_processing, state=tk.DISABLED)
        self.btn_start.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Waiting", fg="blue")
        self.status_label.pack(pady=5)

    def select_file(self):
        """Select a video file and update the UI."""
        path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.gif"), ("All Files", "*.*")]
        )
        if path:
            self.video_path = path
            self.lbl_file.config(text=os.path.basename(path))
            self.file_name = os.path.basename(path)
            self.btn_start.config(state=tk.NORMAL)
            self.update_preview()

    def select_font(self):
        """Select a custom font file."""
        path = filedialog.askopenfilename(
            title="Select Font File",
            filetypes=[("Font Files", "*.ttf *.otf"), ("All Files", "*.*")]
        )
        if path:
            self.font_path = path
            try:
                global FONT
                font_size = int(self.font_size_slider.get())
                FONT = ImageFont.truetype(self.font_path, font_size)
                font_name = os.path.basename(path)
                self.btn_font.config(text=f"Font: {font_name}")
                messagebox.showinfo("Success", "Custom font loaded successfully!")
            except IOError:
                messagebox.showerror("Error", "Failed to load the custom font.")

    def update_status(self, message):
        """Update the status label with a new message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def update_preview(self, event=None):
        """Update the preview image based on the current settings."""
        if not self.video_path:
            return
        try:
            cap = cv2.VideoCapture(self.video_path)
            ret, frame = cap.read()
            cap.release()
            if ret:
                size_val = int(self.size_slider.get())
                gamma_val = float(self.gamma_slider.get())
                brightness_val = float(self.brightness_slider.get())
                contrast_val = float(self.contrast_slider.get())
                r_val = int(self.r_slider.get())
                g_val = int(self.g_slider.get())
                b_val = int(self.b_slider.get())
                ascii_chars = self.ascii_chars.get()
                ascii_table = [ascii_chars[p * (len(ascii_chars) - 1) // 255] for p in range(256)]
                ascii_text = frame_to_ascii_text(frame, new_width=size_val, gamma=gamma_val, brightness=brightness_val, contrast=contrast_val, ascii_table=ascii_table)
                preview_img_arr = ascii_text_to_image(ascii_text, font=FONT, text_color=(r_val, g_val, b_val))
                preview_img = Image.fromarray(preview_img_arr)
                width, height = preview_img.size
                self.size_label.config(text="Output dimensions: " + str(preview_img.size))
                preview_img.thumbnail((int(width / 2), int(height / 2)), Image.LANCZOS)
                preview_photo = ImageTk.PhotoImage(preview_img)
                self.preview_label.config(image=preview_photo)
                self.preview_label.image = preview_photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview:\n{e}")
            logging.error(f"Preview generation error: {e}")

    def update_fps_option(self):
        """Update the FPS slider based on the match original FPS option."""
        if self.match_fps_var.get():
            self.fps_slider.config(state=tk.DISABLED)
        else:
            self.fps_slider.config(state=tk.NORMAL)

    def start_processing(self):
        """Start processing the video in a separate thread."""
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video file first!")
            return
        self.btn_select.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        threading.Thread(target=self.process_video, daemon=True).start()

    def process_video(self):
        """Process the video and generate the ASCII art video."""
        try:
            tracemalloc.start()  # Start tracking memory allocations

            cap_temp = cv2.VideoCapture(self.video_path)
            original_fps = cap_temp.get(cv2.CAP_PROP_FPS)
            cap_temp.release()
            adjusted_fps = int(self.fps_slider.get()) if not self.match_fps_var.get() else int(original_fps)

            self.update_status("Generating ASCII frames...")
            gamma_val = float(self.gamma_slider.get())
            size_val = int(self.size_slider.get())
            brightness_val = float(self.brightness_slider.get())
            contrast_val = float(self.contrast_slider.get())
            r_val = int(self.r_slider.get())
            g_val = int(self.g_slider.get())
            b_val = int(self.b_slider.get())
            frame_skip = int(self.frame_skip_slider.get())
            ascii_chars = self.ascii_chars.get()
            ascii_table = [ascii_chars[p * (len(ascii_chars) - 1) // 255] for p in range(256)]

            frames = []
            for frame in frame_generator_sequential(self.video_path, new_width=size_val, frame_skip=frame_skip, gamma=gamma_val, brightness=brightness_val, contrast=contrast_val,
                                                     r=r_val, g=g_val, b=b_val, status_callback=self.update_status):
                frames.append(frame)

            self.update_status("Combining frames into video...")

            clip = ImageSequenceClip(frames, fps=adjusted_fps)
            output_path = os.path.join(os.path.dirname(self.video_path), self.file_name + "_ASCII.mp4")
            clip.write_videofile(output_path, logger=None)
            self.update_status("Done! Video saved as: " + output_path)
            messagebox.showinfo("Success", "ASCII video saved:\n" + output_path)

            # Explicitly delete large objects and trigger garbage collection
            del frames
            del clip
            gc.collect()

            # Stop tracking memory allocations and print the peak memory usage
            current, peak = tracemalloc.get_traced_memory()
            logging.info(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB.")
            tracemalloc.stop()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Processing error: {e}")
            self.update_status("An error occurred.")
        finally:
            self.btn_select.config(state=tk.NORMAL)
            self.btn_start.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

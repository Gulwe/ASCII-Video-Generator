# ASCII Video Generator

ASCII Video Generator is a Python application that converts a video/animation file into an ASCII art video. The application uses OpenCV for video frame extraction, processes each frame to generate ASCII art, and combines these frames into a new video using MoviePy. The graphical user interface (GUI) is built with Tkinter, allowing users to adjust various settings and preview the conversion in real-time.

## Features

- **Video to ASCII Conversion:**  
  Convert each video frame to ASCII art with customizable parameters.

- **Customizable Settings:**  
  Adjust output dimensions, font size, gamma, brightness, contrast, and RGB text color using intuitive sliders.

- **Custom Font Support:**  
  Load a custom font file for rendering the ASCII art.

- **Real-Time Preview:**  
  Preview the ASCII conversion of the first frame before processing the entire video.

- **Output Video Generation:**  
  Combines the processed frames into a final ASCII art video.

- **Logging & Error Handling:**  
  The application logs processing steps and errors to `ascii_art_generator.log` for easier debugging.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Gulwe/ASCII-Video-Generator
    cd ascii-video-generator
    ```

2. **Install the required dependencies:**
    ```bash
    pip install opencv-python numpy Pillow moviepy
    ```

3. **Run the application:**
    ```bash
    python ascii_video_generator.py
    ```

## Usage

1. **Select a Video File:**  
   Click the "Select Video File" button to choose the video you want to convert.

2. **Load a Custom Font (Optional):**  
   Use the "Load Custom Font" button to load your preferred TTF or OTF font.

3. **Adjust Settings:**  
   - **Output Size:** Use the "Output Size" slider to set the width of the ASCII output.
   - **Font Size:** Adjust the font size for ASCII rendering.
   - **Gamma, Brightness, Contrast:** Fine-tune the visual appearance of the ASCII art.
   - **RGB Colors:** Set the text color for the ASCII characters.
   - **Frame Skip & FPS:** Control the conversion speed and output video frame rate.

4. **Preview:**  
   A preview of the first converted frame is displayed in the "Preview" section.

5. **Convert:**  
   Click the "Convert" button to start processing the video. The final ASCII art video will be saved in the same directory as the source video with `_ASCII.mp4` appended to the filename.

## Code Structure

- **Main Modules:**  
  - `frame_to_ascii_text()`: Converts video frames to ASCII text.
  - `ascii_text_to_image()`: Renders ASCII text into an image.
  - `frame_generator_sequential()`: Generator function for processing video frames sequentially.
  - `App` class: Handles the Tkinter GUI, user interactions, and overall video processing workflow.

- **Logging:**  
  All processing steps and errors are logged in `ascii_art_generator.log`.

## Roadmap / Further development

- **Improved optimisation:** Improved video processing performance and memory management.
- **GIF saving capability:** Extension of functionality to include export to GIF format.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements and new features.

## License

This project is licensed under the MIT License.

---

AI Image Generator using Stable Diffusion
This is a simple GUI-based application that generates images from text prompts using the Stable Diffusion model. The application is built using Tkinter for the graphical interface and diffusers for Stable Diffusion model integration, with support for GPU acceleration (via CUDA).

Features
 Text-to-Image Generation: Enter a text prompt to generate images using the Stable Diffusion model.
 Dark Theme: A dark-themed interface for a visually comfortable experience.
 Save Images: Save the generated images in PNG format.
 Loading Animation: Displays a loading animation while the image is being generated.
 GPU Support: Leverages GPU acceleration if available for faster image generation.
Screenshots
<!-- Include screenshot after adding it to assets -->

Prerequisites
 Python 3.8+
 Torch with CUDA support (for GPU acceleration)
 diffusers library for loading the Stable Diffusion model
 Pillow for image manipulation
 Tkinter for GUI
Installation
 Clone the repository:


git clone https://github.com/your-username/ai-image-generator.git
     cd ai-image-generator
Set up a virtual environment (optional but recommended):


     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required dependencies:


     pip install -r requirements.txt
Install PyTorch and diffusers with GPU support:

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install diffusers[torch]
Usage
Run the application:


    python app.py
Enter a text prompt in the input field and click Generate Image.

The generated image will be displayed in the window. You can then save the image by clicking Save Image.

Files
   app.py: The main application file containing the GUI and logic for generating and saving images.
   requirements.txt: Lists the Python dependencies needed to run the project.
   assets/: Folder to store images like screenshots for the README.
Dependencies

The project depends on the following Python libraries:

torch: PyTorch for running the Stable Diffusion model with GPU support.
diffusers: To load and run the Stable Diffusion model.
Pillow: For image handling in Python.
Tkinter: For building the graphical interface.

Notes
Make sure to have CUDA installed and properly set up if you want to run the model on the GPU.
The application will automatically use CPU if CUDA is unavailable, though the generation might be slower.


License

This project is licensed under the MIT License. See the LICENSE file for more information.

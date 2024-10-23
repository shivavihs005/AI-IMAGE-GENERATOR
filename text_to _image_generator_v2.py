import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import torch
from diffusers import StableDiffusionPipeline
import io
import threading
import time

# Initialize the main window
root = tk.Tk()
root.title("Text-to-Image Generator")
root.geometry("800x600")  # Width x Height

# Set dark theme colors
bg_color = "#2E2E2E"  # Dark gray background
fg_color = "#FFFFFF"  # White text
button_color = "#3E3E3E"  # Slightly lighter gray for buttons
highlight_color = "#009688"  # Accent color (teal)

# Configure style
style = ttk.Style()
style.theme_use("default")

# Configure ttk widgets (buttons, labels, etc.)
style.configure("TButton", background=button_color, foreground=fg_color, font=("Helvetica", 12), padding=6)
style.map("TButton", background=[('active', highlight_color)])
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Helvetica", 12))
style.configure("TText", background=bg_color, foreground=fg_color)

# Set background color for the main window
root.configure(bg=bg_color)

# Initialize the model and ensure it runs on the GPU if available
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")  # Debugging log

try:
    # Add print statement for debug
    print("Loading the model...")
    
    # Loading the model
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        low_cpu_mem_usage=True
    )
    
    # Move model to device
    pipe = pipe.to(device)

    if device == "cuda":
        pipe.enable_attention_slicing()  # Efficient usage of GPU memory
    
    print(f"Model loaded successfully on {device}.")
except Exception as e:
    messagebox.showerror("Error", f"Failed to load the model: {e}")
    print(f"Error loading model: {e}")  # Debugging log
    root.destroy()

# Label for the description
label_prompt = ttk.Label(root, text="Enter description:")
label_prompt.grid(column=0, row=0, padx=10, pady=10, sticky=tk.E)

# Text box for the description
entry_prompt = tk.Text(root, height=4, width=50, wrap='word', bg=bg_color, fg=fg_color, insertbackground=fg_color)
entry_prompt.grid(column=1, row=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

def animate_loading():
    """This function shows rotating dots while waiting for the image to be generated."""
    dots = ""
    while getattr(threading.current_thread(), "keep_running", True):
        dots = dots + "." if len(dots) < 3 else ""
        status_label.config(text=f"Generating image{dots} Please wait.")
        time.sleep(0.5)

def generate_image_thread(prompt):
    """ This function runs in a separate thread to prevent freezing """
    try:
        # Debugging log
        print(f"Generating image for prompt: {prompt}")
        
        # Generate the image on GPU (or CPU if GPU is unavailable)
        with torch.autocast(device):
            image = pipe(prompt).images[0]

        # Resize image to fit the display area
        image = image.resize((512, 512), Image.LANCZOS)

        # Convert the image to a format Tkinter can use
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img = Image.open(io.BytesIO(img_byte_arr))
        img_tk = ImageTk.PhotoImage(img)

        # Update the image display on the main thread
        label_image.config(image=img_tk)
        label_image.image = img_tk  # Keep a reference

        # Store the generated image for saving
        root.generated_image = image

        # Update the status label
        status_label.config(text="Image generated successfully.")
        print("Image generated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate image: {e}")
        print(f"Error generating image: {e}")  # Debugging log
        status_label.config(text="Error occurred.")
    finally:
        # Stop the loading animation
        threading.current_thread().keep_running = False
        button_generate.config(state='normal')

def generate_image():
    prompt = entry_prompt.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("Input Required", "Please enter a description.")
        return

    # Disable the button to prevent multiple clicks
    button_generate.config(state='disabled')

    # Start a new thread to show the loading animation
    loading_thread = threading.Thread(target=animate_loading)
    loading_thread.keep_running = True
    loading_thread.start()

    # Start a new thread to generate the image
    image_thread = threading.Thread(target=generate_image_thread, args=(prompt,))
    image_thread.start()

# Save Image function
def save_image():
    if not hasattr(root, 'generated_image'):
        messagebox.showwarning("No Image", "Please generate an image first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if file_path:
        try:
            root.generated_image.save(file_path)
            messagebox.showinfo("Saved", f"Image saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

# Generate Button
button_generate = ttk.Button(root, text="Generate Image", command=generate_image)
button_generate.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

# Save Button - moved next to the Generate button
button_save = ttk.Button(root, text="Save Image", command=save_image)
button_save.grid(column=2, row=1, padx=10, pady=10, sticky=tk.W)

# Label to display the image
label_image = ttk.Label(root)
label_image.grid(column=0, row=2, columnspan=3, padx=10, pady=10)

# Status Label
status_label = ttk.Label(root, text="Enter a description and generate an image.")
status_label.grid(column=0, row=4, columnspan=3, padx=10, pady=10, sticky=tk.W)

# Set status label colors
status_label.config(background=bg_color, foreground=fg_color)

# Start the GUI event loop
root.mainloop()

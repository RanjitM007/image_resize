import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import os
import tempfile

def open_file():
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Select Image File",
        filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*"))
    )
    if filepath:
        entry_path.delete(0, tk.END)
        entry_path.insert(tk.END, filepath)

def resize_image():
    filepath = entry_path.get()
    resize_option = resize_var.get()
    size_limit = entry_size.get()

    try:
        img = Image.open(filepath)
        resized_img = img.copy()

        if resize_option == "width_height":
            width = entry_width.get()
            height = entry_height.get()
            if width.isnumeric() and height.isnumeric():
                resized_img = resized_img.resize((int(width), int(height)))
            else:
                raise ValueError("Invalid width or height value.")
        elif resize_option == "file_size":
            target_size = int(size_limit) * 1024
            quality = 95  # Adjust the quality value for desired file size

            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_filepath = temp_file.name
                resized_img.save(temp_filepath, format='JPEG', quality=quality)
            
            temp_file_size = os.path.getsize(temp_filepath)
            while temp_file_size > target_size:
                quality -= 5  # Reduce quality if size is still greater than the target
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    temp_filepath = temp_file.name
                    resized_img.save(temp_filepath, format='JPEG', quality=quality)
                    temp_file_size = os.path.getsize(temp_filepath)

            save_filepath = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=(("JPEG", "*.jpg"), ("PNG", "*.png"))
            )
            if save_filepath:
                os.replace(temp_filepath, save_filepath)
                status_label.config(text="Image resized and saved successfully!")

        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)  # Delete the temporary file
        
    except Exception as e:
        if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        status_label.config(text="Error: " + str(e))

# Create a new Tkinter window
window = tk.Tk()
window.title("Image Resize App MS Computer")

# Configure window background color and font
window.configure(bg="#F0F0F0")
window.option_add("*Font", "Arial 10")
window.option_add("*Label.Font", "Arial 10 bold")

# Set the window title font to red and bold
#window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='icon.png'))
window.tk.call('wm', 'title', window._w, "Image Resize App MS Computer")
window.tk.call('wm', 'iconname', window._w, "Image Resize App MS Computer")

# Create and place widgets
label_path = tk.Label(window, text="Image Path:", bg="#F0F0F0")
label_path.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
entry_path = tk.Entry(window, width=50)
entry_path.grid(row=0, column=1, columnspan=2,padx=10, pady=10)
button_browse = tk.Button(window, text="Browse", command=open_file, bg="#4C9BF5", fg="white")
button_browse.grid(row=0, column=3, padx=10, pady=10)

label_resize = tk.Label(window, text="Resize Option:", bg="#F0F0F0")
label_resize.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

resize_var = tk.StringVar()
resize_var.set("width_height")

radio_width_height = tk.Radiobutton(
    window, text="Width & Height",
    variable=resize_var, value="width_height", bg="#F0F0F0"
)
radio_width_height.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

radio_file_size = tk.Radiobutton(
    window, text="File Size (KB)",
    variable=resize_var, value="file_size", bg="#F0F0F0"
)
radio_file_size.grid(row=1, column=2, sticky=tk.W, padx=10, pady=10)

label_width = tk.Label(window, text="Width:", bg="#F0F0F0")
label_width.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
entry_width = tk.Entry(window, width=10)
entry_width.grid(row=2, column=1, padx=10, pady=10)

label_height = tk.Label(window, text="Height:", bg="#F0F0F0")
label_height.grid(row=2, column=2, sticky=tk.W, padx=10, pady=10)
entry_height = tk.Entry(window, width=10)
entry_height.grid(row=2, column=3, padx=10, pady=10)

label_size = tk.Label(window, text="Size (KB):", bg="#F0F0F0")
label_size.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
entry_size = tk.Entry(window, width=10)
entry_size.grid(row=3, column=1, padx=10, pady=10)

button_resize = tk.Button(window, text="Resize", command=resize_image, bg="#4C9BF5", fg="white")
button_resize.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

status_label = tk.Label(window, text="", bg="#F0F0F0", fg="#FF0000", font=("Arial", 12, "bold"))
status_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Create a progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, variable=progress_var, style="Green.Horizontal.TProgressbar", length=300, mode='determinate')
progress_bar.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# Define a custom style for the progress bar
style = ttk.Style()
style.theme_use('default')
style.configure("Green.Horizontal.TProgressbar", troughcolor="#F0F0F0", background="#00FF00")

# Start the Tkinter event loop
window.mainloop()

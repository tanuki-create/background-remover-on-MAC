from rembg import remove
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading

root = tk.Tk()

def set_default_in():
    with open("default_in.txt", "w") as file:
        file.write(named_directory_in.get())

def set_default_out():
    with open("default_out.txt", "w") as file:
        file.write(named_directory_out.get())

def get_path_in():
    named_directory_in.set(filedialog.askdirectory())

def get_path_out():
    named_directory_out.set(filedialog.askdirectory())

def run_batch_removal_tool():
    pic_list = os.listdir(named_directory_in.get())
    save_number = 0

    # Loop over all Images
    for pic in pic_list:
        save_number += 1
        input_path = os.path.join(named_directory_in.get(), pic)
        
        # Store path of the output image in the variable output_path
        output_path = os.path.join(named_directory_out.get(), f'no_bg{save_number}.png')

        # Check if image exists
        if os.path.exists(output_path):
            continue
        
        # Processing the image
        input_image = Image.open(input_path)

        # Removing the background from the given Image
        output = remove(input_image)

        # Saving the image in the given path
        output.save(output_path)

# Load default paths if the files exist
if os.path.exists("default_in.txt"):
    with open("default_in.txt", "r") as file:
        saved_default_in = file.read()
else:
    saved_default_in = ""

if os.path.exists("default_out.txt"):
    with open("default_out.txt", "r") as file:
        saved_default_out = file.read()
else:
    saved_default_out = ""

named_directory_in = tk.StringVar(root, saved_default_in)
named_directory_out = tk.StringVar(root, saved_default_out)

root.geometry("640x250")
root.title("UNCHA - Batch Background Removal Tool")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# GUI Title
ttk.Label(root, text="Uncha - Batch Background Removal Tool", padding=(30, 30)).grid(row=0, column=1)

# File In Button and Info Label
choose_path_in_button = ttk.Button(root, text="Choose Input Path", command=get_path_in).grid(row=1, column=0, sticky="EW")
ttk.Label(root, textvariable=named_directory_in, relief="sunken").grid(row=1, column=1, sticky="EW")
set_default_out_button = ttk.Button(root, text="Set as Default", command=set_default_in).grid(row=1, column=2)

# File Out Button and Info Label
choose_path_out_button = ttk.Button(root, text="Choose Output Path", command=get_path_out).grid(row=2, column=0, sticky="EW")
ttk.Label(root, textvariable=named_directory_out, relief="sunken").grid(row=2, column=1, sticky="EW")
set_default_out_button = ttk.Button(root, text="Set as Default", command=set_default_out).grid(row=2, column=2)

# Run Tool Button
def start_thread():
    threading.Thread(target=run_batch_removal_tool).start()

run_batch_removal_tool_button = ttk.Button(
    root,
    text="Start Background Removal Tool",
    command=start_thread
).grid(row=3, column=1, pady=10)

# Quit GUI and process Button
quit_button = ttk.Button(root, text="Quit", command=root.destroy).grid(row=4, column=1)

root.mainloop()
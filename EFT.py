import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from PIL import Image, ImageTk

filename = "materials.json"

# Load the materials from the file, or create a new dictionary if the file doesn't exist
try:
    with open(filename, "r") as file:
        materials = json.load(file)
except FileNotFoundError:
    materials = {
        '42nd': {'quantity': 1},

    }

# Initialize the GUI
root = tk.Tk()
root.title("Material Tracker")

# Define a function to update the materials
def update_material():
    material = material_entry.get()
    quantity = int(quantity_entry.get())
    materials[material]['quantity'] -= quantity
    with open(filename, "w") as file:
        json.dump(materials, file)
    filtered_materials()

# Define a function to filter the materials
def filtered_materials():
    global filtered_frame  # Declare filtered_frame as a global variable
    material_type = material_type_var.get()
    filtered_materials = [material for material in materials]
    filtered_frame.destroy()
    filtered_frame = tk.Frame(canvas)
    filtered_frame.pack(fill="both", expand=True)
    canvas.create_window((0, 0), window=filtered_frame, anchor="nw")
    
    # set the attribute for the variable 
    item_a = tk.Frame(filtered_frame, height=50)
    item_a.pack(fill="x")
    label_a = tk.Label(item_a, text="Icon",width = 7)
    label_a.pack(side="left")
    name_label_a = tk.Label(item_a, text="Material", width=20)
    name_label_a.pack(side="left")
    quantity_label_a = tk.Label(item_a, text="Quantity", width=10)
    quantity_label_a.pack(side="right")

    for material in filtered_materials:
        
        image = Image.open(f"item_image/{material}.png")
        image = image.resize((50, 50))
        
        photo = ImageTk.PhotoImage(image)

        # Create a custom listbox item with the image and material name and quantity
        item = tk.Frame(filtered_frame, height=50)
        item.pack(fill="x")
        item.photo = photo  

        # Store the photo as an attribute of the item to prevent it from being garbage collected
        label = tk.Label(item, image=photo)
        label.pack(side="left")

        name_label = tk.Label(item, text=material, width=20)
        name_label.pack(side="left")

        quantity_label = tk.Label(item, text=f"{materials[material]['quantity']}", width=10)
        quantity_label.pack(side="right")
        


# Create a frame for the materials list and filter
list_frame = ttk.Frame(root, padding=10)
list_frame.pack(side="left", fill="both", expand=True)

# Create a scrollbar and canvas for the filtered materials
scrollbar = ttk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")
canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set, height=100)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.config(command=canvas.yview)


# Create a frame to hold the filtered materials
filtered_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=filtered_frame, anchor="nw")

# Define a function to update the canvas scroll region
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the function to the filtered frame
filtered_frame.bind("<Configure>", update_scroll_region)

# Create a frame for the material entry and filter controls
control_frame = ttk.Frame(root, padding=10)
control_frame.pack(side="right", fill="both")

# Create a label and entry for the material to update
material_label = ttk.Label(control_frame, text="Material:")
material_label.pack()
material_entry = ttk.Entry(control_frame)
material_entry.pack()

# Create a label and entry for the quantity to subtract
quantity_label = ttk.Label(control_frame, text="You have how many:")
quantity_label.pack()
quantity_entry = ttk.Entry(control_frame)
quantity_entry.pack()

# Create a button to update the materials
update_button = ttk.Button(control_frame, text="Update", command=update_material)
update_button.pack(pady=10)

# Create a label and dropdown for the material type filter
material_type_var = tk.StringVar()
material_type_var.set("quest")

# Filter the materials initially
filtered_materials()

canvas.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Start the main event loop
root.mainloop()

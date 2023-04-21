import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

filename = "materials.json"

# Load the materials from the file, or create a new dictionary if the file doesn't exist
try:
    with open(filename, "r") as file:
        materials = json.load(file)
except FileNotFoundError:
    materials = {
        '42nd': {'quantity': 1, 'type': 'quest'},
        'Apollo': {'quantity': 0, 'type': 'quest'},
        'Aramid': {'quantity': 5, 'type': 'quest'},
        'Book': {'quantity': 1, 'type': 'quest'},
        'BEAR Buddy': {'quantity': 1, 'type': 'quest'},
        'Buckwheat':{'quantity': 0, 'type': 'quest'},
        'DrLupos':{'quantity': 1, 'type': 'quest'}
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
    filtered_materials = [material for material in materials if materials[material]['type'] == material_type]
    filtered_frame.destroy()
    filtered_frame = tk.Frame(canvas)
    filtered_frame.pack(fill="both", expand=True)
    canvas.create_window((0, 0), window=filtered_frame, anchor="nw")
    
    for material in filtered_materials:
        image = Image.open(f"{material}.png")
        image = image.resize((50, 50))
        photo = ImageTk.PhotoImage(image)
        
        # Create a custom listbox item with the image and material name and quantity
        item = tk.Frame(filtered_frame, height=50)
        item.pack(fill="x")
        item.photo = photo  # Store the photo as an attribute of the item to prevent it from being garbage collected
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
quantity_label = ttk.Label(control_frame, text="Quantity:")
quantity_label.pack()
quantity_entry = ttk.Entry(control_frame)
quantity_entry.pack()

# Create a button to update the materials
update_button = ttk.Button(control_frame, text="Update", command=update_material)
update_button.pack(pady=10)

# Create a label and dropdown for the material type filter
material_type_label = ttk.Label(control_frame, text="Filter by type:")
material_type_label.pack()
material_type_var = tk.StringVar()
material_type_var.set("quest")
material_type_dropdown = ttk.OptionMenu(control_frame, material_type_var, "quest", "quest", "hideout", command=filtered_materials)
material_type_dropdown.pack()

'''
# Create a frame for the material types and attributes display
display_frame = ttk.Frame(root, padding=10)
display_frame.pack(side="top", fill="x")    

# Create labels for material types and attributes
material_type_label = ttk.Label(display_frame, text="Material Type:")
material_type_label.pack(side="left", padx=10)
material_type_value = ttk.Label(display_frame, text="")
material_type_value.pack(side="left")

attribute_label = ttk.Label(display_frame, text="Attribute:")
attribute_label.pack(side="left", padx=10)
attribute_value = ttk.Label(display_frame, text="")
attribute_value.pack(side="left")
'''


'''
def update_display():
    # Get the selected material type and attribute
    material_type = material_type_combo.get()
    attribute = attribute_combo.get()

    # Update the labels with the selected values
    material_type_value.config(text=material_type)
    attribute_value.config(text=attribute)

# Call the update_display function whenever the material type or attribute is changed
material_type_combo.bind("<<ComboboxSelected>>", lambda event: update_display())
attribute_combo.bind("<<ComboboxSelected>>", lambda event: update_display())
'''
# Filter the materials initially
filtered_materials()

canvas.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Start the main event loop
root.mainloop()

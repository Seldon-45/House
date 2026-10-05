import tkinter as tk  # Import Tkinter library for creating GUI

root = tk.Tk()  # Create the main window
root.title("My House")  # Set the window title

# Create the canvas
canvas = tk.Canvas(root, width=500,
                   height=350, bg="skyblue")  # Create sky-blue background
canvas.pack()  # Place the canvas inside the window


# Draw the house body
canvas.create_rectangle(150, 150, 350, 300,
                        fill="wheat")  # Draw the house body

# Draw the roof
canvas.create_polygon(130, 150, 250, 70, 370, 150,
                      fill="saddlebrown")  # Draw the roof

# Draw the door
canvas.create_rectangle(225, 220, 275, 300,
                        fill="peru")  # Draw the door

# Draw the left window
canvas.create_rectangle(170, 180, 215, 225,
                        fill="lightcyan")  # Draw the left window

# Draw the right window
canvas.create_rectangle(285, 180, 330, 225,
                        fill="lightcyan")  # Draw the right window


root.mainloop()  # Keep the window open
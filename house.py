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

# Draw the sun
canvas.create_oval(390, 30, 460, 100,
                   fill="gold", outline="orange")

#Draw the Dog House Body
canvas.create_rectangle(50, 245, 125, 300,
                        fill="burlywood")

#Draw the Dog House Roof
canvas.create_polygon(40, 245, 87, 210, 135, 245,
                      fill="firebrick")

#Draw the Dog House Door
canvas.create_oval(75, 265, 100, 300,
                        fill="black")


root.mainloop()  # Keep the window open
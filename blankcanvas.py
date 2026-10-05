import tkinter as tk  #tkinter is Python's built-in library for creating GUI

root = tk.Tk() #This creates the main window of your application.
root.title("My First Canvas") #sets the title of the window.

canvas = tk.Canvas(root, width=500,
                   height=350, bg="white") #creates a Canvas widget.
canvas.pack() #tells Tkinter to place the canvas inside the window.

canvas.create_rectangle(40 , 40, 220, 150, fill="coral") # Draw rectangle
canvas.create_oval(280, 50, 440, 190, fill="lightblue") #Draw oval
canvas.create_line(50, 250, 500, 250, width= 4) #Draw Line
canvas.create_text(272, 310, text="Hello Canvas" , font= ("Arial", 20)) #Add text

# A useful way to remember the drawing commands:
# create_rectangle(x1, y1, x2, y2) → draw a rectangle
# create_oval(x1, y1, x2, y2) → draw an oval
# create_line(x1, y1, x2, y2) → draw a line
# create_text(x, y, text=...) → add text

root.mainloop() #This is what keeps your window open and responsive.
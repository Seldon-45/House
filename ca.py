import tkinter as tk
root= tk.Tk()
root.title("Canvas Animation")
canvas = tk.Canvas(
    root, 
    width=600,
    height=350,
    bg="white"
)

canvas .pack()

ball=canvas.create_oval(
    40,40,90,90, 
    fill="orange", 
    outline=""
)


dx=5
#create the animation function
def animate():
    global dx

    #get ball's current coordinates
    x1, y1, x2, y2 = canvas.coords(ball)

    #check right boundry
    if x2 >=600:
        dx=-5

    #check the left boundry
    elif x1 <=0:
        dx=5

    #move the ball horizontally
    canvas.move(ball, dx, 0)

    #repeat the animation after 20 millisecond
    root.after(20, animate)

#start the animation
animate()
root.mainloop()

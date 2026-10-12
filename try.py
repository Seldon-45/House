import tkinter as tk

root = tk.Tk()
root.title("Bouncing Ball Animation")

canvas = tk.Canvas(
    root,
    width=600,
    height=400,
    bg="white"
)
canvas.pack()

# Draw the ground
ground_y = 350
canvas.create_line(
    0, ground_y, 600, ground_y,
    fill="green",
    width=3
)

# Create the ball
ball = canvas.create_oval(
    50, 50, 100, 100,
    fill="orange",
    outline=""
)

# Animation settings
dx = 4
dy = 0
gravity = 1
bounce_speed = -14
bounces = 0
max_bounces = 4

def animate():
    global dx, dy, bounces

    x1, y1, x2, y2 = canvas.coords(ball)

    # Stop after 4 bounces
    if bounces >= max_bounces:
        canvas.coords(ball, x1, ground_y - 50, x2, ground_y)
        return

    # Move right and apply gravity
    canvas.move(ball, dx, dy)
    dy += gravity

    # Check the ball's position
    x1, y1, x2, y2 = canvas.coords(ball)

    # Bounce when the ball hits the ground
    if y2 >= ground_y:
        canvas.coords(ball, x1, ground_y - 50, x2, ground_y)
        dy = bounce_speed
        bounces += 1

        # Stop after the fourth bounce
        if bounces >= max_bounces:
            return

    # Keep the ball inside the canvas horizontally
    if x2 >= 600:
        dx = -4
    elif x1 <= 0:
        dx = 4

    # Animate quickly
    root.after(15, animate)

animate()
root.mainloop()
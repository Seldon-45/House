"""
Group 1: Smart Traffic Light System
Concepts: after(), functions, state changes, timing

Scenario: A traffic light changes automatically from red to green, then yellow,
and repeats. Cars move only when the light is green. A zebra crossing lets
pedestrians cross while the cars wait on red.

THE WORKSHEET TASKS - and where each one is in this file
  TASK 1  Draw a traffic light using rectangles and circles.
          -> "TASK 1" sections: draw_scene(), draw_car(), draw_pedestrian()
  TASK 2  Change the light colours after specific time intervals.
          -> "TASK 2" section: switch_to() and light_tick() using after()
  TASK 3  Make the car stop at a red light and move at a green light.
          -> "TASK 3" section: update_cars()
  TASK 4  Explain how the program controls the timing and movement.
          -> "TASK 4" explanation at the bottom of this file
  GALLERY CHALLENGE  What happens if green lasts longer than red?
          -> change GREEN_SECONDS below and compare "Cars passed"
  EXTRA   Zebra crossing: pedestrians cross only on red, and cars give way.
          -> "ZEBRA CROSSING" section: update_pedestrian()
"""

import math
import random
import tkinter as tk

# ---------------------------------------------------------------
# Settings - change these to experiment
# ---------------------------------------------------------------
RED_SECONDS = 8
GREEN_SECONDS = 6        # GALLERY CHALLENGE: try 12 (green longer than red)
YELLOW_SECONDS = 3

MAX_SPEED = 5.0          # car speed in pixels per update
ACCEL = 0.10             # how fast a car speeds up
BRAKE = 0.12             # how fast a car slows down
SAFE_GAP = 25            # minimum space between cars (pixels)
UPDATE_DELAY = 30        # ms between movement updates
CAR_WIDTH = 211          # width of the car drawing (x from 5 to 216)
CAR_DY = -22             # lifts the car drawing so its wheels sit on the road
CANVAS_W = 820
MAX_CARS = 6

STOP_LINE_X = 600        # cars must stop before this x position
STOP_MARGIN = 4          # stop this many pixels before the line
ZEBRA_X = 612            # zebra crossing starts here...
ZEBRA_END = 668          # ...and ends here

PED_SPEED = 1.3          # pedestrian speed in pixels per update
PED_TOP_Y = 246          # pedestrian waiting spot, top pavement
PED_BOTTOM_Y = 350       # pedestrian waiting spot, bottom pavement
PED_MIN_TIME = 4         # only start crossing if at least this many seconds of red remain

# ---------------------------------------------------------------
# Window
# ---------------------------------------------------------------
root = tk.Tk()
root.title("Smart Traffic Light System")
canvas = tk.Canvas(root, width=CANVAS_W, height=360, bg="#9fd8f5")
canvas.pack()

status_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
status_label.pack(pady=(6, 0))
stats_label = tk.Label(root, text="", font=("Arial", 11))
stats_label.pack(pady=(0, 6))

# ---------------------------------------------------------------
# State (shared by the timers)
# ---------------------------------------------------------------
DURATIONS = {"red": RED_SECONDS, "green": GREEN_SECONDS, "yellow": YELLOW_SECONDS}
NEXT_STATE = {"red": "green", "green": "yellow", "yellow": "red"}
LAMP_COLORS = {"red": "red", "yellow": "gold", "green": "lime green"}

current_state = "red"        # the ONE variable the light writes and the cars read
remaining = RED_SECONDS      # seconds left in the current state
cars = []                    # cars[0] is the front car, cars[-1] is the last one
next_car_id = 0
cars_passed = 0
LAMPS = {}                   # filled in by draw_scene()

pedestrian = {"y": PED_TOP_Y, "direction": 1, "crossing": False, "crossed": 0,
              "done_this_red": False}

# ===============================================================
# TASK 1 - Draw a traffic light using rectangles and circles
# ===============================================================
def draw_scene():
    """Road, pavements, stop line, zebra crossing and the traffic light."""
    # Pavements (rectangles) and road (rectangle)
    canvas.create_rectangle(0, 238, CANVAS_W, 250, fill="#c8c8c8", outline="")
    canvas.create_rectangle(0, 340, CANVAS_W, 352, fill="#c8c8c8", outline="")
    canvas.create_rectangle(0, 250, CANVAS_W, 340, fill="#555555", outline="")

    # Dashed centre line
    for x in range(0, CANVAS_W, 60):
        canvas.create_rectangle(x, 293, x + 30, 297, fill="yellow", outline="")

    # Stop line: cars wait behind this
    canvas.create_rectangle(STOP_LINE_X, 250, STOP_LINE_X + 6, 340, fill="white", outline="")

    # Zebra crossing: white stripes (rectangles) across the road
    for y in range(254, 334, 14):
        canvas.create_rectangle(ZEBRA_X, y, ZEBRA_END, y + 8, fill="white", outline="")

    # Traffic light: pole + box (rectangles), three lamps (circles)
    lx = 728                                  # centre of the traffic light
    canvas.create_rectangle(lx - 2, 150, lx + 2, 238, fill="gray30", outline="")
    canvas.create_rectangle(lx - 30, 40, lx + 30, 160, fill="black", outline="")
    LAMPS["red"] = canvas.create_oval(lx - 18, 50, lx + 18, 86, fill="gray25")
    LAMPS["yellow"] = canvas.create_oval(lx - 18, 87, lx + 18, 123, fill="gray25")
    LAMPS["green"] = canvas.create_oval(lx - 18, 124, lx + 18, 160, fill="gray25")


def draw_car(x, tag):
    """Draw the green car. x is the car's left edge; every part shares one tag
    so canvas.move(tag, ...) moves the whole car together."""
    car = tag
    ox = x - 5            # the shape below starts at x = 5, so shift it to x
    oy = CAR_DY

    def pts(*coords):
        """Shift a list of x, y numbers to the car's current position."""
        return [c + (ox if i % 2 == 0 else oy) for i, c in enumerate(coords)]

    # Car body
    canvas.create_polygon(
        pts(8, 308, 18, 293, 48, 280,
            91, 273, 137, 282, 169, 302,
            201, 309, 216, 320, 215, 335,
            201, 342, 19, 342, 5, 332),
        fill="#138C3A", outline="#08712B", width=2, tags=car)

    # Car roof
    canvas.create_polygon(
        pts(40, 294, 57, 278, 91, 278,
            119, 282, 142, 299),
        fill="#138C3A", outline="#08712B", width=2, tags=car)

    # Windows
    canvas.create_polygon(
        pts(61, 282, 88, 282, 88, 296, 49, 296),
        fill="#D9F4F7", outline="white", width=2, tags=car)
    canvas.create_polygon(
        pts(94, 282, 117, 285, 134, 296, 94, 296),
        fill="#D9F4F7", outline="white", width=2, tags=car)

    # Door and handle
    canvas.create_line(pts(94, 299, 94, 332), fill="#075F26", width=2, tags=car)
    canvas.create_line(pts(109, 307, 120, 307), fill="white", width=2, tags=car)

    # Wheels
    for wx in [48, 174]:
        canvas.create_oval(pts(wx - 20, 310, wx + 20, 350),
                           fill="#202020", outline="#111111", width=2, tags=car)
        canvas.create_oval(pts(wx - 13, 317, wx + 13, 343),
                           fill="#EEEEEE", outline="#AAAAAA", width=2, tags=car)
        canvas.create_oval(pts(wx - 7, 323, wx + 7, 337),
                           fill="#555555", outline="", tags=car)


def draw_pedestrian():
    """A simple person: a circle for the head, a rectangle for the body."""
    x = (ZEBRA_X + ZEBRA_END) // 2
    y = pedestrian["y"]
    canvas.create_oval(x - 5, y - 26, x + 5, y - 16, fill="#f2c29b", outline="black", tags="ped")
    canvas.create_rectangle(x - 4, y - 16, x + 4, y, fill="#d94f4f", outline="black", tags="ped")


def set_light(state):
    """Turn one lamp on and the other two off."""
    for name, lamp in LAMPS.items():
        canvas.itemconfig(lamp, fill=LAMP_COLORS[name] if name == state else "gray25")


def update_labels():
    waiting = sum(1 for c in cars if c["speed"] < 0.1 and c["x"] + CAR_WIDTH <= STOP_LINE_X)
    walker = "crossing" if pedestrian["crossing"] else "waiting"
    status_label.config(
        text=f"Light: {current_state.upper()}   |   changes in {remaining} s")
    stats_label.config(
        text=f"Cars passed: {cars_passed}   |   Cars waiting: {waiting}   |   "
             f"Pedestrian: {walker} (crossed {pedestrian['crossed']}x)")

# ===============================================================
# TASK 2 - Change the light colours after specific time intervals
# ===============================================================
def switch_to(state):
    """Change the light state (a STATE CHANGE). Cars read current_state."""
    global current_state, remaining
    current_state = state
    remaining = DURATIONS[state]
    set_light(state)
    if state != "red":
        pedestrian["done_this_red"] = False   # pedestrian may cross on the next red
        for car in cars:                      # forget old yellow-light decisions
            car["decision"] = None


def light_tick():
    """Runs once per second using after(): count down, then change state."""
    global remaining
    remaining -= 1
    if remaining <= 0:
        switch_to(NEXT_STATE[current_state])
    update_labels()
    root.after(1000, light_tick)      # ask Tkinter to call this again in 1 s

# ===============================================================
# TASK 3 - Make the car stop at a red light and move at a green light
# ===============================================================
def braking_distance(speed):
    """Distance needed to stop from this speed with constant braking."""
    return speed * speed / (2 * BRAKE)


def spawn_car():
    """Add a new car on the left if there is room. Repeats at random times."""
    global next_car_id
    room = not cars or cars[-1]["x"] > SAFE_GAP
    if len(cars) < MAX_CARS and room:
        tag = f"car{next_car_id}"
        start_x = -CAR_WIDTH - 10
        draw_car(start_x, tag)
        cars.append({"tag": tag, "x": start_x, "speed": MAX_SPEED,
                     "decision": None, "counted": False})
        next_car_id += 1
    root.after(random.randint(2000, 4000), spawn_car)


def update_cars():
    """Runs every 30 ms: decide each car's speed, then move it."""
    global cars_passed
    finished = []

    for i, car in enumerate(cars):
        front = car["x"] + CAR_WIDTH
        dist_to_line = STOP_LINE_X - front
        limit = math.inf              # free space before the car must stop

        # 1) Keep a safe gap to the car in front
        if i > 0:
            limit = min(limit, cars[i - 1]["x"] - front - SAFE_GAP)

        # 2) Obey the light and the zebra crossing (only before the stop line)
        must_stop = False
        if dist_to_line >= -1:
            if current_state == "red" and car["decision"] != "go":
                must_stop = True                       # RED  -> stop
            elif current_state == "yellow":            # YELLOW -> stop if safe
                if car["decision"] is None:
                    can_stop = dist_to_line >= braking_distance(car["speed"])
                    car["decision"] = "stop" if can_stop else "go"
                must_stop = car["decision"] == "stop"
            if pedestrian["crossing"] and car["decision"] != "go":
                must_stop = True                       # give way to pedestrians
        if must_stop:
            limit = min(limit, dist_to_line - STOP_MARGIN)

        # GREEN -> no restriction, the car drives on (limit stays infinite)

        # 3) Target speed that lets the car stop exactly in time
        if limit == math.inf:
            target = MAX_SPEED
        else:
            target = min(MAX_SPEED, math.sqrt(2 * BRAKE * max(limit, 0)))

        # 4) Speed up gently, slow down gently
        if car["speed"] < target:
            car["speed"] = min(target, car["speed"] + ACCEL)
        elif car["speed"] > target:
            car["speed"] = max(target, car["speed"] - 2 * BRAKE)

        # 5) Move the car
        car["x"] += car["speed"]
        canvas.move(car["tag"], car["speed"], 0)

        if not car["counted"] and car["x"] + CAR_WIDTH > STOP_LINE_X + 6:
            car["counted"] = True
            cars_passed += 1
        if car["x"] > CANVAS_W + 20:
            finished.append(car)

    for car in finished:              # remove cars that left the screen
        canvas.delete(car["tag"])
        cars.remove(car)

    update_labels()
    root.after(UPDATE_DELAY, update_cars)

# ===============================================================
# EXTRA - Zebra crossing: pedestrians cross only on red
# ===============================================================
def zebra_is_clear():
    """True if no car is on or touching the zebra crossing."""
    for car in cars:
        if car["x"] + CAR_WIDTH > ZEBRA_X and car["x"] < ZEBRA_END:
            return False
    return True


def update_pedestrian():
    """Runs every 30 ms: wait for a safe red light, then walk across."""
    ped = pedestrian
    if not ped["crossing"]:
        red_long_enough = current_state == "red" and PED_MIN_TIME <= remaining <= RED_SECONDS - 1
        if red_long_enough and not ped["done_this_red"] and zebra_is_clear():
            ped["crossing"] = True            # cars will now give way
    else:
        step = ped["direction"] * PED_SPEED
        ped["y"] += step
        canvas.move("ped", 0, step)
        target = PED_BOTTOM_Y if ped["direction"] == 1 else PED_TOP_Y
        if (ped["direction"] == 1 and ped["y"] >= target) or \
           (ped["direction"] == -1 and ped["y"] <= target):
            canvas.move("ped", 0, target - ped["y"])
            ped["y"] = target
            ped["crossing"] = False
            ped["direction"] *= -1            # next time, walk back
            ped["crossed"] += 1
            ped["done_this_red"] = True           # one crossing per red light
    root.after(UPDATE_DELAY, update_pedestrian)

# ---------------------------------------------------------------
# Start everything
# ---------------------------------------------------------------
draw_scene()
draw_pedestrian()
set_light("red")
update_labels()
root.after(1000, light_tick)             # timer 1: the light (every 1 s)
root.after(500, spawn_car)               # timer 2: new cars (random times)
root.after(UPDATE_DELAY, update_cars)    # timer 3: car movement (every 30 ms)
root.after(UPDATE_DELAY, update_pedestrian)  # timer 4: pedestrian (every 30 ms)
root.mainloop()

# ===============================================================
# TASK 4 - How the program controls the timing and movement
# ===============================================================
# TIMING
#  * root.after(ms, function) tells Tkinter: "call this function after ms
#    milliseconds". It does NOT pause the program, so the window stays alive.
#  * light_tick() calls after() on itself every second. It counts down
#    `remaining`; at 0 it calls switch_to() which changes current_state to the
#    next colour (red -> green -> yellow -> red) and lights the matching lamp.
#  * The durations come from RED_SECONDS, GREEN_SECONDS and YELLOW_SECONDS.
#
# MOVEMENT
#  * update_cars() calls after() on itself every 30 ms. Each time it moves
#    every car a few pixels with canvas.move(), so many small steps look like
#    smooth driving.
#  * Each step the car reads current_state:
#       green  -> no limit, speed up to MAX_SPEED
#       yellow -> stop if it can brake before the line, otherwise keep going
#       red    -> slow down smoothly and stop just behind the stop line
#  * Cars also keep a safe gap to the car in front, so they queue up.
#
# STATE CHANGES
#  * current_state is the shared variable: the light WRITES it, the cars READ it.
#    That is how one timer controls the other.
#
# ZEBRA CROSSING
#  * update_pedestrian() waits for red, with enough time left and a clear
#    zebra. Then it sets pedestrian["crossing"] = True. Cars check this flag
#    and stop, and the person walks across, then waits for the next red.
#
# GALLERY CHALLENGE: What if green lasts longer than red?
#  * Set GREEN_SECONDS = 12 and watch "Cars passed". More cars get through
#    each cycle, but the pedestrians (and any cross traffic) wait much longer.
#    A real signal balances both, which is why green and red times are chosen
#    from how busy each direction is.
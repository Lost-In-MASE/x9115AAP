from swampy.TurtleWorld import *
from math import *

def draw_polyline(t, length, n, angle):
    for i in range(n):
        fd(t, length)
        lt(t, angle)

def draw_arc(t, r, a):
    c = 2 * pi * r * a / 360
    n = int(c / 3) + 1
    length = int(c) / n
    angle = float(a) / n;
    draw_polyline(t, length, n, angle)

def draw_petal(t, r, a):
    for i in range(2):
        draw_arc(t, r, a)
        lt(t, 180 - a)

def draw_flower(t, r, a, n):
    for i in range(n):
        draw_petal(t, r, a)
        lt(t, 360.0/n)

def draw_next(t, r):
    pu(t)
    fd(t, 3 * r)
    pd(t)

world = TurtleWorld()
turtle = Turtle()
turtle.delay = 0.01
radius = 120

draw_flower(turtle, radius, 60, 7)
draw_next(turtle, radius)
draw_flower(turtle, radius, 80, 10)
draw_next(turtle, radius)
draw_flower(turtle, radius, 30, 20)
draw_next(turtle, radius)

wait_for_user()
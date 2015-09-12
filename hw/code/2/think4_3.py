from swampy.TurtleWorld import *
from math import *

def draw_polygon(turtle, n, length):
    angle = 360.0 / n
    lt(turtle)
    for i in range(n):
        fd(turtle, length)
        lt(turtle, angle)
    draw_circumradius(turtle, n, length)

def draw_circumradius(turtle, n, length):
    inner_angle = ((n-2) * 180.0) / n;
    radius = length / (2 * sin(pi / n))
    central_angle = 360.0 / n
    lt(turtle, inner_angle / 2)
    fd(turtle, radius)
    lt(turtle, 180)
    for i in range(n-1):
        lt(turtle, central_angle)
        fd(turtle, radius)
        lt(turtle, 180)
        fd(turtle, radius)
        lt(turtle, 180)
    lt(turtle, central_angle)
    fd(turtle, radius)
    lt(turtle, 180.0 - (inner_angle / 2))

def next_draw(turtle, length):
    pu(turtle)
    rt(turtle, 90)
    fd(turtle, length * 3)
    pd(turtle)

world = TurtleWorld()
turtle = Turtle()
turtle.delay = 0.01
length = 50;
draw_polygon(turtle, 5, length)
next_draw(turtle, length)
draw_polygon(turtle, 6, length)
next_draw(turtle, length)
draw_polygon(turtle, 7, length)

wait_for_user()


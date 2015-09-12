from swampy.TurtleWorld import *
import math
__author__ = 'parthsatra'

def polyline(t, length, n, angle):
    for i in range(n):
        fd(t, length)
        lt(t, angle)

def polygon(t, length, n):
    angle = 360.0/n;
    polyline(t, length, n , angle)

def square(t, length):
    polygon(t, length, 4)

def arc(t, r, a):
    c = 2 * math.pi * r * a / 360
    n = int(c / 3) + 1
    length = int(c) / n
    angle = float(a) / n;
    polyline(t, length, n, angle)

def circle(t, radius):
    arc(t, radius, 360)

world = TurtleWorld()
bob = Turtle()
bob.delay = 0.01

arc(bob, 70, 90)

wait_for_user()


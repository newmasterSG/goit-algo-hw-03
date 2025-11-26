import math
import turtle
from typing import Tuple

Point = Tuple[float, float]


def draw_line(a: Point, b: Point):
    turtle.penup()
    turtle.goto(a[0], a[1])
    turtle.pendown()
    turtle.goto(b[0], b[1])


def draw_koch_segment(a: Point, b: Point, depth: int):
    if depth == 0:
        draw_line(a, b)
        return

    x1, y1 = a
    x2, y2 = b

    dx = (x2 - x1) / 3.0
    dy = (y2 - y1) / 3.0

    p1: Point = (x1 + dx,         y1 + dy)
    p2: Point = (x1 + 2 * dx,     y1 + 2 * dy)

    angle = math.radians(60)
    rx = dx * math.cos(angle) - dy * math.sin(angle)
    ry = dx * math.sin(angle) + dy * math.cos(angle)

    peak: Point = (p1[0] + rx, p1[1] + ry)

    draw_koch_segment(a,    p1,   depth - 1)
    draw_koch_segment(p1,   peak, depth - 1)
    draw_koch_segment(peak, p2,   depth - 1)
    draw_koch_segment(p2,   b,    depth - 1)


def draw_koch_snowflake(center: Point, size: float, depth: int):
    cx, cy = center
    h = size * math.sqrt(3) / 2

    a: Point = (cx - size / 2, cy - h / 3)
    b: Point = (cx + size / 2, cy - h / 3)
    c: Point = (cx,            cy + 2 * h / 3)

    draw_koch_segment(a, b, depth)
    draw_koch_segment(b, c, depth)
    draw_koch_segment(c, a, depth)


def main():
    turtle.speed(0)
    turtle.hideturtle()
    turtle.tracer(False)

    draw_koch_snowflake(center=(0, 0), size=300, depth=4)

    turtle.tracer(True)
    turtle.done()


if __name__ == "__main__":
    main()
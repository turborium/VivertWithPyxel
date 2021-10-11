# pip install вот это https://github.com/kitao/pyxel/
# засохший кусок кода!
import pyxel
from dataclasses import dataclass
import random
import math
import copy


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    dx: float = 0.0
    dy: float = 0.0

@dataclass
class Vivert:
    points: list
    color: int = 8

OLD_VIVERT_COUNT=8
SCREEN_WIDTH=256
SCREEN_HIGHT=192

vivert_colors = [6,8,7]
vivert_list = []
vivert_stack = []

def init():
    for color in vivert_colors:
        object = Vivert([], color)
        for _ in range(4):
            point = Point(x=random.uniform(0, SCREEN_WIDTH), y=random.uniform(0, SCREEN_HIGHT))
            angle = random.uniform(0, math.pi)
            point.dx = math.cos(angle) * 4
            point.dy = math.sin(angle) * 4
            object.points.append(point)
        vivert_list.append(object)
    
    for _ in range(OLD_VIVERT_COUNT):
        vivert_stack.append(vivert_list) 
    
    pyxel.init(SCREEN_WIDTH, SCREEN_HIGHT, fps=15)
    pyxel.run(update, draw)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw_object(points, color):
    pyxel.line(int(points[0].x), int(points[0].y), int(points[1].x), int(points[1].y), color)
    pyxel.line(int(points[1].x), int(points[1].y), int(points[2].x), int(points[2].y), color)
    pyxel.line(int(points[2].x), int(points[2].y), int(points[3].x), int(points[3].y), color)
    pyxel.line(int(points[3].x), int(points[3].y), int(points[0].x), int(points[0].y), color)

def draw():
    # shift old_objects array
    for i in range(len(vivert_stack) - 1):
        vivert_stack[i] = vivert_stack[i+1]
    vivert_stack[len(vivert_stack)-1] = copy.deepcopy(vivert_list)

    for vivert in vivert_list:
        # update points pos
        for point in vivert.points:
            # перемещаем точку в соответсвии со скоростью
            point.x = point.x + point.dx
            point.y = point.y + point.dy

            # обрабатываем вылет за экран
            if point.x < 0:
                point.dx = abs(point.dx)
            if point.x > SCREEN_WIDTH:
                point.dx = -abs(point.dx)
            if point.y < 0:
                point.dy = abs(point.dy)
            if point.y > SCREEN_HIGHT:
                point.dy = -abs(point.dy)

    for old_vivert in vivert_stack[0]:
        draw_object(old_vivert.points, 0)

    for vivert in vivert_list:
        draw_object(vivert.points, vivert.color)

init()
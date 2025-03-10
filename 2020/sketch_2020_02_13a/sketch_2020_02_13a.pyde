"""
Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day
Explorando um experimento de geração de formas
proposto por Leopoldo Leal
"""

from random import choice, sample, shuffle
from itertools import product, permutations, combinations
from forms import b_poly_arc_augmented
from line_geometry import *

NUM_POINTS = 6
BORDER = 100
SIZE = 100
RDS = 25
select_mode = True
points = []

def setup():
    global grid, ensambles
    size(1000, 500)
    grid = list(product(range(BORDER, width / 2 - BORDER + 1, SIZE),
                        range(BORDER, height - BORDER + 1, SIZE)))
    points[:] = sample(grid, 6)
    ensambles = create_ensambles(create_polys(points))

def draw():
    background(200)
    translate(width / 2, 0)
    scale(1 / 4.)
    i = 0
    for y in range(4):
        for x in range(4):
            pushMatrix()
            translate(width / 2 * x, height * y)
            draw_ensembles(i)
            if select_mode:
                draw_pins(i)
            popMatrix()
            i += 1
    resetMatrix()
    for i in range(16):
        draw_ensembles(i)

def create_polys(points):
    """ non intersecting poly """
    all_polys = list(permutations(points, NUM_POINTS))
    tested, polys, ni_polys = set(), [], []
    for poly in all_polys:
        edges = edges_as_sets(poly)
        if edges not in tested and edges:
            tested.add(edges)
            polys.append(poly)
    for poly in polys:
        if not intersecting(poly):
            ni_polys.append(poly)
    print("caminhos sem auto-cruzar: {}".format(len(ni_polys)))
    return list(ni_polys)

def create_ensambles(polys):
    ens = []
    for poly in polys:
        for i in range(2 ** NUM_POINTS):
            rads = []
            rad_opts = num_to_base(i, 2, NUM_POINTS)
            for c in rad_opts:
                if c == "0":
                    rads.append(-1 * RDS)
                else:
                    rads.append(1 * RDS)
            ens.append((poly, rads))
    non_crossing_ens = []
    for e in ens:
        crossing = b_poly_arc_augmented(e[0], e[1], check_intersection=True)
        if not crossing:
            non_crossing_ens.append(e)

    print(
        "variantes arredondadas sem auto-cruzar: {}".format(len(non_crossing_ens)))
    return non_crossing_ens

def draw_ensembles(i):
    if i < len(ensambles):
        noFill()
        stroke(0)
        strokeWeight(8)
        b_poly_arc_augmented(ensambles[i][0], ensambles[i][1])
        if keyPressed and keyCode == SHIFT:
            for p, r in zip(ensambles[i][0], ensambles[i][1]):
                if r > 0:
                    fill(0, 0, 255)
                else:
                    fill(255, 0, 0)
                noStroke()
                circle(p[0], p[1], 10)

def draw_pins(i):
    resetMatrix()
    noStroke()
    fill(255, 100)
    if grid[i] in points:
        fill(0, 100)
    circle(grid[i][0],
           grid[i][1], RDS * 2)

def keyPressed():
    global select_mode
    if key == "p" or key == 'P':
        saveFrame("####.png")
    if key == ' ':
        if select_mode:
            select_mode = False
        else:
            select_mode = True
    if key == 'r':
        if len(points) == NUM_POINTS:
            ensambles[:] = create_ensambles(create_polys(points))
        else:
            print(u"Só vale com {} pinos!".format(NUM_POINTS))   
    if key == 'R':
        points[:] = sample(grid, NUM_POINTS)
        ensambles[:] = create_ensambles(create_polys(points))

def mouseClicked():
    for p in grid:
        if dist(p[0], p[1], mouseX, mouseY) < RDS:
            if p in points:
                points.remove(p)
            else:
                points.append(p)


def num_to_base(num, base, pad=0):
    BS = ""
    for i in range(base):
        BS += str(i)
    result = ""
    while num:
        result += BS[num % base]
        num //= base
    while len(result) < pad:
        result = result + "0"
    return result[::-1]

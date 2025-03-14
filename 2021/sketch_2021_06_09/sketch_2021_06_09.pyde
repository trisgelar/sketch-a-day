from itertools import product, combinations, permutations
from os.path import isfile
import pickle
from villares.line_geometry import edges_as_sets, is_poly_convex
from villares.gif_export import gif_export

add_library('gifAnimation')

def setup():
    global grade, quads
    size(475, 475)
    frameRate(10)
    grade = list(product(range(50, 500, 75), repeat=2))    
    if not isfile(sketchPath("poly.data")):
        all_polys = list(permutations(grade, 4))
        tested, polys = set(), []
        for poly in all_polys:
            if is_poly_convex(poly):
                edges = edges_as_sets(poly)
                if edges not in tested and edges:
                    tested.add(edges)
                    polys.append(poly)
        with open("poly.data", "w") as f:
                pickle.dump(polys, f)
        print("poly.data saved!")
    else:
        with open("poly.data") as f:
                polys = pickle.load(f)
    print("Number of visually unique polys: {}".format(len(polys)))
    t = millis()
    quads = [(a, b, c, d) for a, b, c, d in polys if 
           # 50  in c and 50  not in a and 50 not in d and 50 not in b and
           corner_angle(a, b, d) == HALF_PI  and
           corner_angle(b, a, c) == HALF_PI and
           corner_angle(c, b, d) == HALF_PI
           ]
    
    print("milliseconds finding quads: {}".format(millis() - t))
    quads.sort(key=poly_area)
    print("Number of quads: {}".format(len(quads)))

             
def draw():
    colorMode(RGB)
    fill(200, 32)
    rect(0, 0, width, height)
    # background(200, 200, 180)
    fill(0)
    for x, y in grade:
        circle(x, y, 5)
    q = quads[(frameCount - 1) % len(quads)]
    colorMode(HSB)
    fill(poly_area(q) % 256, 255, 255)
    beginShape()
    for x, y in q:
        vertex(x, y)
    endShape(CLOSE)

    # if frameCount % len(quads) == 0:
    #     gif_export(GifMaker, finish='True')
    #     exit()
    # else:
    #     gif_export(GifMaker, 'output', delay=200, quality=100)


def poly_area(points):
    points = list(points)
    area = 0.0
    for (ax, ay), (bx, by) in zip(points, points[1:] + [points[0]]):
        area += ax * by
        area -= bx * ay
    return abs(area) / 2.0

def corner_angle(c, a, b):
    ac = (c[0] - a[0]) ** 2 + (c[1] - a[1]) ** 2
    bc = (c[0] - b[0]) ** 2 + (c[1] - b[1]) ** 2
    ab = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    return acos((bc + ac - ab) / sqrt(4 * bc * ac))
  

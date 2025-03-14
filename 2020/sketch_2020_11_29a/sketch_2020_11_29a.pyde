from __future__ import division
from itertools import product

from villares.line_geometry import draw_poly, poly_edges, Line
from villares.line_geometry import rect_points, rotate_point, inter_lines

def setup():
    size(500, 500)
    global ang_pairs
    angs = (0, 45, 90, 135) #122.5, 135, 147.5)
    ang_pairs = list(set(frozenset((a, b)) for a, b in  product(angs, repeat=2) if a != b))
    ang_pairs.extend((ang,) for ang in angs)
    textSize(8)
        

def draw():
    background(130, 50, 100)
    print frameRate
    stroke(0)
    fill(255)
    s = 100
    i = 1
    for x, y in grid(5, 6, s, s):
        r = rect_points(5 + x, 5 + y, s - 10, s - 10)
        rect(6 + x, 6 + y, s - 12, s - 12)
        # strokeWeight(3)
        ang_pair = tuple(ang_pairs[i % len(ang_pairs)]) 
        if i >=  2* len(ang_pairs): ang_pair = ang_pair[::-1] if len(ang_pair) > 1 else []
        # else: strokeWeight(1)
        for a, ang in enumerate(ang_pair):
            hatch_rect(r, radians(ang),
                       spacing=6.0,
                       function=fixed_dash_line if i >= len(ang_pairs) and not a % 2 else None,
                       dash_spacing=6.0,
                       # element_spacing=10.0,
                       # element_size=4,
                       # element_function=lambda x, y, _: point(x, y),
                       base=True,
                       )
        text(str(tuple(ang_pair)), x + 10, y + 5)
        i += 1

def fixed_dash_line(xa, ya, xb, yb, **kwargs):
    proportion = kwargs.pop('dash_proportion', kwargs.pop('proportion', 0.5))
    spacing = kwargs.pop('dash_spacing', kwargs.pop('spacing', 20))
    base_line = kwargs.pop('base_line', None)
    inside = Line(xa, ya, xb, yb)
    base_line = base_line or inside
    b = base_line.as_PVector()
    base_length = b.mag()
    divisions = int(base_length / spacing)
    v = (b * spacing).div(base_length)
    xs, ys = base_line[0][0], base_line[0][1]
    for i in range(0, int(divisions) + 1):
        xe, ye = xs + v.x * proportion, ys + v.y * proportion
        start_in, end_in = inside.contains_point(
            xs, ys), inside.contains_point(xe, ye)
        if start_in and end_in:
            line(xs, ys, xe, ye)
        elif end_in:
            ending = Line(xe, ye, inside[1][0], inside[1][1])
            if ending.dist() <= spacing * proportion:
                ending.plot()
        elif start_in:
            starting = Line(xs, ys, inside[0][0], inside[0][1])
            if starting.dist() <= spacing * proportion:
                starting.plot()
        xs += v.x
        ys += v.y


# def element_line(xa, ya, xb, yb, **kwargs):
#     spacing = kwargs.pop('element_spacing', kwargs.pop('spacing', 20))
#     element_size = kwargs.pop('element_size', 5)
#     element_function = kwargs.pop('element_function', square)
#     divisions = int(dist(xa, ya, xb, yb) / spacing) + 1  # + keyPressed
#     for i in range(1, divisions):
#         t = i / float(divisions)
#         x, y, _ = Line(xa, ya, xb, yb).line_point(t)
#         element_function(x, y, element_size)

def grid(cols, rows, colSize=1, rowSize=1):
    """
    Returns an iterator that provides coordinate tuples. Example:
    # for x, y in grid(10, 10, 12, 12):
    #     rect(x, y, 10, 10)
    """
    rowRange = range(int(rows))
    colRange = range(int(cols))
    for y in rowRange:
        for x in colRange:
            yield (x * colSize, y * rowSize)

def keyPressed():
    saveFrame(sketch_name() + '.png')
    
def sketch_name():
    from os import path
    sketch = sketchPath()
    return path.basename(sketch)

def hatch_rect(*args, **kwargs):
    if len(args) == 2:
        r, angle = args
    else:
        x, y, w, h, angle = args
        r = rect_points(x, y, w, h, kwargs.get('mode', CORNER))
    spacing = kwargs.get('spacing', 10)
    function = kwargs.pop('function', None)
    base = kwargs.pop('base', False)
    d = dist(r[0][0], r[0][1], r[2][0], r[2][1])
    cx = (r[0][0] + r[1][0]) / 2.0
    cy = (r[1][1] + r[2][1]) / 2.0
    num = int(d / spacing)
    rr = [rotate_point(x, y, angle, cx, cy)
          for x, y in rect_points(cx, cy, d, d, mode=CENTER)]
    # stroke(255, 0, 0)   # debug mode
    ab = Line(rr[0], rr[1])  # ;ab.plot()  # debug mode
    cd = Line(rr[3], rr[2])  # ;cd.plot()  # debug mode
    for i in range(num + 1):
        abp = ab.line_point(i / float(num) + EPSILON)
        cdp = cd.line_point(i / float(num) + EPSILON)
        if not function:
            for hli in inter_lines(Line(abp, cdp), r):
                hli.plot()
        else:
            kwargs['function'] = function
            if base == True:
                # add back base kwarg as a line
                kwargs['base_line'] = Line(abp, cdp)
                for hli in inter_lines(Line(abp, cdp), r):
                    hli.plot(**kwargs)
            else:
                for hli in inter_lines(Line(abp, cdp), r):
                    hli.plot(**kwargs)

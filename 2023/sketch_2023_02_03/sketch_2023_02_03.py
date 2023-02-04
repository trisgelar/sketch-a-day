import py5

from shapely.affinity import translate as shapely_translate
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection, LineString, Point
from shapely.ops import unary_union

import trimesh

dragged = -1

def setup():
    global shapes
    py5.size(1200, 400, py5.P3D)
    py5.color_mode(py5.HSB)

    font = py5.create_font('Inconsolata Bold', 100)
    shapes = polys_from_text(
        'Oi B008!\né o gnumundo®...\nviva a ciberlândia!',
        font)

def draw():
    py5.window_title(str(py5.get_frame_rate()))
    py5.background(100)
    py5.translate(100, 100)
    if py5.is_key_pressed:
        py5.rotate_x(py5.PI / 10)
    py5.fill(255, 100)
    for i, shp in enumerate(shapes):
        py5.fill((i * 8) % 256, 255, 255, 100)
        if i == dragged:
            draw_shapely_objs(shp)
    
    union = unary_union(shapes)
    if not py5.is_key_pressed:
        draw_shapely_objs(union)
    else:
        for p in union.geoms:
            if isinstance(p, Polygon):
                m = trimesh.creation.extrude_polygon(p, 10)
                draw_mesh(m)
      
def mouse_moved():
    global dragged
    if not py5.is_mouse_pressed:
        for i, shp in enumerate(shapes):
            if shp.contains(Point(py5.mouse_x - 100, py5.mouse_y - 100)):
                dragged = i
                break
        else:
            dragged = -1

def mouse_dragged():
    if dragged >= 0:
        dx = py5.mouse_x - py5.pmouse_x
        dy = py5.mouse_y - py5.pmouse_y
        shapes[dragged] = shapely_translate(shapes[dragged], xoff=dx, yoff=dy) 

def polys_from_text(words, font, alternate_spacing=False):
    """
    Produce a list of shapely Polygons (with holes!) from a string.
    New-line chars will try to move text to a new line.
    
    The alternate_spacing option will pick the glyph
    spacing from py5.text_width() for each glyph, it can be
    too spaced, but good for monospaced font alignment.
    """
    py5.text_font(font)
    space_width = py5.text_width(' ')
    results = []
    x_offset = y_offset = 0
    for c in words:
        if c == '\n':
            y_offset += font.get_size()
            x_offset = 0  # assuming left aligned text...
            continue
        glyph_pt_lists = [[]]
        c_shp = font.get_shape(c, 1)
        vs3 = [c_shp.get_vertex(i) for i in range(c_shp.get_vertex_count())]
        vs = set()
        for vx, vy, _ in vs3:
            x = vx + x_offset
            y = vy + y_offset
            glyph_pt_lists[-1].append((x, y))
            if (x, y) not in vs:
                vs.add((x, y))
            else:
                glyph_pt_lists.append([])  # will leave a trailling empty list
        if alternate_spacing:
            w = py5.text_width(c)
        else:
            w = c_shp.get_width() if vs3 else space_width
        x_offset += w
        # filter out elements with less than 3 points 
        # and stop before the trailling empty list
        glyph_polys = [Polygon(p) for p in glyph_pt_lists[:-1] if len(p) > 2]
        if glyph_polys:  # there are still empty glyphs at this point.
            glyph_shapes = process_glyphs(glyph_polys)
            results.extend(glyph_shapes)
    return results


def process_glyphs(polys):
    """
    Try to subtract the shapely Polygons representing a glyph
    in order to produce appropriate looking glyphs!
    """
    polys = sorted(polys, key=lambda p: p.area, reverse=True)
    results = [polys[0]]
    for p in polys[1:]:
        # works on edge cases like â and ®
        for i, earlier in enumerate(results):
            if earlier.contains(p):
                results[i] = results[i].difference(p)
                break
        else:   # the for-loop's else only executes after unbroken loops 
            results.append(p)
    return results


def draw_shapely_objs(element):
    """
    With py5, draw some shapely object (or a list of objects).
    """
    if isinstance(element, (MultiPolygon, GeometryCollection)):
        for p in element.geoms:
            draw_shapely_objs(p)
    elif isinstance(element, Polygon):
        with py5.begin_closed_shape():
            if element.exterior.coords:
                py5.vertices(element.exterior.coords)
            for hole in element.interiors:
                with py5.begin_contour():
                    py5.vertices(hole.coords)
    elif isinstance(element, list):
        for i, p in enumerate(element):
            draw_shapely_objs(p)
    elif isinstance(element, LineString):
        (xa, ya), (xb, yb) = element.coords
        py5.line(xa, ya, xb, yb)
    elif isinstance(element, Point):
        with py5.push_style():
            x, y = element.coords[0]
            py5.point(x, y)
    else:
        print(f"I can't draw {element}.")

      
def draw_mesh(m):
    for i, face in enumerate(m.faces):
        py5.fill((m.vertices[0][0]) % 256, 255, 255)
        with py5.begin_closed_shape():
            py5.vertices([m.vertices[v] for v in face])

py5.run_sketch()

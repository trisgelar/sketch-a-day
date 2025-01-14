import threading
import py5
import py5_tools
from random import randint, choice, seed

def setup():
    py5.size(900, 900, py5.P3D)
    py5.color_mode(py5.HSB)
    py5.stroke_weight(3)
    seed(1)
    set_records()

def draw():
    seed(1)
    py5.background(100, 60, 60)
    py5.lights()
    py5.translate(py5.width / 2, py5.height / 2, 100)
    py5.scale(0.5)
    py5.rotate_x(py5.QUARTER_PI)
    py5.rotate_z(py5.QUARTER_PI)
    py5.translate(-py5.width / 2, -py5.height / 2, 0)
    draw_records(0, 0, py5.width, py5.height, records, margin=0)


def draw_records(xo, yo, wo, ho, records, **kwargs):
    z = kwargs.pop('z', 100)
    margin = 0 # kwargs.pop('margin', choice((0, 5)))
    x, y = xo + margin, yo + margin,
    w, h = wo - 2 * margin, ho - 2 * margin
    total_area = sum(map(lambda r: r[1], records))
    rx = ry = 0
    for i, (name, area, sub) in enumerate(records):
        py5.fill(512 * area / total_area, 200, 200)
        if w > h:
            rw, rh = py5.remap(area, 0, total_area, 0, w), h
        else:
            rw, rh = w, py5.remap(area, 0, total_area, 0, h)
        if sub:
            py5.push()
            #py5.translate(0, 0, z)
            draw_records(x + rx, y + ry, rw, rh, sub, z=z * 1.25)
            py5.pop()
        else:
            slab(x + rx, y + ry, rw, rh, z)
        if w > h:
            rx += rw
        else:
            ry += rh

def slab(x, y, w, h, d):
    py5.push()
    py5.translate(x + w / 2, y + h / 2, d / 2)
    py5.box(w, h, d)
    py5.pop()


def generate_record(num, name='', max_elements=5):
    if name:
        name += '.'
    result = []
    for i in range(max_elements):
        if randint(1, 10) > 5 or num < 5:
            result.append((name + str(i), randint(1, 5), []))
        else:
            result.append((name + str(i),
                           randint(2, 10),
                           generate_record(num - 5, name + str(i))))
    return result

def key_pressed():
    # save_frame('###.png')
    if py5.key == ' ':
        m = py5.millis()
        seed(m)
        print(m)
        set_records()
    elif py5.key == 'g':
        export.start()

def set_records():
    global records
    records = generate_record(20)

# class SimpleThread(threading.Thread):
#     def __init__(self, func, *args, **kwargs):
#         super().__init__()
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#     def run(self):
#         self.func(*self.args, **self.kwargs)
        
export = threading.Thread(target=py5_tools.animated_gif, args=('out.gif', 10, 1, 0.5))

py5.run_sketch()

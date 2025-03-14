# Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day
SKETCH_NAME = "s189"  # 20180706
OUTPUT = ".gif"

from gif_export_wrapper import *
add_library('gifAnimation')

num_hatches = 5
hatches = []
global_rot = 0

def setup():
    print_text_for_readme(SKETCH_NAME, OUTPUT)
    size(500, 500)
    # smooth(4)
    for _ in range(num_hatches):
        hatches.append(Hatch())

def draw():
    global global_rot
    background(200)
    stroke(0)
    for i, h in enumerate(hatches):
        h.plot(do_rotation = frameCount/50 % num_hatches == i)

    global_rot += 0.0628

    gif_export(GifMaker, filename=SKETCH_NAME)

    if global_rot > PI * num_hatches:
        gif_export(GifMaker, finish=True)
        noLoop()


class Hatch:

    def __init__(self):
        self.n = int(random(20, 60))
        self.space = random(5, 15)
        self.half = self.n * self.space / 2.
        self.x = random(self.half, width - self.half)
        self.y = random(self.half, height - self.half)
        self.rot = random(TWO_PI)

    def plot(self, do_rotation):
        with pushMatrix():
            translate(self.x, self.y)
            rotate(self.rot)
            if do_rotation:
                rotate(global_rot)
            s, l = self.space, self.half
            #ellipse(0, 0, 5,5)

            for i in range(self.n):
                line(s * i - l, -l, s * i - l, l)


def print_text_for_readme(name, output):
    println("""
![{0}]({0}/{0}{2})

{1}: [code](https://github.com/villares/sketch-a-day/tree/master/{0}) [[Py.Processing](https://villares.github.io/como-instalar-o-processing-modo-python/index-EN)]

""".format(name, name[1:], output)
    )

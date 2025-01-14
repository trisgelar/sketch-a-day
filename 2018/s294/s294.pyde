# Alexandre B A Villares - https://abav.lugaralgum.com/sketch-a-day
SKETCH_NAME = "s294"  # 20181019
OUTPUT = ".gif"

NUM = 20 
BORDER = 50
SPACING = 20

def setup():
    global previous_points, next_points, points
    size(500, 500)
    frameRate(5 )
    points = previous_points = create_points(non_intersecting=False)
    
def create_points(non_intersecting=True):
    background(200)
    done = False
    while not done:
        points = [PVector(random(BORDER, width - BORDER),
                         random(BORDER, height - BORDER))
                  for _ in range(NUM)]
        edges = pairwise(points) + [(points[-1], points[0])]
        done = True
        if non_intersecting:
            for p1, p2 in edges:
                for p3, p4 in edges:
                    # test only non consecutive edges
                    if (p1 != p3) and (p2 != p3) and (p1 != p4):
                        if line_instersect(Line(p1, p2), Line(p3, p4)):
                            done = False
                            break
    return points
    
        

def draw():  

    stroke(0, 0, 100)
    fill(0, 0, 100)
    for x in range(0, width, SPACING):
           a = PVector(x, 0)
           b = PVector(x, height)
           inter_points = inter_line(points, Line(a, b))
           draw_inter(inter_points)
            
    stroke(100, 0, 0)
    fill(100, 0, 0)
    for y in range(0, height, SPACING):
           a = PVector(0, y)
           b = PVector(width, y)
           inter_points = inter_line(points, Line(a, b))
           draw_inter(inter_points)
    


def inter_line(points, L):                         
    edges = pairwise(points) + [(points[-1], points[0])]
    inter_points = []
    
    for p1, p2 in edges:
        # strokeWeight(2)
        # line(p1.x, p1.y, p2.x, p2.y)
        inter = line_instersect(Line(p1, p2), L)
        if inter:
            inter_points.append(inter)
    return inter_points   

def draw_inter(inter_points):
    if inter_points and len(inter_points) > 1:
        # strokeWeight(7)
        # for p in inter_points:
        #     point(p.x, p.y)
        strokeWeight(1)
        inter_points.sort()
        pairs = zip(inter_points[::2], inter_points[1::2])
        for p1, p2 in pairs:
            if p2:
               # noFill()
               ellipse(p1.x, p1.y, 5, 5)
               ellipse(p2.x, p2.y, 5, 5)
               line(p1.x, p1.y, p2.x, p2.y)    
    
def keyPressed():
    global points, next_points
    if key == " ": 
        points = create_points(non_intersecting=False)
    if key == "s": saveFrame("###.png")
        
class Line():
    """ I should change this to a named tuple... """
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
def line_instersect(line_a, line_b):     
    """
    code adapted from Bernardo Fontes 
    https://github.com/berinhard/sketches/
    """
       
    x1, y1 = line_a.p1.x, line_a.p1.y
    x2, y2 = line_a.p2.x, line_a.p2.y
    x3, y3 = line_b.p1.x, line_b.p1.y
    x4, y4 = line_b.p2.x, line_b.p2.y
        
    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
    except ZeroDivisionError:
        return 
        
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
        
    x = line_a.p1.x + uA * (line_a.p2.x - line_a.p1.x)
    y = line_a.p1.y + uA * (line_a.p2.y - line_a.p1.y)
        
    return PVector(x, y)


def pairwise(iterable):
    import itertools
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b) 

# print text to add to the project's README.md             
def settings():
    println(
"""
![{0}]({0}/{0}{2})

{1}: [code](https://github.com/villares/sketch-a-day/tree/master/{0}) [[Py.Processing](https://villares.github.io/como-instalar-o-processing-modo-python/index-EN)]
""".format(SKETCH_NAME, SKETCH_NAME[1:], OUTPUT)
    )

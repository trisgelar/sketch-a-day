from __future__ import division

def setup():
    size(600, 600)
    
def draw():
    background(0)
    grid_elem = 10
    spac_size = width / (grid_elem + 1)
    elem_size = spac_size
    v = spac_size * 1.5 / 2
    h = spac_size * sqrt(3)
    for ix in range(-1, grid_elem + 1):
        for iy in range(-1, grid_elem + 1):
            if iy % 2:
                x = ix * h + h / 4.0
            else:
                x = ix * h - h / 4.0
            if ix % 2:
                es = spac_size / 2 #* (0.9 + 0.1 * cos(radians(frameCount)))
            else:
                es = elem_size / 2
            y = iy * v
            tri(x, y +h, es , 0)
            tri(x, y +v, es , 2 * cos(radians(frameCount)))
            
def hexagon(x, y, r, rot=0):
    with pushMatrix():
        translate(x, y)
        beginShape()
        for i in range(6):
            sx = cos(i * TWO_PI / 6 + HALF_PI * rot) * r 
            sy = sin(i * TWO_PI / 6 + HALF_PI * rot) * r
            vertex(sx, sy)
        endShape(CLOSE)
        
def tri(x, y, r, rot=0):
    with pushMatrix():
        translate(x, y)
        beginShape()
        for i in range(3):
            sx = cos(i * TWO_PI / 3 + HALF_PI * rot) * r 
            sy = sin(i * TWO_PI / 3 + HALF_PI * rot) * r
            vertex(sx, sy)
        endShape(CLOSE)

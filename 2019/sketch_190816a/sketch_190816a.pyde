add_library('geomerative')

def setup():
    size(400, 400)
    strokeWeight(3)
    RG.init(this);
 
def draw():
    background(100)
    translate(width / 2, height / 2)
    
    r0= rg_rect(mouseX, mouseY, 200, 200, QUARTER_PI)
    r1= rg_ellipse(mouseX, -mouseY, 200, 200, 0)
    r2= rg_ellipse(-mouseX, -mouseY, 200, 200, QUARTER_PI / 2)
    r3= rg_rect(-mouseX, mouseY, 200, 200)

    resultado = RG.union( r0, r1 )
    resultado = RG.diff( resultado, r2 )
    resultado = RG.diff( resultado, r3 )
    RG.shape(resultado)
    

def rg_rect(x, y, w, h, rot=0):
    r = RShape.createRectangle(0, 0, w, h)
    r.translate(x - w/2, y - h/2)
    r.rotate(rot, RPoint(x, y))
    return r

def rg_ellipse(x, y, w, h, rot=0):
    r = RShape.createEllipse(0, 0, w, h)
    r.translate(x - w/2, y - h/2)
    r.rotate(rot, RPoint(x, y))
    return r

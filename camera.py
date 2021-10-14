from gl import *

pi = 3.14

#primer shader
def gourad(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty, = kwargs['tex_coords']
    vnA, vnB, vnC = kwargs['varying_normals']
    tcolor = render.current_texture.get_color(tx,ty)
    iA, iB, iC  = [dot(n, render.light) for n in (vnA, vnB, vnC)]  # esto da 3 intensidades

    intensity = w*iA + v*iB + u*iC
    return tcolor * intensity

r = Renderer(900, 900)
r.lookAt(V3(0, 0, 10), V3(0, 0, 0), V3(0, 1, 0))
# ------------ FONDO ------------------
t = Texture('./textures/museo.bmp')
r.framebuffer = t.pixels


# ------------- ESTATUA 1 ---------------
r.current_texture = Texture('./textures/e1.bmp')
r.load('./models/chica.obj', translate = (-0.5, -1, 0), scale = (1, 1, 1), rotate = (0, pi/6, 0))
r.active_shader= gourad
r.draw_array('TRIANGLES')

# ------------- GATO ---------------

r.current_texture = Texture('./textures/gatito.bmp')
r.load('./models/cat.obj', translate = (0.4, -2, -25), scale = (3, 3, 3), rotate = (0, -pi/10, 0))
r.active_shader= gourad
r.draw_array('TRIANGLES')

# ------------- BASEBALL ---------------

r.current_texture = Texture('./textures/baseball.bmp')
r.load('./models/baseball.obj', translate = (0, -4, -40), scale = (4, 4, 4), rotate = (0, 0, 0))
r.active_shader= gourad
r.draw_array('TRIANGLES')

# ------------- ESTATUA 2 ---------------

r.current_texture = Texture('./textures/e2.bmp')
r.load('./models/zombie.obj', translate = (-0.3, -1, -3), scale = (0.3, 0.3, 0.3), rotate = (0, pi/20, 0))
r.active_shader= gourad
r.draw_array('TRIANGLES')

# ------------- ESTATUA 3 ---------------
r.current_texture = Texture('./textures/e3.bmp')
r.load('./models/mei.obj', translate = (0.5, -1.4, 4), scale = (1, 1, 1), rotate = (0, -pi/4, 0))
r.active_shader= gourad
r.draw_array('TRIANGLES')




r.write('a.bmp')

 


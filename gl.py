
from obj import Obj, Texture
from lib import *
from math import sin, cos

class Renderer(object):
    def glinit():
        r =  Renderer(1024, 768)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Esta variable le da color al punto
        self.current_color = WHITE
        self.current_texture = None # en los triangulos se revisa la textura actual
        self.light = V3(1, 1, 1)
        self.textureC = None

        self.clear()

    def clear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]
        # hay que hacer un calculo en todos los pixeles, para ver cual corresponde en su coordenada en z
        self.zbuffer = [
            [-99999 for x in range(self.width)]
            for y in range(self.height)
        ]
        
    def write(self, filename):
        f = open(filename, 'bw')

        # File header (14)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Info header (40)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Bitmap (se recorre el framebuffer completo, para meter los bytes en un array de 4)
        for y in range(self.height):
            for x in range(self.width):
                try:
                    f.write(self.framebuffer[y][x].toBytes())
                except:
                    pass
        f.close()


 

    def render(self):
        self.write('a.bmp')

    def set_color(self, color):
        self.current_color = color

        # Se agregara un punto 
    def point(self, x, y, color = None):
        try:
            self.framebuffer[y][x] = color or self.current_color
        except:
            pass

#PARA EL LAB DE TIERRA SE IGNORA LA TEXTURA
    # funcion que recibe 3 vertices y dibuja un triangulo
    def triangle(self):
        A = next(self.active_vertex_array)  # permite acceder al siguiente elemento del array 
        B = next(self.active_vertex_array)
        C = next(self.active_vertex_array)

        if self.current_texture:
            vtA =  next(self.active_vertex_array)
            vtB =  next(self.active_vertex_array)
            vtC =  next(self.active_vertex_array)

        vnA =  next(self.active_vertex_array)
        vnB =  next(self.active_vertex_array)
        vnC =  next(self.active_vertex_array)


        bbox_min, bbox_max = bbox(A, B, C)
        

        # encontrar el rectangulo mas pequeño
        # se va marcando un punto
        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y + 1):
                # se toman las 3 coordenadas de triangulo y el punto P que es (x, y)
                P = V3(x,y)
                w, v, u = barycentric(A, B, C, P)
                # si alguna de las 3 es negativa quiere decir que esta afuera del triangulo
                if w  < 0 or v < 0 or u < 0:
                    continue # todo lo que este despues de continue no se va a ejecutar
                
                # solo si se tiene una textura 
                if self.current_texture:   # cuando se renderizan mas modelos, tiene mas sentido tener current_texture
                    
                    # CAMBIOOOOOOOOOO
                    # se va interpolar un triangulo dentro de otro
                    tx = vtA.x * w  + vtB.x * v + vtC.x * u #estas son las coordenadas que corresponden a x, y de este triangulo
                    ty = vtA.y * w + vtB.y * v + vtC.y * u

                    
                    color1 = self.active_shader(
                        self,
                        # triangle=(A,B,C),
                        bar = (w,v,u),
                        tex_coords = (tx,ty),
                        varying_normals = (vnA, vnB, vnC)
                        
                    )
                else:
                    color1 = WHITE
                    
                    # esto es para sacar colores del archivo de textura

                z = A.z * w + B.z * v + C.z * u # CAMBIOOOOOO
                
                   # SEGUIR ACA!

                if x < 0 or y < 0:
                    continue


                
                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                    self.point(x, y, color1)
                    self.zbuffer[x][y] = z

          

        # esta es una funcion que reciba un vertice como parametro que se transforma en X y Y
    def transform(self, v):
        a_vertex = [
            v[0],
            v[1],
            v[2],
            1
        ] # vertice aumentado 
        
        # CAMBIOOOO
        t_vertex = vector_multiply_list([a_vertex, self.Model, self.Projection, self.Viewport])

        # t_vertex = self.Viewport @ self.Projection @ self.View @ self.Model @ a_vertex # el vertice transformado es igual a matriz modelo por el vertice aumentado
        # t_vertex = t_vertex.tolist()[0] # esto se va al quitar numpy
        
        # print(t_vertex)
        
        # se necesita t_vertex de 3
        t_vertex = [
            t_vertex[0]/t_vertex[3],
            t_vertex[1]/t_vertex[3],
            t_vertex[2]/t_vertex[3]
        ]
        return V3(*t_vertex)

    
    

    # --------------- LINE ---------------
    
    #CAMBIOOOOOOOO
    # Esta funcion es para cargar y renderizar obj
    def load(self, filename, translate, scale, rotate): # ahora a load se le pasa que tanto se quiere que se mueva para los lados y abajo
        # al load se le agregara una textura para cargarla en el modelo 
        self.loadMatrix(translate, scale, rotate)
        model = Obj(filename)
        # se tienen que recorrer las caras, agarrar cada uno de los indices y pintar cada vertice
        vertex_buffer_obj = []     # array de vertices

        for face in model.faces:
            for v in range(len(face)):
                vertex1 =  self.transform(model.vertex[face[v][0] - 1])
                vertex_buffer_obj.append(vertex1)

            if self.current_texture:
                # si tiene una textura actual, se pueden meter los vertices de textura de una vez
                for v in range(len(face)):
                    tvertex =  V3(*model.tvertex[face[v][1] - 1])
                    vertex_buffer_obj.append(tvertex)
            for v in range(len(face)):
                try:

                    normal = norm(V3(*model.nvertex[face[v][2] - 1]))
                    vertex_buffer_obj.append(normal)
                except:
                    pass

        self.active_vertex_array =  iter(vertex_buffer_obj)

    # CAMBIOOOOOOOO
    # metodo para construir matrices. 
    def loadMatrix(self, translate, scale, rotate): 
        # todo el calculo de matriz se hara solo una vez
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        

        translate_m = createMatrix(4,4,
            [1, 0, 0, translate.x,
            0, 1, 0, translate.y,
            0, 0, 1, translate.z,
            0, 0, 0, 1])

        a = rotate.x # angulo de rotacion en x

        rotate_m_x = createMatrix(4,4,
            [1, 0, 0, 0,
            0, cos(a), -sin(a), 0,
            0, sin(a), cos(a), 0,
            0, 0, 0, 1])

        a = rotate.y # angulo de rotacion en y
        
        rotate_m_y = createMatrix(4,4,
            [cos(a), 0, sin(a), 0,  # aqui -sin(A) se convierte en sin(A) porque se revierte la rotacion en Y
            0, 1, 0, 0,
            -sin(a), 0, cos(a), 0,
            0, 0, 0, 1])

        a = rotate.z # angulo de rotacion en z

        rotate_m_z = createMatrix(4,4,
            [cos(a), -sin(a), 0, 0,
            sin(a), cos(a), 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1])

        rotate_m = matrix_multiply(rotate_m_x, matrix_multiply(rotate_m_y, rotate_m_z))

        # rotate_m = rotate_m_x @ rotate_m_y @ rotate_m_z

        scale_m = createMatrix(4,4,
            [scale.x, 0, 0, 0,
            0, scale.y, 0, 0,
            0, 0, scale.z, 0,
            0, 0, 0, 1])

        self.Model = matrix_multiply(translate_m, matrix_multiply(rotate_m, scale_m))
        # self.Model = translate_m @ rotate_m @ scale_m

    # se crea la matriz de vista que se puede utilizar para cambiar de base o punto
    def loadViewMatrix(self, x, y, z, center):
        M = createMatrix(4,4,
            [x.x, x.y, x.z, 0,
            y.x, y.y, y.z, 0,
            z.x, z.y, z.z, 0,
            0, 0, 0, 1]
        )

        O = createMatrix(4,4,
            [1, 0, 0, -center.x,
            0, 1, 0, -center.y,
            0, 0, 1, -center.z,
            0, 0, 0, 1]
        )

        # self.View = M @ O 
        self.View = matrix_multiply(M,O)


    def loadProjectMatrix(self, coeff):
        # se define la matriz de proyeccion
        self.Projection = createMatrix(4,4,
            [1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, coeff, 1]  # se quiere que el coeficiente dependa de z
        )
   
    # esta lleva las coordenadas a un espacio real
    def loadViewportMatrix(self, x = 0, y = 0):
 
        self.Viewport = createMatrix(4,4,
            [self.width/2, 0, 0, x + self.width/2,
            0, self.height/2, 0, y + self.height/2,
            0, 0, 1, 0,
            0, 0, 0, 1])
    
    def lookAt(self, eye, center, up): # donde esta la camara
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))

        self.loadViewMatrix(x, y, z, center)
        self.loadProjectMatrix(
            -1/length(sub(eye, center))
        ) # la distancia depende entre eye y center

        self.loadViewportMatrix(0,0)




    def draw_array(self, polygon):
        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle()
                    # print(self.triangle)
                    
            except StopIteration:
                print('Done')

  
        




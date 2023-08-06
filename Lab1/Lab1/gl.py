import struct
from collections import namedtuple
from obj import Obj
from numpi import Numpi
from texture import Texture
import math


V2= namedtuple('Point2', ['x', 'y'])
V3= namedtuple('Point', ['x', 'y', 'z'])

POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

def char(c):
    #1 byte
   return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int (b * 255),
                  int(g*255),
                  int(r*255)])


class Model(object):
    def __init__(self, filename, translate=(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        model= Obj(filename)

        self.vertices= model.vertices
        self.textcoords= model.texcoords
        self.normals= model.normals
        self.faces= model.faces

        self.translate= translate
        self.rotate= rotate
        self.scale= scale

            
    def LoadTexture(self, textureName):
        self.texture = Texture(textureName)

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.glClearColor(0,0,0)
        self.glClear()

        self.glColor(1,1,1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

    def glAddVertices(self, vertx):
        for vert in vertx:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self, tVerts):
        primitives = []

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVerts), 3):
                triangle = []
                triangle.append( tVerts[i] )
                triangle.append( tVerts[i + 1])
                triangle.append( tVerts[i + 2])
                primitives.append(triangle)

        return primitives

    def draw_lines(self, verti):
        i = 0
        while i + 1 < len(verti):
            self.glLine(verti[i], verti[i + 1])

            if i == len(verti) - 2:
                self.glLine(verti[i + 1], verti[0])
            i += 1

    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)
        
    def glColor(self,r,g,b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
        self.zbuffer = [[float('inf') for y in range(self.height)]
                       for x in range(self.width)]

    def glPoint(self, x, y, clr = None):
        if(0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def glTriangle_bc(self, A, B, C, vtA, vtB, vtC):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        colorA = (1,0,0)
        colorB = (0,1,0)
        colorC = (0,0,1)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                P = (x,y)
                
                try :
                    u,v,w = Numpi.barycentricCoords(A,B,C,P)
                    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1: 

                        z = u * A[2] + v * B[2] + w * C[2]

                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            uvs = (u * vtA[0] + v * vtB[0] + w * vtC[0],
                                   u * vtA[1] + v * vtB[1] + w * vtC[1]
                                  )

                            if self.fragmentShader != None:
                                colorP = self.fragmentShader(textCoords = uvs, 
                                                             texture = self.activetexture)
                                self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                            else:
                                self.glPoint(x, y, colorP)
                except:
                    pass



    def glModelMatrix(self, translate = (0,0,0), scale =(1,1,1), rotate=(0,0,0)):
        #np.matrix
        translation = [[1,0,0,translate[0]],
                      [0,1,0,translate[1]],
                      [0,0,1,translate[2]],
                      [0,0,0,1]]
        
        scaleMat = [[scale[0],0,0,0],
                   [0,scale[1],0,0],
                   [0,0,scale[2],0],
                   [0,0,0,1]]
        
        pitch = rotate[0] * math.pi/180
        yaw = rotate[1] * math.pi/180
        roll = rotate[2] * math.pi/180

        pitchMath = [[1,0,0,0],
            [0,math.cos(pitch),-math.sin(pitch),0 ],
            [0, math.sin(pitch), math.cos(pitch),0],
            [0,0,0,1]]
        
        yawMath =[[math.cos(yaw),0,math.sin(yaw),0],
            [0,1,0,0],
            [-math.sin(yaw),0,math.cos(yaw),0],
            [0,0,0,1]]
        
        rollMath =[[math.cos(roll),-math.sin(roll),0,0],
            [math.sin(roll),math.cos(roll),0,0],
            [0,0,1,0],
            [0,0,0,1]]
        

        Rxy = Numpi.multMatrices(pitchMath,yawMath)
        MatrixRot = Numpi.multMatrices(Rxy, rollMath)
        Mtr = Numpi.multMatrices(translation, MatrixRot)
        result = Numpi.multMatrices(Mtr, scaleMat)
        
        return result #translation * scaleMat#multiplicación matriz 4 * 4
    
    #def fill_polygon(self, vertices, point_to_skip):
    #    if len(vertices) < 3:
    #        return

    #    # Encuentra los límites de la caja que contiene el polígono.
    #    min_x = min(vertices, key=lambda v: v.x).x
    #    max_x = max(vertices, key=lambda v: v.x).x
    #    min_y = min(vertices, key=lambda v: v.y).y
    #    max_y = max(vertices, key=lambda v: v.y).y

    #    # Itera sobre cada punto (x, y) dentro de la caja del polígono
    #    for x in range(min_x, max_x + 1):
    #        for y in range(min_y, max_y + 1):
    #            if self.is_point_inside_polygon(x, y, vertices) and (x, y) != point_to_skip:
    #                self.glPoint(x, y, color(1, 0.5, 0.5))



    #def is_point_inside_polygon(self, x, y, vertices):
    #    n = len(vertices)
    #    inside = False
    #    p1x, p1y = vertices[0]
    #    for i in range(n + 1):
    #        p2x, p2y = vertices[i % n]
    #        if y > min(p1y, p2y):
    #            if y <= max(p1y, p2y):
    #                if x <= max(p1x, p2x):
    #                    if p1y != p2y:
    #                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
    #                    if p1x == p2x or x <= xinters:
    #                        inside = not inside
    #        p1x, p1y = p2x, p2y
    #    return inside


    def glLine(self, v0, v1, clr= None):
 
        x0 = int(v0[0])
        x1 = int(v1[0])        
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y1 == y0: #Si los vertices son el mismo, dibuja un punto
            self.glPoint(x0, y0)

            return 
        
        dx= abs(x1 - x0)
        dy= abs(y1 - y0)

        steep= dy > dx

        if steep: #Si la pendiente es mayor a 1 o menor a -1
            #Intercambio de valores
            x0, y0 = y0, x0
            x1, y1= y1, x1

        if x0 > x1: #Si la linea va de derecha a izquierda, se intercambian valores para dibujarlos de izquierda a derecha
            x0, x1= x1, x0
            y0, y1= y1, y0

        dx= abs(x1 - x0)
        dy= abs(y1 - y0)


        offset= 0
        limit= 0.5

        m = dy / dx
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep: #Dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)

            else: #Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1: #Dibujando de abajo para arriba
                    y += 1
                
                else: #Dibujando de arriba para abajo
                    y -= 1

                limit += 1 
    
    def glLoadModel(self, filename, translate= (0,0,0), rotate=(0,0,0), scale= (1,1,1)):
        model = Model(filename, translate, rotate, scale)
        #model.LoadTexture(textureName)
        
        self.objects.append(model)

    def glRender(self):
        transformedVerts = []
        textCoords = []
        
        for model in self.objects:
            self.activetexture= model.texture

            modelMatrix = self.glModelMatrix(model.translate, model.scale, model.rotate)


            for face in model.faces:
                vertCount= len(face)

                v0= model.vertices[face[0][0] - 1]
                v1= model.vertices[face[1][0] - 1]
                v2= model.vertices[face[2][0] - 1]

                if vertCount==4:
                    v3= model.vertices[face[3][0] - 1]

                if self.vertexShader:
                    v0= self.vertexShader(v0, modelMatrix= modelMatrix)
                    v1= self.vertexShader(v1, modelMatrix= modelMatrix)
                    v2= self.vertexShader(v2, modelMatrix= modelMatrix)

                    if vertCount==4:
                        v3= self.vertexShader(v3, modelMatrix= modelMatrix)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)

                if vertCount==4:
                    transformedVerts.append(v3)
                    transformedVerts.append(v1)
                    transformedVerts.append(v2)

        primitive= self.glPrimitiveAssembly(transformedVerts)


        for prim in primitive:
            if self.primitiveType == TRIANGLES:
                self.glTriangle_bc(prim[0], prim[1], prim[2], 
                                   prim[3],prim[4],prim[5])

        
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            #infoheader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #color table
            for y in range(self.height):
                for x in range (self.width):
                    file.write(self.pixels[x][y])

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
        self.texcoords = model.texcoords
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

        self.activetexture = None

        self.glViewport(0,0,self.width, self.height)
        self.glCamMatrix()
        self.glProjectionMatrix()

    def glAddVertices(self, vertx):
        for vert in vertx:
            self.vertexBuffer.append(vert)

    
    def glPrimitiveAssemly(self, tVerts, tTextCoords):
        primitives = []
        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVerts), 3):
                triangle = []
                #vertices
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2])
                #texturas
                triangle.append(tTextCoords[i])
                triangle.append(tTextCoords[i+1])
                triangle.append(tTextCoords[i+2])

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



    def glTriangle(self, verts, texCoords,normals):
        # Rederización de un triángulo usando coordenadas baricéntricas.
        # Se reciben los vertices A, B y C y las coordenadas de
        # textura vtA, vtB y vtC
        A= verts[0]
        B= verts[1]
        C= verts[2]

        # Bounding box
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        # Para cada pixel dentro del bounding box
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # Si el pixel está dentro del FrameBuffer
                if (0 <= x < self.width) and (0 <= y < self.height):

                    P = (x,y)
                    bCoords = Numpi.barycentricCoords(A, B, C, P)

                    # Si se obtienen coordenadas baricéntricas válidas para este punto
                    if bCoords != None:

                        u, v, w = bCoords

                        # Se calcula el valor Z para este punto usando las coordenadas baricéntricas
                        z = u * A[2] + v * B[2] + w * C[2]

                        # Si el valor de Z para este punto es menor que el valor guardado en el Z Buffer
                        if z < self.zbuffer[x][y]:
                            
                            # Guardamos este valor de Z en el Z Buffer
                            self.zbuffer[x][y] = z

                
                            # Si contamos un Fragment Shader, obtener el color de ahí.
                            # Sino, usar el color preestablecido.
                            if self.fragmentShader != None:
                                # Mandar los parámetros necesarios al shader
                                
                                
                                
                                colorP = self.fragmentShader(texture = self.activeTexture,
                                                             texCoords = texCoords,
                                                             normals = normals,
                                                             dLight = self.directionalLight,
                                                             bCoords = bCoords)


                                self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                                
                            else:
                                self.glPoint(x, y)


    def glViewport(self, x, y, width, height):
        self.vpX =  x
        self.vpY =  y 
        self.vpWidth = width
        self.vpHeight = height 

        self.vpMatrix = [[self.vpWidth/2,0,0,self.vpX + self.vpWidth/2],
                        [0,self.vpHeight/2,0,self.vpY + self.vpHeight/2],
                        [0,0,0.5,0.5],
                        [0,0,0,1]]


    def glCamMatrix(self, translate=(0,0,0) , rotate = (0,0,0)):
        #matriz de camara
         #Crea matrix de camara
        self.camMatrix = self.glModelMatrix(translate, rotate)
        
        #Matriz de vista es igual a la inversa de la camara
        self.viewMatrix = Numpi.inverse_matrix(self.camMatrix)

            
    def glLookAt(self, camPos = (0,0,0), eyePos = (0,0,0)):
        worldUp = (0,1,0)
        
        forward = Numpi.norm_vector(Numpi.vecResta(camPos, eyePos))
        right = Numpi.norm_vector(Numpi.vecMulti(worldUp, forward))
        up = Numpi.norm_vector(Numpi.vecMulti(forward, right))
        
        self.camMatrix = [[right[0],up[0],forward[0],camPos[0]],
                          [right[1],up[1],forward[1],camPos[1]],
                          [right[2],up[2],forward[2],camPos[2]],
                          [0,0,0,1]]
        
        self.viewMatrix = Numpi.inverse_matrix(self.camMatrix)
        
    def glProjectionMatrix(self, fov = 60, n= 0.1, f = 1000):
        aspectRatio = self.vpWidth / self.vpHeight

        t = math.tan((fov * math.pi/180)/2)  * n
        r = t * aspectRatio

        self.projectionMatrix = [[n/r,0,0,0],
                                [0,n/t,0,0],
                                [0,0,-(f+n)/(f-n),-2*f*n/(f-n)],
                                [0,0,-1,0]]

    def glModelMatrix(self, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):
        #np.matrix
        translation = [[1,0,0,translate[0]],
                      [0,1,0,translate[1]],
                      [0,0,1,translate[2]],
                      [0,0,0,1]]
        
                # Matrix de rotación
        
        
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
    
    def glLoadModule(self, filename, textureName, translate = (0,0,0),rotate = (0,0,0), scale = (1,1,1)):
        print(f"Loading module: {filename}")
        print(f"Loading texture: {textureName}")
        
        model = Model(filename, translate, rotate, scale)
        model.LoadTexture(textureName)
        
        self.objects.append(model)

    def glRender(self):
        transformedVerts = []
        textCoords = []

        for model in self.objects:
            
            self.activetexture= model.texture

            mMat = self.glModelMatrix(model.translate, model.rotate, model.scale)

            for face in model.faces:
                verCount = len(face)

                v0 = model.vertices[ face[0][0]-1]
                v1 = model.vertices[ face[1][0]-1]
                v2 = model.vertices[ face[2][0]-1]
                if verCount == 4:
                    v3 = model.vertices[ face[3][0]-1]

                if self.vertexShader:
                    v0 = self.vertexShader(v0, 
                                           modelMatrix = mMat,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                    v1 = self.vertexShader(v1, 
                                           modelMatrix = mMat,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                    v2 = self.vertexShader(v2,
                                           modelMatrix = mMat,
                                           viewMatrix = self.viewMatrix,
                                           projectionMatrix = self.projectionMatrix,
                                           vpMatrix = self.vpMatrix)
                    if verCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix = mMat,
                                                viewMatrix = self.viewMatrix,
                                                projectionMatrix = self.projectionMatrix,
                                                vpMatrix = self.vpMatrix)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if verCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)
                
                vt0 = model.texcoords[face[0][1]-1]
                vt1 = model.texcoords[face[1][1]-1]
                vt2 = model.texcoords[face[2][1]-1]
                if verCount == 4:
                    vt3 =  model.texcoords[face[3][1]-1]
                textCoords.append(vt0)
                textCoords.append(vt1)
                textCoords.append(vt2)
                if verCount == 4:
                    textCoords.append(vt0)
                    textCoords.append(vt2)
                    textCoords.append(vt3)

        primitives = self.glPrimitiveAssemly(transformedVerts, textCoords)       

        for prim in primitives: 
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

from gl import Renderer, V2, V3, color
import shaders  
import random
from obj import Obj

width = 800
height = 800

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader


rend.glLoadModule(filename= "blooddragon.obj", textureName="dino2.bmp",
                translate=(80,20,0), 
                scale=(20,20,20), 
                rotate=(-90,0,0))

rend.glRender()

rend.glFinish("output1.bmp")
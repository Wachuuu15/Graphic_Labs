from gl import Renderer, V2, V3, color
import shaders  
import random
from obj import Obj

width = 900
height = 900

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader


rend.glLoadModule(filename= "13499_Balloon_Cluster_v1_L2.obj", textureName="hea.bmp",
                translate=(110,20,0), 
                scale=(10,10,10), 
                rotate=(-90,0,0))

rend.glLoadModule(filename= "13499_Balloon_Cluster_v1_L2.obj", textureName="hea.bmp",
                translate=(140,500,0), 
                scale=(10,10,10), 
                rotate=(-90,0,-45))

rend.glLoadModule(filename= "13499_Balloon_Cluster_v1_L2.obj", textureName="hea.bmp",
                translate=(400,20,0), 
                scale=(10,10,10), 
                rotate=(-90,0,180))


rend.glLoadModule(filename= "13499_Balloon_Cluster_v1_L2.obj", textureName="hea.bmp",
                translate=(400,300,0), 
                scale=(10,10,10), 
                rotate=(-90,2,45))


rend.glRender()

rend.glFinish("output1.bmp")
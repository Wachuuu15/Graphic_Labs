from gl import Renderer, V2, V3, color
import shaders  
from obj import Obj

width = 900
height = 900

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.waterShader


rend.glLookAt(camPos = (0,0,3), eyePos= (0,0,-5))

rend.glLoadModule(filename = "pinguin_001.obj",
                 textureName = "animals-texture.bmp",
                 translate = (0,-2,-5),
                 rotate = (0, 140, 0),
                 scale = (3,3,3))



rend.glRender()

rend.glFinish("output22.bmp")
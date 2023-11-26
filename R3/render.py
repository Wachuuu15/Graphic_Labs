from gl import Renderer
import shaders  

width = 900
height = 900

modelFile = "obj/13499_Balloon_Cluster_v1_L2.obj"
textureFile = "texture/hea.bmp"
exitFile = "photoshoots/mediumShot.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

#  Medium Shot 
rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

#  Low Angle 
#rend.glLookAt(camPos = (0,-3,-2), eyePos= (0,0,-5))

#  High Angle 
#rend.glLookAt(camPos = (0,3,-1), eyePos= (0,0,-5))

#  Dutch Angle 
#rend.glLookAt(camPos = (-3,-2,-2), eyePos= (0,0,-5))
        
rend.glLoadModel(filename = modelFile,
                 textureName = textureFile,
                 translate = (0,0,-5),
                 rotate = (0, 0, 0),
                 scale = (3,3,3))

rend.glRender()

rend.glFinish(exitFile)
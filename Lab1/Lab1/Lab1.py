from gl import Renderer, Model
import shaders  
from obj import Obj

width = 900
height = 640

rend = Renderer(width, height)

rend.glBackgroundTexture("texturee/wallpaperflare_pesa.bmp")
rend.glClearBackground()

rend.directionalLight=(0,-0.3,-0.8)

rend.glLookAt(camPos=(0, 2, 0),
              eyePos=(0,2,-5))

# Luna
model1 = Model("obj/Moon_2K.obj", 
             translate = (9,5, -14),
               rotate = (0, 0,0),
             scale = (0.01,0.01,0.01))

model1.LoadTexture("texturee/Diffuse_2K.bmp")
model1.SetShaders(shaders.vertexShader, shaders.moonShader)

# Avion
model2 = Model("obj/11804_Airplane_v2_l2.obj",
               translate= (-4, -1, -20),
               rotate = (10, -5, -220),
              scale = (0.01,0.01,0.01))

model2.LoadTexture("texturee/11804_Airplane_diff.bmp")
model2.SetShaders(shaders.vertexShader, shaders.gouradShader)

# Rosa
model3 = Model("obj/rose.obj", 
              translate=(1,0,-8),
               scale = (0.01,0.01,0.01))

model3.LoadTexture("texturee/5177491.bmp")
model3.SetShaders(shaders.vertexShader, shaders.roseShader)


# Zorro
model4 = Model("obj/13577_Tibetan_Hill_Fox_v1_L3.obj", 
              translate=(3,0,-5),
               rotate = (10, -5, 0),
              scale = (0.01,0.01,0.01))

model4.LoadTexture("texturee/Tibetan_Hill_Fox_dif.bmp")
model4.SetShaders(shaders.vertexShader, shaders.gouradShader)


# Jupiter
model5 = Model("obj/Venus_1K.obj", 
             translate= (-4, 6, 0),
             scale = (0.01,0.01,0.01))

model5.LoadTexture("texturee/grass_texture225.bmp")
model5.SetShaders(shaders.vertexShader, shaders.grassShader)


rend.glAddModel(model1)
rend.glAddModel(model2)
rend.glAddModel(model3)
rend.glAddModel(model4)
rend.glAddModel(model5)

# se renderiza la escena
rend.glRender()

# Framme buffer con la escena final-renderizada
rend.glFinish("outputescenefinish.bmp")
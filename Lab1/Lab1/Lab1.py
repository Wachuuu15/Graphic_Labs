
from gl import Renderer, V2, V3, color
import shaders  
import random
from obj import Obj

width = 8000
height = 8000

rend = Renderer(width, height)

#verti =[V2(165, 380),
#         V2(185, 360),
#         V2(180, 330),
#         V2(207, 345),
#         V2(233, 330),
#         V2(230, 360),
#         V2(250, 380),
#         V2(220, 385),
#         V2(205, 410),
#         V2(193, 383)]

#verti2 =[V2(321, 335),
#         V2(288, 286),
#         V2(339, 251),
#         V2(374, 302)]

#verti3 =[V2(377, 249),
#         V2(411, 197),
#         V2(436, 249)]

#verti4 = [V2(413, 177),
#         V2(448, 159),
#         V2(502, 88),
#         V2(553, 53),
#         V2(535, 36),
#         V2(676, 37),
#         V2(660, 52),
#         V2(750, 145),
#         V2(761, 179),
#         V2(672, 192),
#         V2(659, 214),
#         V2(615, 214),
#         V2(632, 230),
#         V2(580, 230),
#         V2(597, 215),
#         V2(552, 214),
#         V2(517, 144),
#         V2(466, 180)]

#verti5 = [V2(682, 175),
#         V2(708, 120),
#         V2(735, 148),
#         V2(739, 170)]

##ciclo dos

## Llamada a la función draw_lines desde Renderer
#rend.draw_lines(verti)
#rend.draw_lines(verti2)
#rend.draw_lines(verti3)
#rend.draw_lines(verti4)
#rend.draw_lines(verti5)


## Rellenar los polígonos
#rend.fill_polygon(verti, V2(0, 0))  # Puedes reemplazar V2(0, 0) con la coordenada que desees omitir
#rend.fill_polygon(verti2, V2(0, 0))
#rend.fill_polygon(verti3, V2(0, 0))
#rend.fill_polygon(verti4, V2(580, 230))
#rend.fill_polygon(verti5, V2(0, 0))

triangle = [(100, 100), (450, 180), (250, 500)]

rend.glTriangle_bc(triangle[0], triangle[1], triangle[2])
rend.glFinish("output.bmp")
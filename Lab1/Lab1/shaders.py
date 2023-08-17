from numpi import Numpi

def vertexShader(vertex, **kwards):
    modelMatrix = kwards["modelMatrix"]
    viewMatrix = kwards["viewMatrix"]
    projectionMatrix = kwards["projectionMatrix"]
    vpMatrix = kwards["vpMatrix"]


    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]


    #simbolo de numpy para sacar una matriz de tipo vector
    vt = Numpi.mulVect(vpMatrix, projectionMatrix, viewMatrix, modelMatrix, vt)

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

def fragmentShader(**kwards):
    textCoords = kwards["textCoords"]
    texture = kwards["texture"]

    if texture != None:
        color = texture.getColor(textCoords[0], textCoords[1])
    else:
        color = (1,1,1)

    return color

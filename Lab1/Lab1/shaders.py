from numpi import Numpi
import random
import math
import time


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


def flatShader(**kwargs):
    dLight = kwargs["dLight"]
    normal= kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = Numpi.productoPunto(normal, negativedLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]

def gouradShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= (u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2])
    
    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = Numpi.productoPunto(normal, negativedLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return (0,0,0)

def inverseShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]

    if texture != None:
        color = texture.getColor(tA[0],tA[1])
        inverted_color = (1 - color[0], 1 - color[1], 1 - color[2])
    else:
        inverted_color = (0, 0, 0)

    return inverted_color

def deepFryShader(**kwargs):
    tA, tB, tC= kwargs["texCoords"]
    texture = kwargs["texture"]
    grain_intensity = 0.2
    
    if texture != None:
        color = texture.getColor(tA[0], tA[1])
        
        r = min(0.1 +1.5 * color[0], 1)
        g = min(1.5 * color[1], 1)
        b = min(1.5 * color[2], 1)
        
        r += random.uniform(-grain_intensity, grain_intensity)
        g += random.uniform(-grain_intensity, grain_intensity)
        b += random.uniform(-grain_intensity, grain_intensity)

        r = min(max(r, 0), 1)
        g = min(max(g, 0), 1)
        b = min(max(b, 0), 1)

        
        return r, g, b
    else:
        return (1, 1, 1)


def waterShader(**kwargs):
    texCoords = kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    
    amplitude = 0.6  # Adjust the wave amplitude
    frequency = 4.0  # Adjust the wave frequency
    time = 2.5  # Use a time value to animate the waves
    
    
    displacement = amplitude * math.sin(u * frequency + time) * math.cos(v * frequency + time)

    # Adjust the normal by the displacement to simulate waves
    distorted_normal = (
        nA[0] + displacement,
        nA[1] + displacement,
        nA[2]
    )

    
    intensity = Numpi.productoPunto(distorted_normal, dLight)
    
    # Apply color and lighting to the water
    r = 0.4 + 0.5 * intensity
    g = 0.3 + 0.7 * intensity
    b = 0.8 + 0.2 * intensity
    
    r = min(max(r, 0), 1)
    g = min(max(g, 0), 1)
    b = min(max(b, 0), 1)
    
    return r, g, b

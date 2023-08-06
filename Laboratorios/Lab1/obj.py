class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines= file.read().splitlines()

        self.vertices= []
        self.texcoords=[]
        self.normals=[]
        self.faces=[]

        for line in self.lines:
            try:
                prefix, value= line.split(" ", 1)

            except:
                continue

            if prefix== "v": #Si es un vertice
                if value.endswith(" "):
                    value = value.rstrip()
                    
                self.vertices.append(list(map(float, filter(lambda x: x != '', value.split(" ")))))
                
            elif prefix== "vt": #Si es una textura
                if value.endswith(" "):
                    value = value.rstrip()
                    
                self.texcoords.append(list(map(float, value.split(" "))))

            elif prefix== "vn": #Si es una normal
                if value.endswith(" "):
                    value = value.rstrip()
                    
                    
                self.normals.append(list(map(float, value.split(" "))))

            elif prefix == "f":
                vals = value.rstrip()
                self.faces.append([list(map(int, vert.split("/"))) for vert in vals.split(" ")])
    

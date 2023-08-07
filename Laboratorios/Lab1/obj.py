class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()
        
        self.vertices = []
        self.texcoords = []
        self.normal = []
        self.faces = []

        for line in self.lines:

            try:
                prefix , val = line.split(" ", 1)
            except:
                continue
            
            if prefix == "v":
                self.vertices.append(list(map(float, val.split(" "))))
            elif prefix == "vt":
                self.texcoords.append(list(map(float, val.split(" "))))    
            if prefix == "vn":
                self.normal.append(list(map(float, val.split(" "))))
            elif prefix == "f":
                vals = val.rstrip()
                self.faces.append([list(map(int, vert.split("/"))) for vert in vals.split(" ")])
    

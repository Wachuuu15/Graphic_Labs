import math
class Numpi:
    def multMatrices(m1, m2):
        if len(m1[0]) == len(m2):
            matRes = [[0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0]]

            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        matRes[i][j] += (m1[i][k] * m2[k][j])

            return matRes

    def mulVect(m1, vector):
        vecRes = [0.0, 0.0, 0.0, 0.0]
        for i in range(4):
            for j in range(4):
                vecRes[i] += (m1[i][j] * vector[j])

        return vecRes

    def barycentricCoords(A,B,C,P):
            areaPCB = ((B[1]-C[1]) * (P[0]-C[0]) + (C[0]-B[0]) * (P[1]-C[1])) 
            areaACP = ((C[1]-A[1]) * (P[0]-C[0]) + (A[0]-C[0]) * (P[1]-C[1])) 
            areaABC = ((B[1]-C[1]) * (A[0]-C[0]) + (C[0]-B[0]) * (A[1]-C[1])) 
            
            if areaABC == 0:
            
                return None

            u = areaPCB / areaABC
            v = areaACP / areaABC
            w = 1 - u -v

            return u, v, w 
    
    def getMatrixMinor(self,matrix,i,j):
        return [row[:j] + row[j+1:] for row in (matrix[:i]+matrix[i+1:])] #minor matrix

    def matrixDeterm(self,matrix):
        if len(matrix) == 2: #case for 2x2 matrix
            return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
        determinant = 0
        for c in range(len(matrix)):
            determinant += ((-1) ** c) * matrix[0][c] * matrixDeterm(getMatrixMinor(matrix, 0, c))
        return determinant

    def invMatrix(self,mx):
        det = matrixDeterm(mx)
        if det == 0:
            print('Determinant is zero')
            return

        if len(mx) == 2:  # case for 2x2 matrix
            return [[mx[1][1] / det, -1 * mx[0][1] / det],
                    [-1 * mx[1][0] / det, mx[0][0] / det]]

        cofactors = []
        for i in range(len(mx)):
            cofactRow = []
            for j in range(len(mx)):
                minorValue = getMatrixMinor(mx, i, j)
                cofactRow.append(((-1) ** (i + j)) * matrixDeterm(minorValue))
            cofactors.append(cofactRow)

        inverse = list(map(list, zip(*cofactors)))  # ...
        for i in range(len(inverse)):
            for j in range(len(inverse)):
                inverse[i][j] = inverse[i][j] / det
        return inverse

    def substractionVectors(a,b):
        return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

    def prodCrossV(a,b):
        cross_product = [a[1] * b[2] - a[2] * b[1],
                        a[2] * b[0] - a[0] * b[2],
                        a[0] * b[1] - a[1] * b[0]]
        return cross_product

    def normalizeVector(vector):
        vectorList = list(vector)
        magnitude = math.sqrt(sum(e ** 2 for e in vectorList))
        if magnitude == 0: #error if magnitude is 0
            print("Unable to normalize")
        
        normVector = [e / magnitude for e in vectorList]
        return tuple(normVector)
        
    def dotProd(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))
    
def getMatrixMinor(matrix,i,j):
    return [row[:j] + row[j+1:] for row in (matrix[:i]+matrix[i+1:])] #minor matrix

def matrixDeterm(matrix):
    if len(matrix) == 2: #case for 2x2 matrix
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    determinant = 0
    for c in range(len(matrix)):
        determinant += ((-1) ** c) * matrix[0][c] * matrixDeterm(getMatrixMinor(matrix, 0, c))
    return determinant

def invMatrix(mx):
    det = matrixDeterm(mx)
    if det == 0:
        print('Determinant is zero')
        return

    if len(mx) == 2:  # case for 2x2 matrix
        return [[mx[1][1] / det, -1 * mx[0][1] / det],
                [-1 * mx[1][0] / det, mx[0][0] / det]]

    cofactors = []
    for i in range(len(mx)):
        cofactRow = []
        for j in range(len(mx)):
            minorValue = getMatrixMinor(mx, i, j)
            cofactRow.append(((-1) ** (i + j)) * matrixDeterm(minorValue))
        cofactors.append(cofactRow)

    inverse = list(map(list, zip(*cofactors)))  # ...
    for i in range(len(inverse)):
        for j in range(len(inverse)):
            inverse[i][j] = inverse[i][j] / det
    return inverse
    
matrix = [[1,2,3],
          [4,5,6],
          [7,88,9]]

print(invMatrix(matrix))

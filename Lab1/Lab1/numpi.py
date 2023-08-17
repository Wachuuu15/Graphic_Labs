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
    
    
    def invertir_matriz(matriz):
        n = len(matriz)
        matriz_identidad = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

        for i in range(n):
            diagonal_elem = matriz[i][i]
            if diagonal_elem == 0:
                raise ValueError("La matriz no tiene inversa")

            Numpi.escalar_fila(matriz, i, 1.0 / diagonal_elem)
            Numpi.escalar_fila(matriz_identidad, i, 1.0 / diagonal_elem)

            for j in range(n):
                if j != i:
                    factor = -matriz[j][i]
                    Numpi.sumar_filas(matriz, j, i, factor)
                    Numpi.sumar_filas(matriz_identidad, j, i, factor)

        return matriz_identidad

    @staticmethod
    def escalar_fila(matriz, fila, escalar):
        matriz[fila] = [elem * escalar for elem in matriz[fila]]

    @staticmethod
    def sumar_filas(matriz, fila_destino, fila_origen, factor):
        matriz[fila_destino] = [elem_dest + factor * elem_orig for elem_dest, elem_orig in zip(matriz[fila_destino], matriz[fila_origen])]

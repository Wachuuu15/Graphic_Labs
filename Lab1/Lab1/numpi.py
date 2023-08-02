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
        
            try:
                u= areaPCB/areaABC
                v= areaACP/areaABC
                w= 1-u-v
                return u,v,w
            except:
                return -1,-1,-1
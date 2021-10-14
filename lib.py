import struct

# -------------------- NUMPY ---------------------

# este codigo fue extraido de: https://integratedmlai.com/basic-linear-algebra-tools-in-pure-python-without-numpy-or-scipy/

def createMatrix(rowCount, colCount, dataList):
    mat = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            # you need to increment through dataList here, like this:
            rowList.append(dataList[rowCount * i + j])
        mat.append(rowList)

    return mat
def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
 
        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)
 
    return M
def matrix_multiply(A, B):
    """
    Returns the product of the matrix A * B
        :param A: The first matrix - ORDER MATTERS!
        :param B: The second matrix
 
        :return: The product of the two matrices
    """
   
    # Section 1: Ensure A & B dimensions are correct for multiplication
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if colsA != rowsB:
        raise ArithmeticError(
            'Number of A columns must equal number of B rows.')
 
    # Section 2: Store matrix multiplication in a new matrix
    C = zeros_matrix(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total
 
    return C

def matrix_vector_multiply(A, B):
    rowsV = len(B)
    colsM = len(A)
    F = [0,0,0,0]

    for i in range(rowsV):
        res = 0
        for j in range(colsM):
            res += A[i][j] * B[j] 
        F[i] = res

    return F


def vector_multiply_list(arrayMatrix):
    vector1 = arrayMatrix[0]
    matrix_result = zeros_matrix(4,4)
    matrix_result = matrix_vector_multiply(arrayMatrix[1], vector1)
    for matrix in arrayMatrix[2:]:
        matrix_result = matrix_vector_multiply(matrix, matrix_result)
 
    return matrix_result



# -------------------- NUMPY ---------------------


# clase vertice que se pueda sumar con el operador + 
class V3(object):   # hay que hacer overwrites
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    # metodo para imprimir algo 
    def __repr__(self):
        return "V3(%s, %s, %s)" %(self.x, self.y, self.z)
def clamp_color(v):
    return max(0, min(255, int(v)))

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    # metodo para imprimir algo 
    def __repr__(self):
        b = clamp_color(self.b) # cual es el valor minimo entre 255 y self.b
        g = clamp_color(self.g)
        r = clamp_color(self.r)
        return "color(%s, %s, %s)" % (r, g, b)

    def toBytes(self):
        b = clamp_color(self.b) # cual es el valor minimo entre 255 y self.b
        g = clamp_color(self.g)
        r = clamp_color(self.r)

        return bytes([b, g, r])

    # suma de colores
    def __add__(self, other):
        r = clamp_color(self.r + other.r)
        g = clamp_color(self.g + other.g)
        b = clamp_color(self.b + other.b)
        return color(r, g, b)

    # multiplica de colores
    def __mul__(self, k):
        r = clamp_color(self.r * k)
        g = clamp_color(self.g * k)
        b = clamp_color(self.b * k)
        return color(r, g, b)


def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short
    return struct.pack('=h', w)

def dword(w):
    # long
    return struct.pack('=l', w)


BLACK =  color(0, 0, 0)
WHITE =  color(255, 255, 255)


# este bounding box va a recibir los 3 parametros A,B,C
def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    # zs = [A.z, B.z, C.z]
    # zs.sort()
    # se utiliza -1 para regresar al ulitmo valor del array
    return V3(round(xs[0]), round(ys[0])), V3(round(xs[-1]), round(ys[-1]))


def cross(v0, v1):
    # el producto cruz entre 3 vectores se calcula
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):
    # calcular producto cruz entre dos vectores para calcular las 3 variables.
    bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )
    cx, cy, cz = bary.__getitem__(0), bary.__getitem__(1), bary.__getitem__(2)
    
    if abs(cz) < 1:
        return -1, -1, -1

    # if abs(bary[2]) < 1:
    #     return -1, -1, -1    # con esto se evita la division entre 0

    w = 1 - (cx + cy) / cz 
    v = cy / cz
    u = cx / cz 


    # # para forzar a que uno sea 1 hay que dividirlos a todos entre cz
    # w = 1 - (bary[0] + bary[1]) / bary[2]
    # v = bary[1] / bary[2]
    # u = bary[0] / bary[2]  # siempre que aparezca una división, hay una posibilidad que cz de 0. Esto significa que el triangulo es solo una linea

    # si ya tenemos herramienta, modulo que se va a priorizar sobretoido el valor de cleinte ubicar que clase o metodos hay que trabajar primero. se tiene que considerar refactorizarlo 
    # que framework de pruebas se van a utilizar.

    return w, v, u


def sub(v0, v1):
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
        v0.z - v1.z,
    )
def length(v0):
    return(v0.x**2 + v0.y**2 +v0.z**2) ** 0.5

def norm(v0):
    l = length(v0)
    if l ==0:
        return V3(0,0,0)

    return V3(
        v0.x / l,
        v0.y / l,
        v0.z / l
    )

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z